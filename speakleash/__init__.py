import requests
import json
from tqdm import tqdm
import os
from lm_dataformat import Reader

class Speakleash(object):

    def __init__(self, replicate_dir):
        self.replicate_dir = replicate_dir
        self.datasets = []
        self.datasets.append(SpeakleashDataset("thesis", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("plwiki", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("1000_novels_corpus_CLARIN-PL", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("wolne_lektury_corpus", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("project_gutenberg_pl_corpus", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("open_subtitles_corpus", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("biblioteka_nauki_pl_corpus", "https://zazepa.pl/speakleash/", self.replicate_dir))
        self.datasets.append(SpeakleashDataset("saos", "https://zazepa.pl/speakleash/", self.replicate_dir))
    def get(self, name):
        for d in self.datasets:
            if d.name == name:
                return d
        return None

class SpeakleashDataset(object):

    def __init__(self, name, url, replicate_dir):
        self.url = url
        self.name = name
        self.replicate_dir = replicate_dir
        self.manifest = self._download_manifest()

    def _download_file(self, file_name):

        ok = True
        url = self.url + self.name + ".jsonl.zst"
        file_path = os.path.join(self.replicate_dir, file_name)

        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            ok = False

        return ok

    def _download_manifest(self):

        try:
            r = requests.get(self.url + self.name + ".manifest")
            if r.ok:
                return json.loads(r.text)
        except:
            print("Error downloading manifest {0}".format(self.url + self.name + ".manifest"))
            return{}
                
        return {}

    @property
    def characters(self):
        s = self.manifest.get("stats",{}).get("characters",0)
        return s

    @property
    def documents(self):
        s = self.manifest.get("stats",{}).get("documents",0)
        return s

    @property
    def nouns(self):
        return self.manifest.get("stats",{}).get("nouns",[])

    @property
    def verbs(self):
        return self.manifest.get("stats",{}).get("verbs",[])

    @property
    def symbols(self):
        return self.manifest.get("stats",{}).get("symbols",[])

    @property
    def punctuations(self):
        return self.manifest.get("stats",{}).get("punctuations",[])

    @property
    def sentences(self):
        return self.manifest.get("stats",{}).get("sentences",[])

    @property
    def words(self):
        return self.manifest.get("stats",{}).get("words",[])

    @property
    def description(self):
        return self.manifest.get("description","")

    @property
    def license(self):
        return self.manifest.get("license","")

    @property
    def category(self):
        return self.manifest.get("category","")

    @property
    def sources (self):
        return self.manifest.get("sources",{})


    @property
    def jsonl_zst_file_size(self):
        return self.manifest.get("file_size",0)


    def check_file(self):

        if not os.path.exists(self.replicate_dir):
            os.makedirs(self.replicate_dir, exist_ok=True)

        file_name_json_zst = os.path.join(self.name + ".jsonl.zst")
        file_path_json_zst = os.path.join(self.replicate_dir, file_name_json_zst)
        file_json_zst_exists = False

        if os.path.exists(file_path_json_zst):
            file_size = os.path.getsize(file_path_json_zst)
            if file_size == self.jsonl_zst_file_size:
                file_json_zst_exists = True

        if not file_json_zst_exists:
            if not self._download_file(file_name_json_zst):
                return False, ""

        return True, file_path_json_zst


    @property
    def ext_data(self):

        ok, file_path_json_zst = self.check_file()
        if not ok:
            return None

        rdr = Reader(file_path_json_zst)
        return rdr.stream_data(get_meta=True)

    @property
    def data(self):

        ok, file_path_json_zst = self.check_file()
        if not ok:
            return None

        rdr = Reader(file_path_json_zst)
        return rdr.stream_data()

    def __repr__(self):
        return "SpeakleashDataset([{0},{1},{2}])".format(self.name, self.url, self.characters)

    def __str__(self):
        return "name: {0}, url: {1}, characters: {2}".format(self.name, self.url, self.characters)
    
