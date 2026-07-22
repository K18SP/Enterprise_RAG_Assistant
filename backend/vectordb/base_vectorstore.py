from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document

class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(self, documents: List[Document]): # Add documents
        pass

    @abstractmethod
    def similarity_search(self, query:str, k: int=5): # Similarity search and return top k relevant chunks
        pass

    @abstractmethod
    def save(self): #Save the data
        pass

    @abstractmethod
    def load(self): #Load the data
        pass
