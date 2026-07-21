from langchain_community.document_loaders import TextLoader
from .base_loader import BaseLoader # Here we import BaseLoader class from base_loader.py

# Here we have created child class "MarkdownLoader" from BaseLoader
class MarkdownLoader(BaseLoader): 

    def load(self, file_path): # Implement the abstract load method for markdown files

        loader = TextLoader(file_path)

        return loader.load()