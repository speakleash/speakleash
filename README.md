# SpeakLeash

SpeakLeash agnostic dataset for Polish

## Basic Usage

If you just want to see the details of the datasets

```
from speakleash import Speakleash
import os

base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)

for d in sl.datasets:
    print(d.name)
    for doc in d.data:
        size_mb = round(d.characters/1024/1024)
        print("Dataset: {0}, size: {1} MB, characters: {2}, documents: {3}".format(d.name, size_mb, d.characters, d.documents))

```

You can use individual properties (e.g.:***characters***, ***documents***), but you can display the entire manifest
```
sl = Speakleash(replicate_to)
print(sl.get("plwiki").manifest)

```

If you chose one of them (***.get(name of dataset)***) then you will get a lot of text data ;-)
```
from speakleash import Speakleash
import os

base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)

wiki = sl.get("plwiki").data
for doc in wiki:
    print(doc[:40])

```

If you also need meta data then use the ***ext_data*** property
```

ds = sl.get("plwiki").ext_data
for doc in ds:
    print(doc)
    txt, meta = doc
    print(meta.get("title"))
    print(txt)


```

Popular meta data:

* title
* length
* sentences
* words
* verbs
* nouns
* symbols
* punctuations


## Supported languages

On June 9, 2023, Croatia joined our projects. If you want to use Croatian language datasets just add lang parameter when creating Speakleash object.

```
from speakleash import Speakleash
import os

base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to, "hr")

for d in sl.datasets:
    print(d.name)
    for doc in d.data:
        size_mb = round(d.characters/1024/1024)
        print("Dataset: {0}, size: {1} MB, characters: {2}, documents: {3}".format(d.name, size_mb, d.characters, d.documents))

```