from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from .base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def load(self, file_path: str) -> List[Document]:

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        file_name = Path(file_path).name
        file_extension = Path(file_path).suffix

        for index, doc in enumerate(documents):

            # Keep useful metadata
            doc.metadata["source"] = file_name
            doc.metadata["file_path"] = file_path
            doc.metadata["filename"] = file_name
            doc.metadata["extension"] = file_extension

            # Ensure page always exists
            doc.metadata["page"] = doc.metadata.get("page", index)

        return documents