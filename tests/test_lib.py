"""Unit Tests for importphotos.lib module."""
import datetime
import pytest

from importphotos.lib import Photo

def test_photo_init(mocker):
    """Test Photo class init."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        Photo("tests/data/IMG_20210101_000000.ARW")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    #mock all file system calls
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert photo.filename == "IMG_20210101_000000.ARW"
    assert photo.date_taken == taken
    assert photo.path == "tests/data/IMG_20210101_000000.ARW"

def test_photo_get_date_taken(mocker):
    """Test Photo class get_date_taken, exit data present."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    magic_mock = mocker.MagicMock()
    magic_mock.getexif.return_value = dict({306: "2021-01-01:00:00:00"})
    mocker.patch("PIL.Image.open", return_value=magic_mock)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert photo.date_taken == taken

def test_photo_get_date_taken_no_exif_alternative(mocker):
    """Test Photo class get_date_taken, no exif data, alternative file to read."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    bad_mock = mocker.MagicMock()
    bad_mock.getexif.return_value = None
    good_mock = mocker.MagicMock()
    good_mock.getexif.return_value = {306: "2021-01-01:00:00:00"}
    mocker.patch("PIL.Image.open", side_effect=[bad_mock, good_mock])
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert photo.date_taken == taken

def test_photo_get_date_taken_no_exif_no_alternative(mocker):
    """Test Photo class get_date_taken, no exif data, no alternative file to read."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", side_effect=[True, False, False])
    mock = mocker.MagicMock()
    mock.getexif.return_value = None
    mocker.patch("PIL.Image.open", return_value=mock)
    mocker.patch("os.path.getmtime", return_value=1609459200.0)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert photo.date_taken == taken

def test_photo_get_date_taken_no_exif_no_alternative_jpg(mocker):
    """Test Photo class get_date_taken, no exit, no alternative because it is a jpg."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", side_effect=[True, True, False])
    mock = mocker.MagicMock()
    mock.getexif.return_value = None
    mocker.patch("PIL.Image.open", return_value=mock)
    mocker.patch("os.path.getmtime", return_value=1609459200.0)
    photo = Photo("tests/data/IMG_20210101_000000.JPG")
    assert photo.date_taken == taken

def test_photo_str(mocker):
    """Test Photo class str."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    #mock all file system calls
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert str(photo) == "IMG_20210101_000000.ARW"

def test_photo_repr(mocker):
    """Test Photo class repr."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    #mock all file system calls
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert repr(photo) == "Photo(IMG_20210101_000000.ARW, 2021-01-01 00:00:00, tests/data/IMG_20210101_000000.ARW)"