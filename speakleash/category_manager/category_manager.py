import requests
import os
import tempfile

from speakleash.config_loader import ConfigLoader


class CategoryManager:

    def __init__(self):

        self.temp_dir = os.path.join(tempfile.gettempdir(), "speakleash")

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

        self.categories_pl = self.__categories("pl")
        self.categories_en = self.__categories("en")

    def __categories(self, lang="pl"):

        urls_config = ConfigLoader.load_config()

        if lang == "pl":
            url = urls_config["url_categories_pl"]

        if lang == "en":
            url = urls_config["url_categories_en"]

        if url:
            if os.path.exists(os.path.join(self.temp_dir, lang + "_categories.txt")):
                with open(os.path.join(self.temp_dir, lang + "_categories.txt"), 'r') as f:
                    categories = f.readlines()
                    categories = [line.strip() for line in categories]
                return categories

            try:
                data = ""
                r = requests.get(url)
                r.encoding = 'utf-8'
                if r.ok:
                    data = r.text
            except:
                pass

            categories = data.split("\n")

            with open(os.path.join(self.temp_dir, lang + "_categories.txt"), encoding="utf-8", mode='w') as f:
                for c in categories:
                    f.write(c + "\n")

        return categories

    def categories(self, lang="pl"):

        if lang == "pl":
            return self.categories_pl
        if lang == "en":
            return self.categories_en

        return []

    def __get_pl_category(self, name, lang):

        index = None

        if lang == "en":
            try:
                index = self.categories_en.index(name)
            except:
                pass

        if index is not None:
            return self.categories_pl[index]

        return None

    def check_category(self, meta, categories, cf, lang="pl"):

        if not meta:
            return False

        if len(categories) == 0:
            return False

        for category in categories:

            category_pl = None
            if lang != "pl":
                category_pl = self.__get_pl_category(category, lang)
            else:
                category_pl = category

            if category_pl:
                meta_categories = meta.get("category", {})
                for meta_category in meta_categories:
                    if meta_category.upper() == category_pl.upper():
                        if meta_categories[meta_category] >= cf:
                            return True

        return False
