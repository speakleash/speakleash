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
from typing import List, Optional

from speakleash.dataset import SpeakleashDataset
from speakleash.downloader import StructureDownloader
from speakleash.config_loader import ConfigLoader

class Speakleash:
    """
    Represents the Speakleash class, main entity object,
    responsible for managing and accessing datasets.
    """

    def __init__(self, replicate_dir: str, lang: str = "pl"):
        """
        Initialize an instance of Speakleash class.

        :param replicate_dir: The directory to replicate the datasets.
        :param lang: The language for the Speakleash datasets (default is 'pl').
        """
        self.replicate_dir = replicate_dir
        self.lang = lang
        self.structure_file = self.get_structure_file()
        self.url = self.get_url()
        self.datasets = self.populate_datasets()
        self.config = ConfigLoader.load_config()


    def get_structure_file(self) -> str:
        """
        Retrieves the structure file based on the specified language.

        :param lang: The language code ('pl' or 'hr').
        :return: The name of the structure file corresponding to the language.
        """
        # if self.lang == 'hr':
        #     return "speakleash_hr.json"
        # return "speakleash.json"
        if self.lang == 'hr':
            return self.config["structure_files"]["hr"]
        return self.config["structure_files"]["pl"]

    def get_url(self) -> str:
        """
        Retrieves the URL based on the provided language.

        :param lang: The language code ('pl' or 'hr').
        :return: The URL corresponding to the provided language.
        """
        # if self.lang == 'hr':
        #     return self.config["url_datasets_text_hr"]
        # return self.config["url_datasets_text_pl"]
        if self.lang == 'hr':
            return self.config["urls"]["datasets"]["text_hr"]
        return self.config["urls"]["datasets"]["text_pl"]

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
