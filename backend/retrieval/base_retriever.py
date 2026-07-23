from abc import ABC, abstractmethod

class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(self, query:str, k:int=5):

        pass