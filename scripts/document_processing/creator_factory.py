from scripts.document_processing.parquet_document import Parquet
from scripts.document_processing.excel_document import Excel
from scripts.document_processing.json_document import JSON
from scripts.document_processing.hdf_document import HDF
from scripts.document_processing.feather_document import Feather
from scripts.document_processing.stata_document import Stata
from scripts.document_processing.sas_document import SAS
from scripts.document_processing.spss_document import SPSS
from scripts.document_processing.sql_document import SQL
from scripts.document_processing.csv_document import CSV
from scripts.document_processing.pickle_document import Pickle
from abc import ABC, abstractmethod


class CreateDocumentObject(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def createDocument(self):
        pass

    def readDocument(self):
        document = self.createDocument()
        return document.readDoc()


class CreateCSV(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return CSV(self.filepath)


class CreateExcel(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return Excel(self.filepath)


class CreateJSON(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return JSON(self.filepath)


class CreateParquet(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return Parquet(self.filepath)


class CreateHDF(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return HDF(self.filepath)


class CreateFeather(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return Feather(self.filepath)


class CreateStata(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return Stata(self.filepath)


class CreateSAS(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return SAS(self.filepath)


class CreateSPSS(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return SPSS(self.filepath)


class CreateSQL(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return SQL(self.filepath)


class CreatePickle(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return Pickle(self.filepath)