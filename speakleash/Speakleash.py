from SpeakleashDataset import SpeakleashDataset

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
    def get(self, name):
        for d in self.datasets:
            if d.name == name:
                return d
        return None