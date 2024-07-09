"""
API that serves up a RAG pipeline for performing queries on a chroma instance.
"""

from typing import Union
from haystack import Pipeline
from fastapi import FastAPI


def stream_callback(chunk):
    """
    Basic callback for streaming responses from an llm or generator.
    """
    print(chunk.content, end="", flush=True)


def load_rag_pipeline(file):
    """
    Loads a pipeline for haystack from a yaml file.
    """
    print(f'Loading {file} as RAG pipeline source.')
    with open(file) as f:
        return Pipeline.loads(f.read())

file = 'llama3-rag-pipe.yml'
pipeline = load_rag_pipeline(file)
app = FastAPI()


@app.get("/query")
def query(query_string: Union[str, None] = None):
    """
    Query the API with a prompt. This method will run the RAG pipeline and return the result.
    """
    print(f'Received query: "{query_string}"')
    results = pipeline.run(
        {
            "retriever": {"query": query_string, "top_k": 3},
            "prompt_builder": {"query": query_string},
            "llm": {"generation_kwargs": {"max_new_tokens": 100}},
        }
    )
    return {"query": query_string, "results": results}
