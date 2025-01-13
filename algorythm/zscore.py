from strategy.anomaly_detection_strategy import AnomalyDetectionStrategy
import numpy as np
import pandas as pd

class ZScoreStrategy(AnomalyDetectionStrategy):
    def fit(self, data):
        pass  # Z-Score no requiere entrenamiento

    def predict(self, data):
        # Calcula el Z-Score
        z_scores = (data - data.mean()) / data.std()
    
        # Calcula el umbral dinámico basado en el percentil (específico por columna)
        dynamic_thresholds = z_scores.abs().quantile(0.9999)
    
        # Identifica las filas donde alguna característica supera el umbral dinámico
        is_anomaly = (z_scores.abs() > dynamic_thresholds).any(axis=1)

        # Agrega las columnas de resultados al DataFrame
        data['anomaly_score'] = z_scores.abs().max(axis=1)  # Máximo Z-Score por fila
        data['anomaly'] = is_anomaly.apply(lambda x: "Anomaly" if x else "Normal")

        return data
