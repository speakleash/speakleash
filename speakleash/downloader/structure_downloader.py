import requests
import json
import os
import hashlib
from datetime import datetime
import glob


class StructureDownloader:

    def __init__(self, replicate_dir):
        self.replicate_dir = replicate_dir

    def _remove_old_files(self, url):

        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filter = os.path.join(self.replicate_dir, hash + "-*.json")
        files = glob.glob(filter)
        for f in files:
            try:
                os.remove(f)
            except:
                pass

        return

    def get_structure(self, url, hourly=True):

        now = datetime.now()
        data = None

        if hourly:
            ts = now.strftime("-%m_%d_%y_%H")
        else:
            ts = now.strftime("-%m_%d_%y")

        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        file = os.path.join(self.replicate_dir, hash + ts + ".json")

        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                return data
            except:
                pass

        self._remove_old_files(url)

        try:
            r = requests.get(url)
            if r.ok:
                data = json.loads(r.text)
        except:
            pass

        try:
            with open(file, 'w') as f:
                json.dump(data, f)
        except:
            pass

        return data
