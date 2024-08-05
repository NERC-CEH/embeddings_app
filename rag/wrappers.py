import logging
from haystack import Pipeline
from typing import Optional, List

DEFAULT_URL = "https://catalogue.ceh.ac.uk/eidc/documents?page=1&rows=2000&term=state%3Apublished+AND+view%3Apublic+AND+recordType%3ADataset"


class PipelineWrapper:
    """
    Simple wrapper class for haystack pipelines
    """

    def __init__(self, yml_file: str) -> None:
        """
        Constructor which takes a yaml file as a configuration for a haystack
        pipeline.
        """
        self.pipeline = None
        self.file = yml_file
        self.logger = logging.getLogger(__name__)

    def load_pipeline(self) -> Pipeline:
        """
        Loads a pipeline for haystack from a yaml file.
        """
        self.logger.info(f"Loading {self.file} as pipeline source.")
        with open(self.file) as f:
            return Pipeline.loads(f.read())

    def get_pipeline(self) -> Pipeline:
        """
        Retrieves the pipeline, or creates it if it doesn't exist.
        """
        if self.pipeline is None:
            self.pipeline = self.load_pipeline()
        return self.pipeline


class IndexPipelineWrapper(PipelineWrapper):
    """
    Warpper for an index pipeline.
    """

    def index(
        self,
        url: Optional[str] = DEFAULT_URL,
        metadata_fields: Optional[List[str]] = None,
    ):
        self.get_pipeline().run(
            data={
                "fetcher": {"urls": [url]},
                "converter": {"metadata_fields": metadata_fields},
            }
        )
