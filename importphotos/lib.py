"""Class for Photo Files."""
import datetime
import os
import shutil

from PIL import Image, UnidentifiedImageError

from importphotos.helpers.cli import print_progress_bar, print_message

class Job():
    """Class for jobs of Photos."""
    def __init__(self, folder):
        if len(folder.photos) == 0:
            raise ValueError(f"Folder {folder.path} has no photos.")
        self._folder = folder
        self.result = None

    def add_photo(self, photo):
        """Add a photo to the job."""
        self._folder.add_photo(photo)

    def done(self):
        """Return the result of the job."""
        return self.result is not None

    def __str__(self) -> str:
        return f"Job({self._folder}, {self.result})"

    def __repr__(self) -> str:
        return f"Job({self._folder}, {self.result})"

class DeleteJob(Job):
    """Class for deleting photos."""
    def __init__(self, folder):
        super().__init__(folder)

    def execute(self, j, verbose=False):
        """Delete files, returns amount of deleted files"""
        print_message(f'[{j}] - Deleting {len(self._folder.photos)} files')
        print_progress_bar(0, len(self._folder.photos), prefix = 'Deleting:', suffix = f'Job {j}', length = 56)
        deleted_files = []
        errored_files = []
        for i, photo in enumerate(self._folder.photos):
            print_progress_bar(i + 1, len(self._folder.photos), prefix = 'Progress:', suffix = '', length=56)
            try:
                os.remove(photo.path)
                deleted_files.append(photo)
            except Exception as err:
                errored_files.append(photo)
                if verbose:
                    print(err)

        print_message(f"Deleted {len(deleted_files)} files")
        if verbose:
            print_message("Deleted files:")
            for file in deleted_files:
                print_message(f"{file}")
        print_message(f"Errored out on {len(errored_files)} files")
        if verbose:
            print_message("Errored files:")
            for file in errored_files:
                print_message(f"{file}")
        self.result = deleted_files, errored_files
        return self.result

    def __str__(self):
        return f"DeleteJob({self._folder}, {self.result})"

    def __repr__(self):
        return f"DeleteJob({self._folder}, {self.result})"

class ImportJob(Job):
    """Class for copying photos."""
    def __init__(self, folder, destination, overwrite=False):
        super().__init__(folder)
        try:
            os.makedirs(destination)
        except FileExistsError:
            pass
        self.destination_folder = destination
        self.overwrite = overwrite

    def execute(self, j, verbose=False):
        """Copy files does not overwrtite files, returns amount of copied files"""
        #Input validation
        if not os.path.exists(self.destination_folder):
            raise FileNotFoundError(f"Destination folder {self.destination_folder} does not exist.")

        print_message(f'[{j}][{os.path.basename(self.destination_folder)}] - Processing {len(self._folder.photos)} files, syncing with {self.destination_folder}')
        print_progress_bar(0, len(self._folder.photos), prefix = f'Syncing {os.path.basename(self.destination_folder)}:', suffix = f'Job {j}', length = 56)
        skipped_files = []
        copied_files = []
        errored_files = []
        for i, photo in enumerate(self._folder.photos):
            print_progress_bar(i + 1, len(self._folder.photos), prefix = 'Progress:', suffix = '', length=56)
            if os.path.exists(os.path.join(self.destination_folder, os.path.basename(photo.path))) and not self.overwrite:
                skipped_files.append(photo)
                continue
            try:
                shutil.copy(photo.path, self.destination_folder)
                copied_files.append(photo)
            except shutil.SameFileError:
                copied_files.append(photo)
            except shutil.Error as err:
                errored_files.append(photo)
                if verbose:
                    print(err)

        print_message(f"Copied {len(copied_files)} files to {os.path.basename(self.destination_folder)}")
        if verbose:
            print_message("Copied files:")
            for file in copied_files:
                print_message(f"{file} -> {self.destination_folder}")
        print_message(f"Skipped {len(skipped_files)} files with duplicates in {os.path.basename(self.destination_folder)}")
        if verbose:
            print_message("Skipped files:")
            for file in skipped_files:
                print_message(f"{file} == {self.destination_folder}")
        print_message(f"Errored out on {len(errored_files)} files")
        if verbose:
            print_message("Errored files:")
            for file in errored_files:
                print_message(f"{file}")
        self.result = copied_files, errored_files, skipped_files
        return self.result

    def sort_files_by_date(self, verbose = False):
        """Sort files by date taken and return a list of new ImportJobs."""
        jobs = dict()
        for photo in self._folder.photos:
            try:
                year_month = photo.date_taken.strftime('%Y-%m')
            except Exception as e:
                print(f"Faulted on {photo.path} file")
                raise e
            if verbose:
                print(f"Sorting {photo} into {os.path.join(self.destination_folder, year_month)}")
            if year_month not in jobs.keys():
                folder = Folder(self._folder.path)
                folder.add_photo(photo)
                jobs[year_month] = ImportJob(folder, os.path.join(self.destination_folder, year_month), self.overwrite)
            else:
                jobs[year_month].add_photo(photo)
        return jobs

    def __str__(self):
        return f"ImportJob({self._folder}, {self.destination_folder}, {self.overwrite}, {self.result})"

    def __repr__(self):
        return f"ImportJob({self._folder}, {self.destination_folder}, {self.overwrite}, {self.result})"

class Folder():
    """Class for folders of Photos."""
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Folder {path} does not exist.")
        self.path = path
        self.photos = []

    def add_photo(self, photo):
        """Add a photo to the folder."""
        self.photos.append(photo)

    def get_files_with_extension(self, extensions, recurse=False, verbose=False):
        """Get source files from folder and filter by extension.
            If recurse is True, search subfolders for files."""
        found_photos = []
        found_files = []
        for root, dirs, files in os.walk(self.path):
            found_photos.extend([Photo(os.path.join(root,k)) for k in files if k.upper().endswith(extensions)])
            found_files.extend([os.path.join(root,k) for k in files if not k.upper().endswith(extensions)])
            print_message(f"Found {len(files)} files in {root}")
            if verbose:
                print_message(f"{len(found_photos)} Selected from {root}")
                print_message(f"{len(dirs)} folders in {root}")
                for file in found_photos:
                    print_message(f"{file}")
                print_message(f"{len(found_files)} Not selected from {root}")
                for file in (file for file in found_files if file not in found_photos):
                    print_message(f"{file}")
            if not recurse:
                break
        print_message(f"Found {len(found_photos)} {extensions} total in {self.path}.")
        self.photos = found_photos
        return len(found_photos)

    def filter_by_date(self, start, end, verbose = False):
        """Filter files by date modified."""
        filtered_files = []
        for photo in self.photos:
            if photo.date_taken >= start and photo.date_taken <= end:
                filtered_files.append(photo)
            else:
                print(verbose)
                if verbose:
                    print_message(f"Not selected {photo}")
        if verbose:
            for photo in filtered_files:
                print_message(f"Selected {photo}")
        print_message(f"Selected {len(filtered_files)} files in date range.")
        if len(filtered_files) == 0:
            return filtered_files
        self.photos = filtered_files
        return self.photos

    def __str__(self):
        return f"Folder({self.path}, {len(self.photos)} photos)"

    def __repr__(self):
        return f"Folder({self.path}, {len(self.photos)} photos)"

class Photo():
    """Class for photos."""
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.path = path
        self.filename = os.path.basename(path)
        self.date_taken = self._get_date_taken()

    def _get_date_taken(self):
        """Get date taken from EXIF data or file modified date if not available."""
        date_taken = None
        try:
            exif = Image.open(self.path).getexif()
            print(exif)
            if not exif:
                raise UnidentifiedImageError(f'Image {self.path} does not have EXIF data.')
            #text = exif[36867]
            text = exif[306]
            date_taken = text.replace(":", "-", 2).replace(" ", ":", 1)
            return datetime.datetime.fromisoformat(date_taken)
        except UnidentifiedImageError:
            alternatives = [".JPG", ".JPEG"]
            for alt in alternatives:
                file, extension = os.path.splitext(self.path)
                new_path = file + alt
                if os.path.exists(new_path) and not new_path == file + extension.upper():
                    return Photo(new_path).date_taken
            return datetime.datetime.fromtimestamp(os.path.getmtime(self.path))

    def __str__(self):
        return f"{self.filename}"

    def __repr__(self):
        return f"Photo({self.filename}, {self.date_taken}, {self.path})"
