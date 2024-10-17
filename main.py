import pandas as pd
from abc import ABC, abstractmethod
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
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

# Simular la pantalla de carga mientras se procesa el archivo
for i in tqdm(range(100), desc="Procesando datos...", ascii=True):
    time.sleep(0.4)  # Simulación de procesamiento

doc = factory.getDocument("data/raw/Jsonaexcel.xlsx")
df = doc.readDocument()
df = df.drop("Column1.created_date", axis=1)
df = df.drop("Column1.id", axis=1)
# Manejar valores NaN
df = df.fillna(0)


iso_forest = IsolationForest(contamination=0.1)
iso_forest.fit(df)

df['anomaly_score'] = iso_forest.fit_predict(df)

df['anomaly'] = df['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')

df.to_csv("data/output/Jsonaexcel.csv")

plt.figure(figsize=(6,6))
df['anomaly'].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'red'], shadow=True, startangle=90)
plt.title('Proporción de Anomalías')
plt.ylabel('')
plt.show()

print("Análisis completado y gráfico generado.")