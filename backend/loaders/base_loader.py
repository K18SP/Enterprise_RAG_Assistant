from abc import ABC, abstractmethod

# Abstract class as blueprint for all types of files
class BaseLoader(ABC):

    @abstractmethod
    def load(self, file_path): # Every loader should expose exactly one method
        pass