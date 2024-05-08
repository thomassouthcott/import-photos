"""Unit tests for the validators.py module."""
import argparse
import pytest

from importphotos.validators import FileValidator

def side_effect(arg):
    if arg == 1:
        return True
    else:
        return False

def test_file_extension():
    """Test file_extension validator."""
    assert FileValidator.file_extension(".jpg") == (".JPG",)
    assert FileValidator.file_extension(".jpg, .jpeg") == (".JPG", ".JPEG")
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_extension("jpg")
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_extension(".jpg, .jpeg, png")
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_extension(".jpg, .jpeg, .file_extension")

def test_file_path():
    """Test file_path validator."""
    #TODO: Mock os.path.exists
    assert FileValidator.file_path("tests/test_validators.py") == "tests/test_validators.py"
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_path("tests/test_validators.pyx")
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_path("tests/test_validators.py, tests/test_validators.pyx")