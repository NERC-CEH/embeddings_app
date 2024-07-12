"""
API that serves up a RAG pipeline for performing queries on a chroma instance.
"""

import logging
from typing import Union
from haystack import Pipeline
from fastapi import FastAPI


logging.getLogger().setLevel(logging.INFO) 


def stream_callback(chunk):
    """
    Basic callback for streaming responses from an llm or generator.
    """
    print(chunk.content, end="", flush=True)


def load_rag_pipeline(file):
    """
    Loads a pipeline for haystack from a yaml file.
    """
    logging.info(f"Loading {file} as RAG pipeline source.")
    with open(file) as f:
        return Pipeline.loads(f.read())


file = "llama3-rag-pipe.yml"
# file = 'flan-t5-rag-pipe.yml'
pipeline = load_rag_pipeline(file)
app = FastAPI()


@app.get("/query")
def query(query_string: Union[str, None] = None):
    """
    Query the API with a prompt. This method will run the RAG pipeline and return the result.
    """
    logging.info(f'Received query: "{query_string}"')
    results = pipeline.run(
        {
            "retriever": {"query": query_string},
            "prompt_builder": {"query": query_string},
            "answer_builder": {"query": query_string}
        }
    )
    return {"query": query_string, "results": results}

