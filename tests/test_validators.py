"""Unit tests for the validators.py module."""
import argparse
import pytest

from importphotos.validators import FileValidator

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

def test_file_path(mocker):
    """Test file_path validator."""
    mocker.patch("os.path.exists", side_effect=[True, False, False])
    assert FileValidator.file_path("tests/test_validators.py") == "tests/test_validators.py"
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_path("tests/test_validators.py")
    with pytest.raises(argparse.ArgumentTypeError):
        FileValidator.file_path("tests/test_validators.py, tests/test_validators.pyx")