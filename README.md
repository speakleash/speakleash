<h1 align="center">
<img src="https://raw.githubusercontent.com/speakleash/speakleash/main/branding/logo/speakleash_logo.png" width="300">
</h1><br>

<p align="center">
    <a href="https://pypi.org/project/speakleash"><img src="https://badge.fury.io/py/speakleash.svg"></a>
    <a href="https://speakleash.org/"><img src="https://img.shields.io/badge/organisation-Speakleash-orange"></a>
    <a href="https://pypi.org/project/speakleash"><img src="https://img.shields.io/badge/python-_>=_3.6-blue"></a>
    <a href="https://speakleash.org/dashboard/"><img src="https://img.shields.io/badge/dynamic/json?url=https://cutt.ly/ywcfnFY7&query=datasetsGB&suffix=%20GB&label=datasets&color=brightgreen"></a>
    <a href="https://speakleash.org/spolecznosc-i-kontakt/"><img src="https://img.shields.io/discord/1043112910278381619?logo=discord&label=discord&color=%23603FEF"></a>
</p>

### UPDATE 05.05.2024: 
Due to the changes related with the hosting, it is recommended to update the version of the package to the newest one, using command:
```python
pip install --upgrade speakleash
```

[SpeakLeash](href="https://pypi.org/project/speakleash) is a lightweight library providing datasets for the Polish language
and tools to make them useful.

- **Website:** https://speakleash.org/
- **Datasets:** https://speakleash.org/dashboard/
- **Source code:** https://github.com/speakleash/speakleash
- **Data in action:** https://github.com/speakleash/speakleash-examples
- **Bug reports:** https://github.com/speakleash/speakleash/issues

## Installation

Speakleash package can be installed from PyPi and has to be installed in a virtual environment:
```python
pip install speakleash
```

## Basic Usage

If you just want to see the details of the datasets

```python
from speakleash import Speakleash
import os

base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)

for d in sl.datasets:
    size_mb = round(d.characters/1024/1024)
    print("Dataset: {0}, size: {1} MB, characters: {2}, documents: {3}".format(d.name, size_mb, d.characters, d.documents))
```

You can use individual properties (e.g.:***characters***, ***documents***), but you can display the entire manifest
```python
sl = Speakleash(replicate_to)
print(sl.get("plwiki").manifest)
```

If you chose one of them (***.get(name of dataset)***) then you will get a lot of text data ;-)
```python
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
```python
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
