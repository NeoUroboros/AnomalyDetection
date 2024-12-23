from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def readDoc(self):
        pass
