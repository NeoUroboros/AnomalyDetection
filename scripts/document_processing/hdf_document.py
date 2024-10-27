import pandas as pd
from scripts.document_processing.base_document import Document

class HDF(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_hdf(self.filepath)
