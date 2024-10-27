import time
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from sklearn.ensemble import IsolationForest
from scripts.document_processing.document_factory import DocumentFactory
from scripts.document_processing.creator_factory import *
from scripts.data_preprocessing.preprocessing import preprocess_data
from utils.visualization import plot_anomaly_pie

start_time = time.time()

factory = DocumentFactory()
factory.registerFormat('csv', CreateCSV)
factory.registerFormat('xlsx', CreateExcel)
factory.registerFormat('json', CreateJSON)
factory.registerFormat('parquet', CreateParquet)
factory.registerFormat('sqlite', CreateSQL)
factory.registerFormat('h5', CreateHDF)
factory.registerFormat('feather', CreateFeather)
factory.registerFormat('dta', CreateStata)
factory.registerFormat('sas7bdat', CreateSAS)
factory.registerFormat('sav', CreateSPSS)
factory.registerFormat('pkl', CreatePickle)

doc = factory.getDocument("data/raw/Jsonaexcel.xlsx")
df = doc.readDocument()
columns = ["Column1.id", "Column1.created_date"]
df = preprocess_data(df, columns)

iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(df)

n_splits = 4
df_splits = np.array_split(df, n_splits)


def predict_chunk(chunk):
    chunk['anomaly_score'] = iso_forest.predict(chunk)
    chunk['anomaly'] = chunk['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')
    return chunk


# Ejecutar en paralelo
df_processed = Parallel(n_jobs=n_splits)(delayed(predict_chunk)(chunk) for chunk in df_splits)

# Concatenar y guardar el resultado
df_result = pd.concat(df_processed)
df_result.to_csv("data/output/Jsonaexcel.csv", index=False)

# Graficar resultados
plot_anomaly_pie(df_result)
print("Análisis completado y gráfico generado.")

# Tiempo total
end_time = time.time()
print("Tiempo total:", end_time - start_time)
