from langchain_community.document_loaders import Docx2txtLoader
from .base_loader import BaseLoader # Here we import BaseLoader class from base_loader.py

# Here we have created child class "DOCXLoader" from BaseLoader
class DOCXLoader(BaseLoader): 

    def load(self, file_path): # Implement the abstract load method for word files

        loader = Docx2txtLoader(file_path)

        return loader.load()