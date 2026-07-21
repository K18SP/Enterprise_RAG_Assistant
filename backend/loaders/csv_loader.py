from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import CSVLoader
from .base_loader import BaseLoader # Here we import BaseLoader class from base_loader.py

# Here we have created child class "CSVDocumentLoader" from BaseLoader
class CSVDocumentLoader(BaseLoader):

    def load(self, file_path):

        loader = CSVLoader(file_path)# Implement the abstract load method for csv files

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