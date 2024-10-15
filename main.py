import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def __init__(self, doc):
        self.doc = doc

    def readDoc(self):
        pass

    def writeDoc(self):
        pass
