"""
StructureDownloader Module

This module provides the StructureDownloader class, an entity responsible for
downloading and managing dataset structures.

Classes:
- StructureDownloader: Represents the StructureDownloader class.

Dependencies:
- hashlib: Provides the algorithm for generating a hash from a URL.
- json: Provides methods for working with JSON data.
- os: Provides a way of using operating system dependent functionality.
- datetime: Provides classes for manipulating dates and times.
- glob: Provides a function for creating lists of file paths matching a pathname pattern.
- typing: Provides the Optional and Dict types for type hinting.
- requests: Provides methods for sending HTTP requests.

"""
import hashlib
import json
import os
from datetime import datetime
import glob
from typing import Optional, Dict

import requests


class StructureDownloader:
    """
    Represents the StructureDownloader class, an entity responsible for
    downloading and managing dataset structures.
    """

    def __init__(self, replicate_dir: str):
        """
        Initialize an instance of the StructureDownloader class.

        :param replicate_dir: The directory where the dataset structures are replicated.
        """
        self.replicate_dir = replicate_dir
        self.data: Optional[Dict] = None

    @staticmethod
    def generate_hash(url: str) -> str:
        """
        Generates a hash from a URL.

        :param url: The URL to be hashed.
        :return: The hash of the URL.
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    @staticmethod
    def get_timestamp(hourly: bool = True) -> str:
        """
        Generates a timestamp.

        :param hourly: If True, the timestamp will include the current hour.
        Otherwise, it will only include the date. Defaults to True.
        :return: The timestamp.
        """
        now = datetime.now()
        if hourly:
            return now.strftime("-%m_%d_%y_%H")
        return now.strftime("-%m_%d_%y")

    def _remove_old_files(self, url: str) -> None:
        """
        Removes old files that match the hash of the URL.

        :param url: The URL for generating the hash.
        """
        url_hash = self.generate_hash(url)
        absolute_file_path = os.path.join(self.replicate_dir, f"{url_hash}-*.json")
        files = glob.glob(absolute_file_path)

        for file in files:
            try:
                os.remove(file)
            except:
                pass

    def get_data_from_file(self, file: str) -> None:
        """
        Loads data from a file.

        :param file: The file path.
        """
        try:
            with open(file, 'r', encoding='utf-8') as data_file:
                self.data = json.load(data_file)
        except:
            pass

    def get_data_from_url(self, url: str) -> None:
        """
        Downloads data from a URL.

        :param url: The URL.
        """
        try:
            response = requests.get(url)
            if response.ok:
                self.data = json.loads(response.text)
        except:
            pass

    @staticmethod
    def write_data_to_file(data: Dict, file: str) -> None:
        """
        Writes data to a file.

        :param data: The data to be written.
        :param file: The path of the file.
        """
        try:
            with open(file, 'w', encoding='utf-8') as data_file:
                json.dump(data, data_file)
        except:
            pass

    def get_structure(self, url: str, hourly: bool = True) -> Dict:
        """
        Retrieves the dataset structure. If the structure already exists in a file,
        it is loaded from there. Otherwise, it is downloaded from the URL.

        :param url: The URL for downloading the dataset structure.
        :param hourly: If True, the timestamp will include the current hour.
        Otherwise, it will only include the date. Defaults to True.
        :return: The dataset structure.
        """
        timestamp = self.get_timestamp(hourly)
        url_hash = self.generate_hash(url)
        file = os.path.join(self.replicate_dir, f"{url_hash}{timestamp}.json")

        if os.path.exists(file):
            self.get_data_from_file(file)
        else:
            self._remove_old_files(url)
            self.get_data_from_url(url)
            self.write_data_to_file(self.data, file)
        return self.data
