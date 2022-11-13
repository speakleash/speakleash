# SpeakLeash

SpeakLeash agnostic dataset for Polish

## Basic Usage

```
from speakleash import Speakleash
import os

base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)

for d in sl.datasets:
    print(d.name)
    for doc in d.data:
        print(doc[:10])

```

or 

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


