from abc import ABC, abstractmethod


class BaseTransaction(ABC):

    @abstractmethod
    def execute(self):
        pass


    @abstractmethod
    def rollback(self):
        pass