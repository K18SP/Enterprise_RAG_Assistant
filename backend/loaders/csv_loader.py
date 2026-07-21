from langchain_community.document_loaders import CSVLoader
from .base_loader import BaseLoader # Here we import BaseLoader class from base_loader.py

# Here we have created child class "CSVDocumentLoader" from BaseLoader
class CSVDocumentLoader(BaseLoader):

    def load(self, file_path):

        loader = CSVLoader(file_path)# Implement the abstract load method for csv files

        return loader.load()