import pandas as pd
from abc import ABC, abstractmethod
import sqlite3


class Document(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def readDoc(self):
        pass


class CSV(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_csv(self.filepath)


class Excel(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_excel(self.filepath)


class JSON(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_json(self.filepath)


class Parquet(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_parquet(self.filepath)


class HDF(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_hdf(self.filepath)


class Feather(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_feather(self.filepath)


class Stata(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_stata(self.filepath)


class SAS(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_sas(self.filepath)


class SPSS(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_spss(self.filepath)


class SQL(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        conn = sqlite3.connect(self.filepath)
        query = "SELECT * FROM your_table"  # Hace falta modificar segun la consulta
        return pd.read_sql_query(query, conn)


class Pickle(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_pickle(self.filepath)


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
factory.registerFormat('xlsx', CreateExcel)
factory.registerFormat('json', CreateJSON)
factory.registerFormat('parquet', CreateParquet)
factory.registerFormat('h5', CreateHDF)
factory.registerFormat('feather', CreateFeather)
factory.registerFormat('dta', CreateStata)
factory.registerFormat('sas7bdat', CreateSAS)
factory.registerFormat('sav', CreateSPSS)
factory.registerFormat('sqlite', CreateSQL)
factory.registerFormat('pkl', CreatePickle)

# Ejemplo de uso
doc = factory.getDocument("data/raw/Jsonaexcel.xlsx")
df = doc.readDocument()
print(df)
df = df.drop("Column1.created_date", axis=1)
df = df.drop("Column1.id", axis=1)
print(df)
