"""
Category Manager Module

This module provides the CategoryManager class designed for operations related to categories.
The class can fetch categories from files or URLs, update the categories, and check given categories
against provided meta-data.

Classes:
- CategoryManager: Manages category operations, fetching, and verification.

Dependencies:
- os: For handling file and directory operations.
- tempfile: To get the system's temporary directory.
- requests: For sending HTTP requests.
- typing: Provides List, Optional, Dict, and Union types for type hinting.
- speakleash.config_loader: Provides the ConfigLoader class for loading configurations.
"""

import os
import tempfile
from typing import List, Optional, Dict, Union
import requests

from speakleash.config_loader import ConfigLoader


class CategoryManager:
    """
    A manager class to handle categories operations including fetching, updating, and checking.
    """

    def __init__(self):
        """
        Initializes the CategoryManager with directories and categories.
        """
        self.temp_dir: str = os.path.join(tempfile.gettempdir(), "speakleash")
        self.create_dirs(self.temp_dir)
        self.categories_pl: List[str] = self.__get_categories_from_file_or_url("pl")
        self.categories_en: List[str] = self.__get_categories_from_file_or_url("en")

    @staticmethod
    def create_dirs(temp_dir: str) -> None:
        """
        Creates the specified directory if it does not exist.

        :param temp_dir: Directory path to be created.
        """
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)

    @staticmethod
    def get_url_from_config(lang: str) -> str:
        """
        Retrieves the category URL based on the given language.

        :param lang: Language code ('pl' or 'en').
        :return: The URL corresponding to the provided language.
        """
        urls_config = ConfigLoader.load_config()
        return urls_config[f'url_categories_{lang}']

    @staticmethod
    def get_categories_from_file(categories_file_path: str) -> List[str]:
        """
        Fetches categories from the specified file path.

        :param categories_file_path: Path to the categories file.
        :return: List of categories.
        """
        with open(categories_file_path, 'r', encoding='utf-8') as temp_file:
            return [line.strip() for line in temp_file.readlines()]

    @staticmethod
    def get_categories_from_url(url: str) -> List[str]:
        """
        Retrieves categories from the provided URL.

        :param url: The URL to fetch categories from.
        :return: List of categories.
        """
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            if response.ok:
                return response.text.split("\n")
        except requests.RequestException:
            pass

        return []

    @staticmethod
    def write_categories_to_file(categories_file_path: str, categories: List[str]) -> None:
        """
        Writes categories to the specified file path.

        :param categories_file_path: Path to the categories file.
        :param categories: List of categories to be written.
        """
        with open(categories_file_path, encoding="utf-8", mode='w') as categories_file:
            for category in categories:
                categories_file.write(category + "\n")

    def update_categories_dir(self, categories: str = 'pl') -> List[str]:
        """
        Updates the categories directory. (TODO: Functionality needs to be implemented)

        :param categories: Language code ('pl' or 'en') for the categories.
        :return: Updated list of categories.
        """
        pass

    def __get_categories_from_file_or_url(self, lang: str = "pl") -> List[str]:
        """
        Helper method to retrieve categories based on language.

        :param lang: Language code ('pl' or 'en').
        :return: List of categories.
        """
        url = self.get_url_from_config(lang)
        categories_file_path = os.path.join(self.temp_dir, f'{lang}_categories.txt')

        if os.path.exists(categories_file_path):
            return self.get_categories_from_file(categories_file_path)
        elif url:
            categories_from_url = self.get_categories_from_url(url)
            self.write_categories_to_file(categories_file_path, categories_from_url)
            return categories_from_url

        return []

    def categories(self, lang: str = "pl") -> List[str]:
        """
        Fetches categories based on the provided language.

        :param lang: Language code ('pl' or 'en').
        :return: List of categories.
        """
        lang_options = {
                'pl': self.categories_pl,
                'en': self.categories_en
        }
        return lang_options.get(lang.lower()) or []

    def __get_pl_category(self, category_name: str, lang: str) -> Optional[str]:
        """
        Retrieves the Polish category name corresponding to the given category in another language.

        :param category_name: Category name in the given language.
        :param lang: Language code (should be 'en' for this method).
        :return: Polish category name corresponding to the given name, or None if not found.
        """
        if lang == "en":
            try:
                index = self.categories_en.index(category_name)
                return self.categories_pl[index]
            except:
                pass
        return None

    def check_category(self, meta: Dict[str, Union[str, float]], categories: List[str], cf: float,
                       lang: str = "pl") -> bool:
        """
        Checks if the category matches the meta data.

        :param meta: Meta data containing category information.
        :param categories: List of categories to check.
        :param cf: Confidence factor for category matching.
        :param lang: Language code ('pl' or 'en').
        :return: True if a matching category is found, False otherwise.
        """
        if not meta or not categories:
            return False

        for category in categories:
            if lang != "pl":
                pl_category = self.__get_pl_category(category, lang)
            else:
                pl_category = category

            if pl_category:
                for meta_cat, confidence in meta.get("category", {}).items():
                    if meta_cat.upper() == pl_category.upper() and confidence >= cf:
                        return True

        return False
