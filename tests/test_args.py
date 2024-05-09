"""Unit Tests for importphotos.args module."""


import argparse
import datetime
import pytest

from importphotos.args import ArgumentParser

def test_init():
    """Test the initialization of the ArgumentParser class."""
    parser = ArgumentParser()
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.prog == 'ImportPhotos.py'
    assert parser.description == 'Sync photos from source folder to destination folder, examines EXIF data for date taken and sorts by year-month.'
    assert parser.epilog == 'See config.ini for configuration options.'

def test_recursive():
    """Test the recursive argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.recursive is False
    args = parser.parse_args(['-r'])
    assert args.recursive is True

def test_move():
    """Test the move argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.move is False
    args = parser.parse_args(['-m'])
    assert args.move is True

def test_interactive():
    """Test the interactive argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.interactive is False
    args = parser.parse_args(['-i'])
    assert args.interactive is True

def test_dry_run():
    """Test the dry_run argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.dry_run is False
    args = parser.parse_args(['-d'])
    assert args.dry_run is True

def test_overwrite():
    """Test the overwrite argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.overwrite is False
    args = parser.parse_args(['-w'])
    assert args.overwrite is True

def test_verbose():
    """Test the verbose argument."""
    parser = ArgumentParser()
    args = parser.parse_args('')
    assert args.verbose is False
    args = parser.parse_args(['-v'])
    assert args.verbose is True

def test_foldername():
    """Test the foldername argument."""
    parser = ArgumentParser()
    args = parser.parse_args()
    assert args.foldername is None
    args = parser.parse_args(['foldername'])
    assert args.foldername == 'foldername'

def test_date_search():
    """Test the date_search arguments."""
    parser = ArgumentParser()
    args = parser.parse_args(['-s', '2021-01-01:00:00:00', '2021-12-31:23:59:59'])
    assert args.date_search == [
        datetime.datetime.fromisoformat('2021-01-01:00:00:00'),
        datetime.datetime.fromisoformat('2021-12-31:23:59:59')
    ]
    with pytest.raises(SystemExit):
        args = parser.parse_args(['-s', '2021-12-31:23:59:59', '2021-12-32:23:59:59'])

def test_extension(mocker):
    """Test the extension arguments."""
    mocker.patch('importphotos.validators.FileValidator.file_extension', return_value=True)
    parser = ArgumentParser()
    args = parser.parse_args(['-e', '.jpg'])
    assert args.extension

def test_version():
    """Test the version argument."""
    parser = ArgumentParser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--version'])

def test_path(mocker):
    """Test the source path argument."""
    mocker.patch('importphotos.validators.FileValidator.file_path', return_value=True)
    parser = ArgumentParser()
    args = parser.parse_args(['-p', 'tests/test_args.py'])
    assert args.path

def test_destination(mocker):
    """Test the destination argument."""
    mocker.patch('importphotos.validators.FileValidator.file_path', return_value=True)
    parser = ArgumentParser()
    args = parser.parse_args(['-o', 'tests/test_args.py'])
    assert args.destination
