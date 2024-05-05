"""
Speakleash Module

This module provides the Speakleash class, the main entity object
responsible for managing and accessing datasets.

Classes:
- Speakleash: Represents the Speakleash class.

Dependencies:
- typing: Provides the List and Optional types for type hinting.
- speakleash.dataset: Provides the SpeakleashDataset class for dataset handling.
- speakleash.downloader: Provides the StructureDownloader class for downloading dataset structures.
- speakleash.config_loader: Provides the ConfigLoader class for loading configuration.
"""
import os
from typing import List, Optional

from speakleash.dataset import SpeakleashDataset
from speakleash.downloader import StructureDownloader
from speakleash.config_loader import ConfigLoader


class Speakleash:
    """
    Represents the Speakleash class, main entity object,
    responsible for managing and accessing datasets.
    """

    def __init__(self, replicate_dir: Optional[str] = None, lang: str = "pl"):
        """
        Initialize an instance of Speakleash class.

        :param replicate_dir: The directory to replicate the datasets.
        :param lang: The language for the Speakleash datasets (default is 'pl').
        """
        self.replicate_dir = self.destination_dir(replicate_dir)
        self.structure_file = self.get_structure_file(lang)
        self.url = self.get_url(lang)
        self.datasets = self.populate_datasets()

    @staticmethod
    def destination_dir(replicate_dir: str) -> str:
        """
        Returns the destination directory for datasets. If the 'replicate_dir' value is empty or not provided,
        it is set to 'datasets' by default.

        :param replicate_dir: The directory name where the dataset should be replicated.
        :return: The path to the destination directory.
        """
        if not replicate_dir:
            replicate_dir = 'datasets'
        base_dir = os.path.join(os.path.abspath(''))
        return os.path.join(base_dir, replicate_dir)

    @staticmethod
    def get_structure_file(lang: str) -> str:
        """
        Retrieves the structure file based on the specified language.
        DISCLAIMER: Croatian language is currently not supported.

        :param lang: The language code ('pl').
        :return: The name of the structure file corresponding to the language.
        """
        return "speakleash.json"

    @staticmethod
    def get_url(lang: str) -> str:
        """
        Retrieves the URL based on the provided language.
        DISCLAIMER: Croatian language is currently not supported.

        :param lang: The language code ('pl').
        :return: The URL corresponding to the provided language.
        """
        urls_config = ConfigLoader.load_config()
        return urls_config["url_datasets_text_pl"]

    def populate_datasets(self) -> Optional[List[SpeakleashDataset]]:
        """
        Populates the datasets list by fetching dataset names.

        :return: A list of SpeakleashDataset instances, or None if no names are fetched.
        """
        names = StructureDownloader(self.replicate_dir).get_structure(
            self.url + self.structure_file)
        if names:
            return [SpeakleashDataset(item["name"], self.url,
                                      self.replicate_dir) for item in names if
                    "name" in item]
        return None

    def get(self, name: str) -> Optional[SpeakleashDataset]:
        """
        Retrieves a dataset by its provided name.

        :param name: The name of the dataset.
        :return: The SpeakleashDataset instance corresponding to the given name,
        or None if not found.
        """
        if self.datasets:
            for dataset in self.datasets:
                if dataset.name == name:
                    return dataset
        return None
