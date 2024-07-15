#!/usr/bin/env python
from ast import literal_eval

import chromadb
import pandas as pd

COLLECTION_NAME = "eidc_datasets"
FILE_NAME = "eidc_embeddings.csv"

EMBEDDINGS_HEADER = "embeddings"
UMAP_HEADER = "umap_reduced"
TITLE_HEADER = "title"
DESC_HEADER = "description"
LIN_HEADER = "lineage"
TOPIC_HEADER = "topic_number"
KEY_HEADER = "topic_keywords"

if __name__ == "__main__":
    client = chromadb.HttpClient(host="localhost", port=8000)
    print("Connecting to database...")
    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"Reading {FILE_NAME}...")
    df = pd.read_csv(FILE_NAME)
    embeddings = [literal_eval(e) for e in df[EMBEDDINGS_HEADER]]
    metadatas = list(
        zip(
            df[UMAP_HEADER].to_list(),
            df[TITLE_HEADER].to_list(),
            df[DESC_HEADER].to_list(),
            df[LIN_HEADER].to_list(),
            df[TOPIC_HEADER].to_list(),
            df[KEY_HEADER].to_list(),
        )
    )
    metadatas = [
        {
            UMAP_HEADER: a[0],
            TITLE_HEADER: a[1],
            DESC_HEADER: a[2],
            LIN_HEADER: a[3],
            TOPIC_HEADER: a[4],
            KEY_HEADER: a[5],
        }
        for a in metadatas
    ]
    doc_ids = [f"doc_{idx:04d}" for idx in df.index.values.tolist()]
    docs = list(
        map(
            "\n".join,
            zip(
                df[TITLE_HEADER].to_list(),
                df[DESC_HEADER].to_list(),
                df[LIN_HEADER].to_list(),
            ),
        )
    )
    print("Adding data...")
    collection.add(
        embeddings=embeddings, metadatas=metadatas, ids=doc_ids, documents=docs
    )
