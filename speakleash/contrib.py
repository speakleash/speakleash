from itertools import chain

import pandas as pd
from datasets import Dataset
from joblib import Parallel, delayed
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm


def sl_hf_dataset_for_tokenizer(
    sl, sl_dataset_name, tokenizer, max_length, margin=192, min_length=7
):
    """
    Create a HuggingFace dataset from a SpeakLeash dataset.

    params: sl: SpeakLeash object
    params: sl_dataset_name: SpeakLeash dataset name
    params: tokenizer: HuggingFace tokenizer
    params: max_length: maximum length of the tokenized text
    params: margin: margin subtract from the max_length (this helps
        to avoid RecursiveCharacterTextSplitter returning too many
        too long chunks)
    params: min_length: minimum length of the tokenized text
    returns: HuggingFace dataset
    """
    corpus = sl.get(sl_dataset_name)

    # this is used only for length calculation
    def token_len(text):
        return len(tokenizer.encode(text, max_length=None, truncation=False))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_length - margin,
        chunk_overlap=0,
        length_function=token_len,
    )

    dataset = Parallel(n_jobs=-1)(
        delayed(text_splitter.split_text)(document)
        for document in tqdm(corpus.data, total=corpus.manifest["stats"]["documents"])
    )
    dataset = list(chain.from_iterable(dataset))

    df = pd.DataFrame(dataset, columns=["text"])
    hf_dataset = Dataset.from_pandas(df)

    hf_dataset = hf_dataset.map(
        lambda examples: tokenizer(examples["text"], truncation=True, max_length=max_length),
        batched=True,
    )
    # Filter out samples that have input_ids exceeding max_length
    hf_dataset = hf_dataset.filter(
        lambda sample: min_length <= len(sample["input_ids"]) < max_length
    )

    return hf_dataset
