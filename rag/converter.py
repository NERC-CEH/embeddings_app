from haystack import component, Document, logging
from typing import Optional, List, Union
from haystack.dataclasses import ByteStream
from haystack.components.converters.utils import get_bytestream_from_source
import json

logger = logging.getLogger(__name__)


@component
class EIDCJSONToDocument:
    """
    Converts a json response from the EIDC API to a set of Documents based on the results.
    """

    def __init__(self, metadata_fields: Optional[List[str]] = None):
        self.metadata_fields = metadata_fields

    @component.output_types(documents=List[Document])
    def run(self, sources: List[Union[ByteStream]]):
        documents = []
        for source in sources:
            try:
                bytestream = get_bytestream_from_source(source)
            except Exception as e:
                logger.warning(
                    "Could not read {source}. Skipping. Error: {error}",
                    source=source,
                    error=e,
                )

            try:
                json_string = bytestream.data.decode("utf-8")
                api_response = json.loads(json_string)
                for dataset in api_response["results"]:
                    document = Document(content=dataset["title"])
                    documents.append(document)

            except Exception as conversion_e:
                logger.warning(
                    "Failed to extract document(s) from {source}. Skipping. Error: {error}",
                    source=source,
                    error=conversion_e,
                )

        return {"documents": documents}
