from rag.wrappers import PipelineWrapper
from typing import Optional, List


DEFAULT_URL = "https://catalogue.ceh.ac.uk/eidc/documents?page=1&rows=2000&term=state%3Apublished+AND+view%3Apublic+AND+recordType%3ADataset"


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
