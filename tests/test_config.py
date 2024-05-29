"""Unit Tests for importphotos.config module."""
import argparse
import configparser
import pytest
import os

from importphotos.config import Config

def input_config():
    """Test data for Config class."""
    return {
        "DEFAULT": {
            "source_dir": "tests/data",
            "destination_dir": "tests/data",
            "file_types": ".jpg, .jpeg, .arw",
        }
    }

def expected_config():
    return {
        "DEFAULT": {
            "source_dir": "tests/data",
            "destination_dir": "tests/data",
            "file_types": (".JPG", ".JPEG", ".ARW"),
        }
    }
def get_test_data_item(group, key):
    if key.lower().endswith("s"):
        return [item.strip() for item in input_config()[group][key].split(",")]
    return input_config()[group][key]

def get_expected_item(group, key):
    if key.lower().endswith("s"):
        return [item.strip() for item in expected_config()[group][key].split(",")]
    return expected_config()[group][key]

expected_config_str = "source_dir=tests/data, destination_dir=tests/data, file_types=.JPG, .JPEG, .ARW"
expected_config_repr = f"Config({expected_config_str})"



def test_config_init(mocker):
    """Test Config class init."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=[''])
    mocker.patch.object(configparser.ConfigParser, "has_section", return_value=True)
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    config = Config()
    assert config.source_dir == "tests/data"
    assert config.destination_dir == "tests/data"
    assert config.file_types == expected_config()["DEFAULT"]["file_types"]
    mocker.patch.object(Config, "validate", side_effect=configparser.Error("Configuration is invalid: "))
    with pytest.raises(configparser.Error):
        Config()

def test_config_validate(mocker):
    """Test Config class validate."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    mocker.patch("os.path.exists", return_value=True)
    err = argparse.ArgumentTypeError("Configuration is invalid:")
    mocker.patch("importphotos.validators.FileValidator.file_path", side_effect=err)
    with pytest.raises(configparser.Error):
        Config().validate()
    mocker.patch("importphotos.validators.FileValidator.file_path", side_effect=[None, err])
    with pytest.raises(configparser.Error):
        Config().validate()
    mocker.patch("importphotos.validators.FileValidator.file_path", side_effect=[None, None])
    mocker.patch("importphotos.validators.FileValidator.file_extension", side_effect=err)
    with pytest.raises(configparser.Error):
        Config().validate()

def test_config_get_config_item(mocker):
    """Test Config class _get_config_item."""
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    # No Section
    with pytest.raises(KeyError):
        config.get_config_item("group", "key")
    # No Option
    with pytest.raises(KeyError):
        config.get_config_item("DEFAULT", "key")
    mocker.patch.object(configparser.ConfigParser, "has_section", return_value=True)
    with pytest.raises(KeyError):
        config.get_config_item("group", "key")
    assert config.get_config_item("DEFAULT", "source_dir") == config.source_dir
    assert config.get_config_item("DEFAULT", "destination_dir") == config.destination_dir
    for item in config.get_config_item("DEFAULT", "file_types"):
        assert item.upper() in config.file_types

def test_config_read_config(mocker):
    """Test Config class _read_config."""
    file_input = r"""[DEFAULT]
source_dir = D:\DCIM\100MSDCF
destination_dir = C:\Users\thomasedward\Pictures\Camera Roll
file_types = .jpg .jpeg .png .cr2 .arw .mp4"""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", return_value=file_input)
    try:
        config = Config()
    except Exception as exc:
        pytest.fail(f"Config._read_config() rasied {exc}")

def test_config_write_config(mocker):
    """Test Config class _write_config."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=[''])
    mocker.patch.object(configparser.ConfigParser, "has_section", return_value=True)
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    
    config = Config()
    try:
        config._write_config()
    except Exception as exc:
        pytest.fail(f"Config._write_config() raised {exc}")

def test_config_str(mocker):
    """Test Config class str."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert str(config) == expected_config_str

def test_config_repr(mocker):
    """Test Config class repr."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch.object(Config, "get_config_item", side_effect=get_test_data_item)
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert repr(config) == expected_config_repr
