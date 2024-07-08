"""
API that serves up a RAG pipeline for performing queries on a chroma instance.
"""

from typing import Union

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceLocalGenerator
from haystack import Pipeline

from fastapi import FastAPI


def create_pipeline():
    """
    Create the RAG pipeline.
    """
    print("Setting up chroma db...")
    document_store = ChromaDocumentStore(
        collection_name="eidc_datasets",
        persist_path="chroma-data",
    )
    retriever = ChromaQueryTextRetriever(document_store, top_k=2)
    print("Creating prompt template...")
    template = """
    Given the following information, answer the question.

    Question: {{query}}

    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Answer:
    """

    prompt_builder = PromptBuilder(template=template)
    models = [
        "openai-community/gpt2",
        "google/flan-t5-large",
        "MBZUAI/LaMini-Flan-T5-783M",
        "google/long-t5-tglobal-base",
    ]
    model_name = models[1]
    print(f"Setting up model ({model_name})...")
    llm = HuggingFaceLocalGenerator(
        model=model_name,
        task="text2text-generation",
        generation_kwargs={"max_new_tokens": 100, "temperature": 0.9},
    )
    print("Warming up model...")
    llm.warm_up()
    print("Creating haystack pipeline...")
    rag_pipe = Pipeline()
    rag_pipe.add_component("retriever", retriever)
    rag_pipe.add_component("prompt_builder", prompt_builder)
    rag_pipe.add_component("llm", llm)
    rag_pipe.connect("retriever.documents", "prompt_builder.documents")
    rag_pipe.connect("prompt_builder", "llm")
    return rag_pipe


pipeline = create_pipeline()
app = FastAPI()


@app.get("/query")
def query(query_string: Union[str, None] = None):
    """
    Query the API with a prompt. This method will run the RAG pipeline and return the result.
    """
    results = pipeline.run(
        {
            "retriever": {"query": query_string, "top_k": 2},
            "prompt_builder": {"query": query_string},
            "llm": {"generation_kwargs": {"max_new_tokens": 100}},
        }
    )
    return {"query": query_string, "results": results}
