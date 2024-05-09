"""Config Parser for importphotos"""
import argparse
import configparser
import dataclasses

from importphotos.validators import FileValidator

# Configuration Constants
@dataclasses.dataclass
class Config:
    """Class to hold the configuration of the program"""
    _config: configparser.ConfigParser
    source_dir: str
    destination_dir: str
    file_types: list

    def __init__(self):
        self._config = self._read_config()
        self.source_dir = self._get_config_item("DEFAULT", "source_dir")
        self.destination_dir = self._get_config_item("DEFAULT", "destination_dir")
        self.file_types = self._get_config_item("DEFAULT", "file_types")
        try:
            self.validate()
        except configparser.Error as exc:
            raise exc

    def save(self):
        """Saves the configuration to the config file"""
        self._set_config_item("DEFAULT", "source_dir", self.source_dir)
        self._set_config_item("DEFAULT", "destination_dir", self.destination_dir)
        self._set_config_item("DEFAULT", "file_types", self.file_types)
        self._write_config(self._config)

    def validate(self):
        """Validates the configuration"""
        try:
            FileValidator.file_path(self.source_dir)
            FileValidator.file_path(self.destination_dir)
            for file_type in self.file_types:
                FileValidator.file_extension(file_type)
        except argparse.ArgumentTypeError as exc:
            raise configparser.Error(f"Configuration is invalid: {exc}") from exc

    def _get_config_item(self, group, key):
        """Returns the value of the key in the group"""
        try:
            if key.endswith("s"):
                return self._config[group][key].split(", ")
            else:
                return self._config[group][key]
        except KeyError as exc:
            raise KeyError(f"Key {key} not found in group {group}") from exc

    def _set_config_item(self, group, key, value):
        """Sets the value of the key in the group"""
        try:
            if key.endswith("s"):
                self._config[group][key] = ", ".join(value)
            else:
                self._config[group][key] = value
        except KeyError as exc:
            raise KeyError(f"Key {key} not found in group {group}") from exc

    def _read_config(self, config_file = "config.ini"):
        """Loads the config from the config file"""
        config = configparser.ConfigParser()
        return config.read(config_file)

    def _write_config(self, config_file = "config.ini"):
        """Saves the config to the config file"""        
        config = configparser.ConfigParser()
        config.read_dict(self._config)
        with open(config_file, "w", encoding='utf-8') as file:
            config.write(file)

    def __str__(self):
        return f"source_dir={self.source_dir}, destination_dir={self.destination_dir}, file_types={", ".join(self.file_types)}"

    def __repr__(self):
        return f"Config(source_dir={self.source_dir}, destination_dir={self.destination_dir}, file_types={", ".join(self.file_types)})"