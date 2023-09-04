<h1 align="center">
<img src="https://speakleash.org/wp-content/uploads/2023/03/SpeakLeash_logo-2-1980x382.png" width="300">
</h1><br>

<p align="center">
    <a href="https://pypi.org/project/speakleash">
        <img src="https://badge.fury.io/py/speakleash.svg">
    </a>
    <a href="https://speakleash.org/">
        <img src="https://img.shields.io/badge/organisation-Speakleash-orange">
    </a>
    <a href="https://pypi.org/project/speakleash">
        <img src="https://img.shields.io/badge/python-_>=_3.6-blue">
    </a>
    <a href="https://speakleash.org/dashboard/">
        <img src="https://img.shields.io/badge/datasets-367_GB-brightgreen">
    </a>
    <a href="https://discord.com/invite/35cSny6Q?utm_source=Discord%20Widget&utm_medium=Connect">
        <img src="https://img.shields.io/discord/1043112910278381619?logo=discord&label=discord&color=%23603FEF">
    </a>
</p>

[SpeakLeash](href="https://pypi.org/project/speakleash) is a lightweight library providing datasets for the Polish language
and tools to make them useful.

- **Website:** https://speakleash.org/
- **Source code:** https://github.com/speakleash/speakleash
- **Bug reports:** https://github.com/speakleash/speakleash/issues

## Installation

Speakleash package can be installed from PyPi and has to be installed in a virtual environment:
```
pip install speakleash
```

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