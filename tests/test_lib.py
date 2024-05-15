"""Unit Tests for importphotos.lib module."""
import datetime
import pytest
import shutil

from PIL import Image

from importphotos.lib import Job, DeleteJob, ImportJob, Folder, Photo

def test_job_init(mocker):
    """Test Job class init."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        Job(Folder("tests/data"))
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    with pytest.raises(ValueError):
        Job(folder)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    folder.add_photo(Photo("tests/data/IMG_20210101_000000.ARW"))
    job = Job(folder)

    assert job._folder == folder
    assert job.result == None

def test_job_add_photo(mocker):
    """Test Job class add_photo."""    
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)

    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    new_photo = Photo("tests/data/IMG_20210101_000001.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = Job(folder)
    job.add_photo(new_photo)
    assert job._folder.photos == [photo, new_photo]

def test_job_done(mocker):
    """Test Job class done."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = Job(folder)
    assert not job.done()
    job.result = "Done"
    assert job.done()

def test_job_str(mocker):
    """Test Job class str."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = Job(folder)
    assert str(job) == "Job(Folder(tests/data, 1 photos), None)"

def test_job_repr(mocker):
    """Test Job class repr."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = Job(folder)
    assert repr(job) == "Job(Folder(tests/data, 1 photos), None)"

def test_delete_job_init(mocker):
    """Test DeleteJob class init."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        DeleteJob(Folder("tests/data"))
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    with pytest.raises(ValueError):
        DeleteJob(folder)
    folder.add_photo(Photo("tests/data/IMG_20210101_000000.ARW"))
    job = DeleteJob(folder)

    assert job._folder == folder
    assert job.result == None

def test_delete_job_execute_delete(mocker, capsys):
    """Test DeleteJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.remove", return_value=None)
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = DeleteJob(folder)
    deleted, errored = job.execute(1)

    captured = capsys.readouterr()
    assert "Deleting 1 files" in captured.out
    assert "Deleted 1 files" in captured.out
    assert "Errored out on 0 files" in captured.out

def test_delete_job_execute_error(mocker, capsys):
    """Test DeleteJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.remove", side_effect=FileNotFoundError("Error"))
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = DeleteJob(folder)
    deleted, errored = job.execute(1)

    captured = capsys.readouterr()
    assert "Deleting 1 files" in captured.out
    assert "Deleted 0 files" in captured.out
    assert "Errored out on 1 files" in captured.out

def test_delete_job_execute_verbose(mocker, capsys):
    """Test DeleteJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.remove", side_effect=[None, FileNotFoundError("Error")])
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(photo)
    job = DeleteJob(folder)
    deleted, errored = job.execute(1, True)

    captured = capsys.readouterr()
    assert "Deleting 2 files" in captured.out
    assert "Deleted 1 files" in captured.out
    assert "Errored out on 1 files" in captured.out
    assert "Deleted files:" in captured.out
    assert "IMG_20210101_000000.ARW" in captured.out
    assert "Errored files:" in captured.out
    assert "IMG_20210101_000000.ARW" in captured.out

def test_delete_job_str(mocker):
    """Test DeleteJob class str."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = DeleteJob(folder)
    assert str(job) == "DeleteJob(Folder(tests/data, 1 photos), None)"

def test_delete_job_repr(mocker):
    """Test DeleteJob class repr."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = DeleteJob(folder)
    assert repr(job) == "DeleteJob(Folder(tests/data, 1 photos), None)"

def test_import_job_init(mocker):
    """Test ImportJob class init."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        ImportJob(Folder("tests/data"), "tests/destination", False)
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    with pytest.raises(ValueError):
        ImportJob(folder, "tests/destination", False)
    folder.add_photo(Photo("tests/data/IMG_20210101_000000.ARW"))
    job = ImportJob(folder, "tests/destination", False)

    assert job._folder == folder
    assert job.result == None
    assert job.destination_folder == "tests/destination"
    assert job.overwrite == False

def test_import_job_execute_no_path(mocker):
    """Test ImportJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        job.execute(1)

def test_import_job_execute_copy(mocker, capsys):
    """Test ImportJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("shutil.copy", side_effect=[None, shutil.SameFileError("Error")] )
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    second_photo = Photo("tests/data/IMG_20210102_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(second_photo)
    job = ImportJob(folder, "tests/destination", False)
    mocker.patch("os.path.exists", side_effect=[True, False, False])
    copied, errored, skipped = job.execute(1)

    captured = capsys.readouterr()
    assert "Processing 2 files, syncing with tests/destination" in captured.out
    assert "Copied 2 files to destination" in captured.out
    assert "Skipped 0 files with duplicates in destination" in captured.out
    assert "Errored out on 0 files" in captured.out

def test_import_job_execute_skip(mocker, capsys):
    """Test ImportJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("shutil.copy", return_value=None)
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    copied, errored, skipped = job.execute(1)

    captured = capsys.readouterr()
    assert "Processing 1 files, syncing with tests/destination" in captured.out
    assert "Copied 0 files to destination" in captured.out
    assert "Skipped 1 files with duplicates in destination" in captured.out
    assert "Errored out on 0 files" in captured.out

def test_import_job_execute_error(mocker, capsys):
    """Test ImportJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("shutil.copy", side_effect=shutil.Error("Error"))
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    mocker.patch("os.path.exists", side_effect=[True, False])
    copied, errored, skipped = job.execute(1)
    captured = capsys.readouterr()
    print(captured.out)
    assert "Processing 1 files, syncing with tests/destination" in captured.out
    assert "Copied 0 files to destination" in captured.out
    assert "Skipped 0 files with duplicates in destination" in captured.out
    assert "Errored out on 1 files" in captured.out

def test_import_job_execute_verbose(mocker, capsys):
    """Test ImportJob class execute."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("shutil.copy", side_effect=[None, shutil.Error("Error")])
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(photo)
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    mocker.patch("os.path.exists", side_effect=[True, False, True, False])
    copied, errored, skipped = job.execute(1, True)

    captured = capsys.readouterr()
    assert "Processing 3 files, syncing with tests/destination" in captured.out
    assert "Copied 1 files to destination" in captured.out
    assert "Skipped 1 files with duplicates in destination" in captured.out
    assert "Errored out on 1 files" in captured.out
    assert "Copied files:" in captured.out
    assert "IMG_20210101_000000.ARW -> tests/destination" in captured.out
    assert "Errored files:" in captured.out
    assert "IMG_20210101_000000.ARW" in captured.out
    assert "Skipped files:" in captured.out
    assert "IMG_20210101_000000.ARW == tests/destination" in captured.out

def test_import_job_sort_files_by_date_one_folder(mocker):
    """Test ImportJob class sort_files_by_date."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    second_taken = datetime.datetime.fromisoformat("2021-01-02:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", side_effect=[taken, second_taken])
    folder = Folder("tests\\data")
    photo = Photo("tests\\data\\IMG_20210101_000000.ARW")
    second_photo = Photo("tests\\data\\IMG_20210102_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(second_photo)
    job = ImportJob(folder, "tests\\destination", False)
    jobs = job.sort_files_by_date()
    actual = jobs['2021-01']
    assert actual._folder.photos == [photo, second_photo]
    assert actual._folder.path == "tests\\data"

def test_import_job_sort_files_by_date_two_folders(mocker):
    """Test ImportJob class sort_files_by_date."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    second_taken = datetime.datetime.fromisoformat("2021-02-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", side_effect=[taken, second_taken])
    folder = Folder("tests\\data")
    photo = Photo("tests\\data\\IMG_20210101_000000.ARW")
    second_photo = Photo("tests\\data\\IMG_20210201_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(second_photo)
    job = ImportJob(folder, "tests\\destination", False)
    jobs = job.sort_files_by_date()
    actual = jobs['2021-01']
    assert actual.destination_folder == "tests\\destination\\2021-01"
    assert actual._folder.photos == [photo]
    assert actual._folder.path == "tests\\data"
    assert actual.overwrite == job.overwrite
    actual = jobs['2021-02']
    assert actual.destination_folder == "tests\\destination\\2021-02"
    assert actual._folder.photos == [second_photo]
    assert actual._folder.path == "tests\\data"
    assert actual.overwrite == job.overwrite

def test_import_job_sort_files_by_date_exception(mocker):
    """Test ImportJob class sort_files_by_date."""
    mocker.patch("os.path.exists", return_value=True)
    mock = mocker.MagicMock()
    mock.strftime= mocker.MagicMock(side_effect=TypeError)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value=mock)
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    with pytest.raises(TypeError):
        job.sort_files_by_date()

def test_import_job_sort_files_by_date_verbose(mocker, capsys):
    """Test ImportJob class sort_files_by_date."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    second_taken = datetime.datetime.fromisoformat("2021-02-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", side_effect=[taken, second_taken])
    folder = Folder("tests\\data")
    photo = Photo("tests\\data\\IMG_20210101_000000.ARW")
    second_photo = Photo("tests\\data\\IMG_20210201_000000.ARW")
    folder.add_photo(photo)
    folder.add_photo(second_photo)
    job = ImportJob(folder, "tests\\destination", False)
    jobs = job.sort_files_by_date(True)
    captured = capsys.readouterr()
    assert "Sorting IMG_20210101_000000.ARW into tests\\destination\\2021-01" in captured.out
    assert "Sorting IMG_20210201_000000.ARW into tests\\destination\\2021-02" in captured.out

def test_import_job_str(mocker):
    """Test ImportJob class str."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    assert str(job) == "ImportJob(Folder(tests/data, 1 photos), tests/destination, False, None)"

def test_import_job_repr(mocker):
    """Test ImportJob class repr."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder = Folder("tests/data")
    folder.add_photo(photo)
    job = ImportJob(folder, "tests/destination", False)
    assert repr(job) == "ImportJob(Folder(tests/data, 1 photos), tests/destination, False, None)"

def test_folder_init(mocker):
    """Test Folder class init."""
    mocker.patch("os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        Folder("tests/data")
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    assert folder.path == "tests/data"
    assert folder.photos == []

def test_folder_add_photo(mocker):
    """Test Folder class add_photo."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    folder.add_photo(photo)
    assert folder.photos == [photo]

def test_folder_get_files_with_extension_no_recurse(mocker, capsys):
    """Test Folder class get_files_with_extension."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.walk", return_value=[("tests\\data", [], ["IMG_20210101_000000.ARW", "IMG_20210101_000001.JPG"])])
    folder = Folder("tests\\data")
    found_photos = folder.get_files_with_extension((".ARW"))
    assert found_photos == 1
    assert folder.photos[0].filename == "IMG_20210101_000000.ARW"
    captured = capsys.readouterr()
    assert "Found 2 files in tests\\data" in captured.out
    assert "Found 1 .ARW total in tests\\data" in captured.out
    folder = Folder("tests\\data")
    found_photos = folder.get_files_with_extension((".ARW"), False, True)
    captured = capsys.readouterr()
    assert found_photos == 1
    assert "1 Selected from tests\\data" in captured.out
    assert "0 folders in tests\\data" in captured.out
    assert "IMG_20210101_000000.ARW" in captured.out
    assert "1 Not selected from tests\\data" in captured.out
    assert "tests\\data\\IMG_20210101_000001.JPG" in captured.out

def test_folder_get_files_with_extension_recurse(mocker, capsys):
    """Test Folder class get_files_with_extension."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", return_value= taken)
    mocker.patch("os.walk", return_value=[
        ("tests\\data", ["dir"], ["IMG_20210101_000000.ARW", "IMG_20210101_000001.JPG"]),
        ("tests\\data\\dir", [], ["IMG_20210101_000002.ARW"])
    ])
    folder = Folder("tests\\data")
    found_photos = folder.get_files_with_extension((".ARW"), recurse=True)
    assert found_photos == 2
    assert folder.photos[0].filename == "IMG_20210101_000000.ARW"
    assert folder.photos[1].filename == "IMG_20210101_000002.ARW"

def test_folder_filter_by_date(mocker, capsys):
    """Test Folder class filter_by_date."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    second_taken = datetime.datetime.fromisoformat("2021-01-02:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("importphotos.lib.Photo._get_date_taken", side_effect=[taken, second_taken])
    folder = Folder("tests/data")
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    second_photo = Photo("tests/data/IMG_20210102_000000.ARW")
    folder.add_photo(photo)
    start = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    end = datetime.datetime.fromisoformat("2021-01-02:00:00:00")
    assert folder.filter_by_date(start, end) == [photo]
    start = datetime.datetime.fromisoformat("2021-01-02:00:00:00")
    end = datetime.datetime.fromisoformat("2021-01-03:00:00:00")
    assert not folder.filter_by_date(start, end)
    folder.add_photo(second_photo)
    assert folder.filter_by_date(start, end, True) == [second_photo]
    captured = capsys.readouterr()
    assert "Not selected IMG_20210101_000000.ARW" in captured.out
    assert "Selected IMG_20210102_000000.ARW" in captured.out

def test_folder_str(mocker):
    """Test Folder class str."""
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    assert str(folder) == "Folder(tests/data, 0 photos)"

def test_folder_repr(mocker):
    """Test Folder class repr."""
    mocker.patch("os.path.exists", return_value=True)
    folder = Folder("tests/data")
    assert repr(folder) == "Folder(tests/data, 0 photos)"

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
    magic_mock.getexif.return_value = dict({306: "2021:01:01 00:00:00"})
    mocker.patch("PIL.Image.open", return_value=magic_mock)
    photo = Photo("tests/data/IMG_20210101_000000.ARW")
    assert photo.date_taken == taken

def test_photo_get_date_taken_no_exif_alternative_exif(mocker):
    """Test Photo class get_date_taken, no exif data, alternative file to read."""
    taken = datetime.datetime.fromisoformat("2021-01-01:00:00:00")
    mocker.patch("os.path.exists", return_value=True)
    bad_mock = mocker.MagicMock()
    bad_mock.getexif.side_effect = Image.UnidentifiedImageError('')
    good_mock = mocker.MagicMock()
    good_mock.getexif.return_value = {306: "2021:01:01 00:00:00"}
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