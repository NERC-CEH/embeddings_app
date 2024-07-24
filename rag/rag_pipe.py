import logging
import time

import pandas as pd
from haystack import Pipeline


class RagPipe:

    def __init__(self, yml_file: str):
        self.pipeline = None
        self.file = yml_file
        self.logger = logging.getLogger(__name__)

    def load_rag_pipeline(self):
        """
        Loads a pipeline for haystack from a yaml file.
        """
        self.logger.info(f"Loading {self.file} as RAG pipeline source.")
        with open(self.file) as f:
            return Pipeline.loads(f.read())

    def get_rag_pipeline(self):
        if self.pipeline is None:
            self.pipeline = self.load_rag_pipeline()
        return self.pipeline

    def query(self, query: str):
        start = time.time()
        results = self.get_rag_pipeline().run(
            {
                "retriever": {"query": query},
                "prompt_builder": {"query": query},
                "answer_builder": {"query": query},
            }
        )
        end = time.time()
        self.logger.info(f"Queried in {(end - start):.3f}s")
        return self.extract_answer_and_datasets(results)

    def extract_answer_and_datasets(self, response):
        answer = response["answer_builder"]["answers"][0]
        answer_data = answer.data
        docs = [doc.meta["title"] for doc in answer.documents]
        scores = [doc.score for doc in answer.documents]
        df = pd.DataFrame({"dataset": docs, "score": scores})
        df.sort_values("score", inplace=True, ascending=False)
        return answer_data, df
