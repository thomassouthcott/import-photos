"""Unit Tests for importphotos.config module."""
import configparser

from importphotos.config import Config

def expected_config():
    return{
        "DEFAULT": {
            "source_dir": "tests/data",
            "destination_dir": "tests/data",
            "file_types": ".jpg, .jpeg, .arw",
        }
    }

expected_config_str = "source_dir=tests/data, destination_dir=tests/data, file_types=.jpg, .jpeg, .arw"
expected_config_repr = f"Config({expected_config_str})"

def test_config_init(mocker):
    """Test Config class init."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert config.source_dir == "tests/data"
    assert config.destination_dir == "tests/data"
    assert config.file_types == [".jpg", ".jpeg", ".arw"]

def test_config_save(mocker):
    """Test Config class save."""    
    mocker.patch.object(configparser.ConfigParser, "read", side_effect=[expected_config()])
    mocker.patch.object(configparser.ConfigParser, "write")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open")
    config = Config()
    config.save()
    assert config._config["DEFAULT"]["source_dir"] == "tests/data"
    assert config._config["DEFAULT"]["destination_dir"] == "tests/data"
    assert config._config["DEFAULT"]["file_types"] == ".jpg, .jpeg, .arw"

def test_config_validate(mocker):
    """Test Config class validate."""
    mocker.patch("importphotos.validators.FileValidator.file_path")
    mocker.patch("importphotos.validators.FileValidator.file_extension")
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    Config().validate()

def test_config_get_config_item(mocker):
    """Test Config class _get_config_item."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert config._get_config_item("DEFAULT", "source_dir") == config.source_dir
    assert config._get_config_item("DEFAULT", "destination_dir") == config.destination_dir
    assert config._get_config_item("DEFAULT", "file_types") == config.file_types

def test_config_set_config_item(mocker):
    """Test Config class _set_config_item."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    config._set_config_item("DEFAULT", "source_dir", "tests/new")
    assert config._config["DEFAULT"]["source_dir"] == "tests/new"

def test_config_read_config(mocker):
    """Test Config class _read_config."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert config._config == expected_config()

def test_config_write_config(mocker):
    """Test Config class _write_config."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open")
    config = Config()
    config._write_config(config._config)
    assert config._config == expected_config()

def test_config_str(mocker):
    """Test Config class str."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert str(config) == expected_config_str

def test_config_repr(mocker):
    """Test Config class repr."""
    mocker.patch.object(configparser.ConfigParser, "read", return_value=expected_config())
    mocker.patch("os.path.exists", return_value=True)
    config = Config()
    assert repr(config) == expected_config_repr
