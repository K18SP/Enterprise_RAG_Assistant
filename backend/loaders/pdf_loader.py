from langchain_community.document_loaders import PyPDFLoader
from .base_loader import BaseLoader # Here we import BaseLoader class from base_loader.py

# Here we have created child class "PDFLoader" from BaseLoader
class PDFLoader(BaseLoader): 

    def load(self, file_path): # Implement the abstract load method for PDF files

        loader = PyPDFLoader(file_path)

        return loader.load()