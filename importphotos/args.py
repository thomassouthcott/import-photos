"""Argument parser for ImportPhotos.py"""
import argparse
import datetime

from importphotos.validators import FileValidator

class ArgumentParser(argparse.ArgumentParser):
    """Argument parser for ImportPhotos.py"""
    def __init__(self):
        super().__init__(
            prog='ImportPhotos.py',
            description='Sync photos from source folder to destination folder, examines EXIF data for date taken and sorts by year-month.',
            epilog='See config.ini for configuration options.')
        self.add_argument('foldername', default=None, type=str, nargs='?',
                            help='Name of the sub-folder to copy files to. If not provided, will sort by year-month.')
        self.add_argument('-r', '--recursive', action='store_true',
                            help='Recursively search for files in subfolders of source folder.')
        self.add_argument('-m', '--move', action='store_true',
                            help='Deletes source files after copying.')
        self.add_argument('-s' , '--date-search', nargs=2, metavar=('start-dtm', 'end-dtm'),
                            type=datetime.datetime.fromisoformat, help='Filter source files by start and end date. ISOformat - YYYY-MM-DD:HH:mm:ss')
        self.add_argument('-i', '--interactive', action='store_true', help='Interactive mode.')
        self.add_argument('-e', '--extension', type=FileValidator.file_extension, nargs='+',
                            help='File extension to search for in source folder.')
        self.add_argument('--version', action='version', version='Import Photos 1.1')
        self.add_argument('-p', '--path', type=FileValidator.file_path, help='Path to source folder.')
        self.add_argument('-o', '--destination', type=FileValidator.file_path, help='Path to destination folder.')
        self.add_argument('-d', '--dry-run', action='store_true', help='Dry run. Does not copy files.')
        self.add_argument('-w', '--overwrite', action='store_true', help='Overwrite files in destination folder.')
        self.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')