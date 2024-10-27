from scripts.document_processing.document_factory import DocumentFactory
from scripts.document_processing.creator_factory import *

from anomaly_detection.isolation_forest_model import IsolationForestModel
from scripts.data_preprocessing.preprocessing import preprocess_data
from utils.visualization import plot_anomaly_pie

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

df = preprocess_data(df)

iso_forest = IsolationForestModel(contamination=0.1)
df['anomaly_score'] = iso_forest.fit_predict(df)

df['anomaly'] = df['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')

df.to_csv("data/output/Jsonaexcel.csv", index=False)

plot_anomaly_pie(df)
print("Análisis completado y gráfico generado.")
