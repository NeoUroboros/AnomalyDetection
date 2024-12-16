import time
import pandas as pd
from anomaly_detection.strategyselector import StrategySelector
from anomaly_detection.anomaly_detector import AnomalyDetector
from scripts.data_preprocessing.preprocessing import preprocess_data
from scripts.document_processing.document_factory import DocumentFactory
from scripts.document_processing.creator_factory import *
from utils.visualization import plot_anomaly_pie

try:
    start_time = time.time()

    # Inicializar la fábrica de documentos
    factory = DocumentFactory()
    factory.registerFormat('csv', CreateCSV)
    factory.registerFormat('xlsx', CreateExcel)
    factory.registerFormat('feather', CreateFeather)
    factory.registerFormat('hdf', CreateHDF)
    factory.registerFormat('json', CreateJSON)
    factory.registerFormat('parquet', CreateParquet)
    factory.registerFormat('pickle', CreatePickle)
    factory.registerFormat('sas', CreateSAS)
    factory.registerFormat('spss', CreateSPSS)
    factory.registerFormat('sql', CreateSQL)
    factory.registerFormat('stata', CreateStata)

    # Lectura del archivo
    start_lecture_time = time.time()
    doc = factory.getDocument("data/raw/isoforest.csv")
    df = doc.readDocument()
    if df is None or df.empty:
        raise ValueError("El archivo no contiene datos o no se pudo leer correctamente.")
    end_lecture_time = time.time()

    # Preprocesamiento
    start_preprocess_time = time.time()
    columns = ["Column1.id", "Column1.created_date"]
    df = preprocess_data(df, columns)
    if df.empty:
        raise ValueError("El DataFrame está vacío después del preprocesamiento.")
    end_preprocess_time = time.time()

    # Selección de estrategia y creación del detector
    start_strategy_time = time.time()
    strategy_selector = StrategySelector(df)
    strategy = strategy_selector.select()
    if strategy is None:
        raise ValueError("No se pudo seleccionar una estrategia para los datos proporcionados.")
    detector = AnomalyDetector(strategy)
    end_strategy_time = time.time()

    # Entrenamiento y predicción
    start_fit_time = time.time()
    detector.fit(df)
    end_fit_time = time.time()

    start_predict_time = time.time()
    df_result = detector.predict(df)
    if df_result is None or df_result.empty:
        raise ValueError("La predicción no retornó resultados válidos.")
    end_predict_time = time.time()

    # Guardado y visualización
    df_result.to_csv("data/output/high_density_with_noise.csv", index=False)
 
    # Métricas de tiempo
    end_time = time.time()
    print(f"Tiempo total de lectura: {end_lecture_time - start_lecture_time:.2f}")
    print(f"Tiempo total de preprocesamiento: {end_preprocess_time - start_preprocess_time:.2f}")
    print(f"Tiempo total de selección de estrategia: {end_strategy_time - start_strategy_time:.2f}")
    print(f"Estrategia utilizada: {detector.strategy}")
    print(f"Tiempo total de entrenamiento: {end_fit_time - start_fit_time:.2f}")
    print(f"Tiempo total de predicción: {end_predict_time - start_predict_time:.2f}")
    print(f"Tiempo total: {end_time - start_time:.2f}")
    print("Análisis completado y gráfico generado.")
    plot_anomaly_pie(df_result)


except Exception as e:
    print(f"Error encontrado: {e}")
