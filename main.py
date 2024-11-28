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

start_lecture_time = time.time()
doc = factory.getDocument("data/raw/Jsonaexcel.csv")
df = doc.readDocument()
end_lecture_time = time.time()

start_preprocess_time = time.time()
columns = ["Column1.id", "Column1.created_date"]
df = preprocess_data(df, columns)
end_preprocess_time = time.time()

start_isomodel_time = time.time()
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(df)
end_isolationtreemodel_time = time.time()

n_splits = 4
df_splits = np.array_split(df, n_splits)


def predict_chunk(chunk):
    chunk['anomaly_score'] = iso_forest.predict(chunk)
    chunk['anomaly'] = chunk['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')
    return chunk


start_paral_time = time.time()
df_processed = Parallel(n_jobs=n_splits)(delayed(predict_chunk)(chunk) for chunk in df_splits)
end_parallel_time = time.time()

df_result = pd.concat(df_processed)
df_result.to_csv("data/output/Jsonaexcel.csv", index=False)

plot_anomaly_pie(df_result)
print("Análisis completado y gráfico generado.")
end_time = time.time()

print(f"Tiempo total de lectura: {end_lecture_time - start_lecture_time:.2f}")
print(f"Tiempo total de preprocesamiento: {end_preprocess_time - start_preprocess_time:.2f}")
print(
    f"Tiempo total de creacion del modelo de Isolation Forest: {end_isolationtreemodel_time - start_isomodel_time:.2f}")
print(
    f"Tiempo total de ejecucion del algorimto Isolation Forest en paralelo: {end_parallel_time - start_paral_time:.2f}")
print(f"Tiempo total: {end_time - start_time:.2f}")