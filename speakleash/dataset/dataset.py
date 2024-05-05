"""
Speakleash Dataset Module

This module provides the SpeakleashDataset class which is responsible for
managing individual datasets, downloading them, and accessing various properties.

Dependencies:
- os: Provides a way of using operating system dependent functionality.
- lm_dataformat: Provides a reader for the data format.
- requests: Allows sending HTTP requests.
- tqdm: Instantly makes loops show a smart progress meter.
- typing: Provides the Dict, Tuple, List and Union types for type hinting.
- speakleash.downloader: Provides the StructureDownloader class for downloading dataset structures.
"""
import os
from typing import Any, Dict, Generator, List, Optional, Tuple

from lm_dataformat import Reader
import requests
from tqdm import tqdm

from speakleash.downloader import StructureDownloader


class SpeakleashDataset:
    """
    Represents a dataset in the Speakleash system.

    This class allows for the downloading of datasets, access to its various
    properties, and extraction of samples from the dataset.

    Attributes:
    - name (str): The name of the dataset.
    - url (str): The base URL for fetching the dataset and manifest.
    - replicate_dir (str): Directory path to replicate the datasets.
    """

    BLOCK_SIZE = 1024

    def __init__(self, name: str, url: str, replicate_dir: str) -> None:
        """
        Initializes the SpeakleashDataset instance.

        :param name: The name of the dataset.
        :param url: The base URL for fetching the dataset.
        :param replicate_dir: Directory path to replicate the datasets.
        """
        self.name = name
        self.url = url
        self.replicate_dir = replicate_dir
        self.manifest = self._download_manifest()

    def _download_file(self, file_name: str) -> bool:
        """
        Downloads a specified file from the Speakleash dataset URL.

        :param file_name: The name of the file to download.
        :return: True if download is successful, False otherwise.
        """
        url = f"{self.url}{self.name}.jsonl.zst"
        file_path = os.path.join(self.replicate_dir, file_name)
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('Content-Length', 0))

        with open(file_path, 'wb') as file:
            progress_bar = self.display_progress_bar(response, file, total_size_in_bytes)

        return self._download_complete(total_size_in_bytes, progress_bar.n)

    @staticmethod
    def _download_complete(size: int, progress: int) -> bool:
        """
        Checks if the download is complete based on size and progress.

        :param size: The total size of the content to be downloaded.
        :param progress: The current size that has been downloaded.
        :return: True if the download is complete, otherwise False.
        """
        if size != 0 and progress != size:
            return False
        return True

    def display_progress_bar(self, response: requests.Response, file: Any, total_size_in_bytes: int) -> tqdm:
        """
        Displays a progress bar for file downloads.

        :param response: The HTTP response object.
        :param file: The file object to write to.
        :param total_size_in_bytes: Total size of the file in bytes.
        :return: The progress bar object.
        """
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        for data in response.iter_content(self.BLOCK_SIZE):
            progress_bar.update(len(data))
            file.write(data)

        progress_bar.close()
        return progress_bar

    def _download_manifest(self) -> dict:
        """
        Downloads the manifest file for the dataset.

        :return: A dictionary containing the manifest data or an empty dictionary on failure.
        """
        structure_url = f"{self.url}{self.name}.manifest"
        data = StructureDownloader(self.replicate_dir).get_structure(structure_url)

        if data:
            return data
        print(f"Error downloading manifest {self.url}{self.name}.manifest")

        return {}

    @property
    def characters(self) -> int:
        """
        Retrieves the number of characters from the dataset manifest.

        :return: The number of characters in the dataset or 0 if not present.
        """
        return self.manifest.get("stats", {}).get("characters", 0)

    @property
    def quality_metrics(self) -> str:
        """
        Determines the quality metric level of the dataset based on the presence
        of HIGH, MEDIUM, or LOW metrics.

        :return: A string indicating the quality metric level ("HIGH", "MEDIUM", "LOW")
        or an empty string if none is found.
        """
        quality = self.manifest.get("stats", {}).get("quality", {})
        for key in ["HIGH", "MEDIUM", "LOW"]:
            if quality.get(key, 0) != 0:
                return key
        return ""

    @property
    def categorization(self) -> bool:
        """
        Checks if any category in the dataset manifest exceeds 95%.

        :return: True if any category exceeds 95%, otherwise False.
        """
        categories = self.manifest.get("category=95%", {})
        for value in categories.values():
            if value > 0:
                return True
        return False

    @property
    def categories(self) -> Dict[str, int]:
        """
        Retrieves categories and their respective percentages from
        the dataset manifest.

        :return: A dictionary of categories with their respective percentages,
        or an empty dictionary if not present.
        """
        return self.manifest.get("category=95%", {})

    @property
    def quality(self) -> Dict[str, float]:
        """
        Retrieves quality metrics from the dataset manifest.

        :return: A dictionary of quality metrics, or an empty dictionary if not present.
        """
        return self.manifest.get("stats", {}).get("quality", {})

    @property
    def documents(self) -> int:
        """
        Retrieves the number of documents from the dataset manifest.

        :return: The number of documents, or 0 if not present.
        """
        return self.manifest.get("stats", {}).get("documents", 0)

    @property
    def stopwords(self) -> int:
        """
        Retrieves the number of stopwords from the dataset manifest.

        :return: The number of stopwords, or 0 if not present.
        """
        return self.manifest.get("stats", {}).get("stopwords", 0)

    @property
    def nouns(self) -> List[str]:
        """
        Retrieves a list of nouns from the dataset manifest.

        :return: A list of nouns, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("nouns", [])

    @property
    def verbs(self) -> List[str]:
        """
        Retrieves a list of verbs from the dataset manifest.

        :return: A list of verbs, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("verbs", [])

    @property
    def symbols(self) -> List[str]:
        """
        Retrieves a list of symbols from the dataset manifest.

        :return: A list of symbols, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("symbols", [])

    @property
    def punctuations(self) -> List[str]:
        """
        Retrieves a list of punctuations from the dataset manifest.

        :return: A list of punctuations, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("punctuations", [])

    @property
    def sentences(self) -> List[str]:
        """
        Retrieves a list of sentences from the dataset manifest.

        :return: A list of sentences, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("sentences", [])

    @property
    def words(self) -> List[str]:
        """
        Retrieves a list of words from the dataset manifest.

        :return: A list of words, or an empty list if not present.
        """
        return self.manifest.get("stats", {}).get("words", [])

    @property
    def description(self) -> str:
        """
        Retrieves the description of the dataset from the manifest.

        :return: The dataset's description, or an empty string if not present.
        """
        return self.manifest.get("description", "")

    @property
    def license(self) -> str:
        """
        Retrieves the license information of the dataset from the manifest.

        :return: The dataset's license information, or an empty string if not present.
        """
        return self.manifest.get("license", "")

    @property
    def category(self) -> str:
        """
        Retrieves the primary category of the dataset from the manifest.

        :return: The dataset's primary category, or an empty string if not present.
        """
        return self.manifest.get("category", "")

    @property
    def sources(self) -> List[Dict[str, str]]:
        """
        Retrieves the sources from which the dataset was derived from the manifest.

        :return: A list of sources, or an empty list if not present.
        """
        return self.manifest.get("sources", {})

    @property
    def jsonl_zst_file_size(self) -> int:
        """
        Retrieves the file size of the dataset in JSONL.ZST format from the manifest.

        :return: The file size of the dataset in JSONL.ZST format, or 0 if not present.
        """
        return self.manifest.get("file_size", 0)

    def check_file(self) -> Tuple[bool, str]:
        """
        Checks the existence and integrity of the dataset file by following these steps:

        1. If the specified directory does not exist, create it. No error is returned if the
           directory already exists.
        2. Generate the file's name with the ".json.zst" extension.
        3. Construct the absolute path for the file.
        4. Check if the file exists and if its size matches the size provided in the manifest.
            - If both conditions are met, return True along with the path to the existing file.
        5. If the file does not exist or its size doesn't match the expected value, attempt to
           download it.
            - If the download fails, return False and an empty string.
        6. After a successful download, return True and the path to the downloaded file.

        :return: A tuple containing a boolean indicating the success of the operation,
                 and the path to the file (if successful) or an empty string.
        """
        if not os.path.exists(self.replicate_dir):
            os.makedirs(self.replicate_dir, exist_ok=True)

        file_name_json_zst = f'{self.name}.jsonl.zst'
        file_path_json_zst = os.path.join(self.replicate_dir, file_name_json_zst)

        if os.path.exists(file_path_json_zst) and \
                (os.path.getsize(file_path_json_zst) == self.jsonl_zst_file_size):
            return True, file_path_json_zst

        if not self._download_file(file_name_json_zst):
            return False, ""

        return True, file_path_json_zst

    @property
    def samples(self) -> List[str]:
        """
        Retrieves samples from the dataset.

        :return: A list of samples from the dataset.
        """
        sample_url = f"{self.url}{self.name}.sample"
        return StructureDownloader(self.replicate_dir).get_structure(sample_url, False) or []

    @property
    def ext_data(self) -> Optional[Generator[str, None, None]]:
        """
        Extracts extended data from the dataset file.

        :return: A generator containing the streamed data with metadata, or None if the file check fails.
        """
        file_valid, file_path_json_zst = self.check_file()

        if not file_valid:
            return None

        return Reader(file_path_json_zst).stream_data(get_meta=True)

    @property
    def data(self) -> Optional[Generator[str, None, None]]:
        """
        Extracts data from the dataset file.

        :return: A generator containing the streamed data, or None if the file check fails.
        """
        file_valid, file_path_json_zst = self.check_file()

        if not file_valid:
            return None

        return Reader(file_path_json_zst).stream_data()

    def __repr__(self):
        return f"SpeakleashDataset([{self.name},{self.url},{self.characters}])"

    def __str__(self):
        return f"name: {self.name}, url: {self.url}, characters: {self.characters}"
