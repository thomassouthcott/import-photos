"""Custom validators for argparse."""
import argparse
import os
import re

class FileValidator:
    """Validators for File inputs."""
    @staticmethod
    def file_extension(arg_value, pat=re.compile(r"^\.[a-zA-Z0-9]{3,4}$")):
        """Check if argument is a valid file extension."""
        arg_value = arg_value.replace(",", " ")
        extensions = tuple(f.upper() for f in arg_value.split(" ") if f != "")
        for ext in extensions:
            if not pat.match(ext):
                raise argparse.ArgumentTypeError(f"{ext} must be a valid file extension. Example: '.jpg'")
        return extensions

    @staticmethod
    def file_path(arg_value):
        """Check if argument is a valid file path."""
        if not os.path.exists(arg_value):
            raise argparse.ArgumentTypeError(f"file path {arg_value} does not exist.")
        return arg_value
