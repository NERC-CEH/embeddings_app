from typing import List
from haystack.dataclasses import Document
from haystack.document_stores.types import DuplicatePolicy


class FileDocumentStore:
    """
    Basic document store to save ouput from a document writer to files. Documents will be saved as *.txt files using the document ID at the path defined in the constructor.
    """

    def __init__(self, path) -> None:
        self.path = path

    def write_document(self, doc: Document) -> None:
        if doc.meta["eidc_metadata_key"] == "description":
            with open(f"{self.path}/{doc.id}.txt", "w") as f:
                f.write(doc.content)

    def write_documents(
        self,
        documents: List[Document],
        policy: DuplicatePolicy = DuplicatePolicy.NONE,
    ) -> int:
        for doc in documents:
            self.write_document(doc)
        return len(documents)
