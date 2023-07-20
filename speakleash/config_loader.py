"""
ConfigLoader Module

This module provides the ConfigLoader class, a utility for loading configuration from a JSON file.

Classes:
- ConfigLoader: Utility class for loading configuration from a JSON file.

Dependencies:
- os: Provides functions for interacting with the operating system.
- json: Provides functions for working with JSON data.

"""
import os
import json


class ConfigLoader:
    """
    Utility class for loading configuration from a JSON file.
    """

    @staticmethod
    def load_config() -> dict:
        """
        Loads the configuration from the 'config.json' file.

        :return: The loaded configuration as a dictionary.
        :rtype: dict
        """
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as cfg_file:
            config = json.load(cfg_file)
        return config
