"""Class for Photo Files."""
import datetime
import os

from PIL import Image, UnidentifiedImageError

class Photo(object):
    """Class for photos."""
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.path = path
        self.filename = os.path.basename(path)
        self.date_taken = self._get_date_taken()
        self.path = path

    def _get_date_taken(self):
        """Set the date taken."""
        """Get date taken from EXIF data or file modified date if not available."""
        date_taken = None
        try: 
            exif = Image.open(self.path).getexif()
            if not exif:
                raise UnidentifiedImageError(f'Image {self.path} does not have EXIF data.')
            #text = exif[36867]
            text = exif[306]
            date_taken = text
        except UnidentifiedImageError:
            alternatives = [".JPG", ".JPEG"]
            for alt in alternatives:
                file, extension = os.path.splitext(self.path)
                new_path = file + alt
                if os.path.exists(new_path) and not new_path == file + extension.upper():
                    return Photo(new_path).date_taken
            return datetime.datetime.fromtimestamp(os.path.getmtime(self.path))
        return datetime.datetime.fromisoformat(date_taken)

    def __str__(self):
        return f"{self.filename}"

    def __repr__(self):
        return f"Photo({self.filename}, {self.date_taken}, {self.path})"
