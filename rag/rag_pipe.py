import logging
import time

import pandas as pd
from haystack import Pipeline


class RagPipe:
    """
    Wrapper class to provide easy access to a haystack pipeline.
    """

    def __init__(self, yml_file: str) -> None:
        """
        Constructor which takes a yaml file as a configuration for a haystack
        pipeline.
        """
        self.pipeline = None
        self.file = yml_file
        self.logger = logging.getLogger(__name__)

    def load_rag_pipeline(self) -> Pipeline:
        """
        Loads a pipeline for haystack from a yaml file.
        """
        self.logger.info(f"Loading {self.file} as RAG pipeline source.")
        with open(self.file) as f:
            return Pipeline.loads(f.read())

    def get_rag_pipeline(self) -> Pipeline:
        """
        Retrieves the pipeline, or creates it if it doesn't exist.
        """
        if self.pipeline is None:
            self.pipeline = self.load_rag_pipeline()
        return self.pipeline

    def query(self, query: str) -> tuple[str, pd.DataFrame]:
        """
        Queries the pipeline and return the generated answer and the datasets
        retrieved by the pipeline.
        """
        start = time.time()
        results = self.get_rag_pipeline().run(
            {
                "retriever": {"query": query},
                "prompt_builder": {"query": query},
                "answer_builder": {"query": query},
            },
            include_outputs_from={"prompt_builder"},
        )
        end = time.time()
        self.logger.info(f"Queried in {(end - start):.3f}s")
        self.logger.debug(f"{results['prompt_builder']}")
        answer = results["answer_builder"]["answers"][0]
        return answer.data, self.extract_datasets(answer)

    def extract_datasets(self, answer) -> pd.DataFrame:
        """
        Extracts the datasets from the pipelines return object and returns
        them in a dataframe with their scores.
        """
        docs = [doc.meta["dataset_title"] for doc in answer.documents]
        fields = [doc.meta["eidc_metadata_key"] for doc in answer.documents]
        scores = [doc.score for doc in answer.documents]
        df = pd.DataFrame(
            {"dataset": docs, "metadata": fields, "score": scores}
        )
        df.sort_values("score", inplace=True, ascending=False)
        return df
