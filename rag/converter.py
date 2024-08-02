from haystack import component, Document, logging
from typing import Optional, List, Union
from haystack.dataclasses import ByteStream
from haystack.components.converters.utils import get_bytestream_from_source
import json

logger = logging.getLogger(__name__)


@component
class EIDCJSONToDocument:
    """
    Converts a JSON response from the EIDC API to a set of Documents based on the results.

    Each metadata field from the eidc will be individually converted to a document with referene to the dataset identifier and key name in the document metadata.

    Alternatively, a list of fields can be specified to extract only the required metadata.
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
                api_response = json.loads(bytestream.data.decode("utf-8"))

                for dataset in api_response["results"]:
                    keys = (
                        self.metadata_fields
                        if self.metadata_fields
                        else dataset
                    )
                    for key in keys:
                        metadata = {
                            "src_dataset": dataset["identifier"],
                            "eidc_metadata_key": key,
                        }
                        doc = Document(
                            content=str(dataset[key]), meta=metadata
                        )
                        documents.append(doc)

            except Exception as conversion_e:
                logger.warning(
                    "Failed to extract document(s) from {source}. Skipping. Error: {error}",
                    source=source,
                    error=conversion_e,
                )

        return {"documents": documents}
