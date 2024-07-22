import logging

import pandas as pd
from haystack import Pipeline

logging.getLogger().setLevel(logging.INFO)

file = "flan-t5-rag-pipe.yml"
pipeline = None


def load_rag_pipeline(file):
    """
    Loads a pipeline for haystack from a yaml file.
    """
    logging.info(f"Loading {file} as RAG pipeline source.")
    with open(file) as f:
        return Pipeline.loads(f.read())


def get_rag_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = load_rag_pipeline(file)
    return pipeline


def query(query: str):
    results = get_rag_pipeline().run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        }
    )
    return extract_answer_and_datasets(results)


def extract_answer_and_datasets(response):
    answer = response["answer_builder"]["answers"][0]
    answer_data = answer.data
    docs = [doc.meta["title"] for doc in answer.documents]
    scores = [doc.score for doc in answer.documents]
    df = pd.DataFrame({"dataset": docs, "score": scores})
    df.sort_values("score", inplace=True, ascending=False)
    return answer_data, df
