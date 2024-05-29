"""Config Parser for importphotos"""
import argparse
import configparser
import dataclasses
import inspect
import os
from importphotos.validators import FileValidator
import importphotos

# Configuration Constants
@dataclasses.dataclass
class Config:
    """Class to hold the configuration of the program"""
    _config: configparser.ConfigParser
    source_dir: str
    destination_dir: str
    file_types: list[str]

    def __init__(self):
        self._config = self._read_config()
        self.source_dir = self.get_config_item("DEFAULT", "source_dir")
        self.destination_dir = self.get_config_item("DEFAULT", "destination_dir")
        self.file_types = self.get_config_item("DEFAULT", "file_types")
        try:
            self.validate()
        except configparser.Error as exc:
            raise exc

    def validate(self):
        """Validates the configuration"""
        try:
            FileValidator.file_path(self.source_dir)
            FileValidator.file_path(self.destination_dir)
            self.file_types = FileValidator.file_extension(" ".join(self.file_types))
        except argparse.ArgumentTypeError as exc:
            raise configparser.Error(f"Configuration is invalid: {exc}") from exc

    def get_config_item(self, group, key):
        """Returns the value of the key in the group"""
        try:
            if not self._config.has_section(group) and group!="DEFAULT":
                raise KeyError(f"Group {group} not found")
            if group=="DEFAULT" and not self._config.has_option("", key):
                raise KeyError(f"Key {key} not found in group {group}")
            elif not self._config.has_option(group, key):
                raise KeyError(f"Key {key} not found in group {group}")
            if key.lower().endswith("s"):
                return tuple(self._config[group][key].split(" "))
            return self._config[group][key]
        except KeyError as exc:
            print(exc)
            raise KeyError(f"Key {key} not found in group {group}") from exc

    def _read_config(self, config_file = None):
        """Loads the config from the config file"""
        if config_file is None:
            config_file = os.path.join(os.path.dirname(inspect.getfile(importphotos)),"config.ini")
        config = configparser.ConfigParser()
        config.read(os.path.abspath(config_file))
        return config

    def _write_config(self, config_file = "config.ini"):
        """Saves the config to the config file"""
        self._config.write(os.path.abspath(config_file))

    def __str__(self):
        return f"source_dir={self.source_dir}, destination_dir={self.destination_dir}, file_types={", ".join(self.file_types)}"

    def __repr__(self):
        return f"Config(source_dir={self.source_dir}, destination_dir={self.destination_dir}, file_types={", ".join(self.file_types)})"