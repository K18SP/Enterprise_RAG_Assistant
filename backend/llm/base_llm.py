from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, query:str, context:str)->str:
        """
        Generate an answer using the query and retrieved context.
        """
        pass