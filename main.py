import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def readDoc(self):
        pass

    @abstractmethod
    def writeDoc(self, out):
        pass


class CSV(Document):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.document = None

    def readDoc(self):
        self.document = pd.read_csv(self.filepath)
        return self.document

    def writeDoc(self, out):
        if self.document is not None:
            return self.document.to_csv(out)


class CreateDocumentObject(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath
        self.document = None

    @abstractmethod
    def createDocument(self):
        pass

    def readDocument(self):
        self.document = self.createDocument()
        return self.document.readDoc()

    def writeDocument(self, out):
        if self.document is not None:
            return self.document.writeDoc(out)


class CreateCSV(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return CSV(self.filepath)


class DocumentFactory:
    def __init__(self):
        self.creators = {}

    def registerFormat(self, extension, creator):
        self.creators[extension] = creator

    def getDocument(self, filepath):
        extension = filepath.split(".")[-1]
        creator = self.creators.get(extension)
        if not creator:
            raise ValueError(f"No document handler for extension: {extension}")
        return creator(filepath)


factory = DocumentFactory()
factory.registerFormat('csv', CreateCSV)

doc = factory.getDocument("data/raw/iris.csv")

df = doc.readDocument()
print(df)
