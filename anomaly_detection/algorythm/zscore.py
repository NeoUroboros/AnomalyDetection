from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy


class ZScoreStrategy(AnomalyDetectionStrategy):
    def fit(self, data):
        pass  # Z-Score no requiere entrenamiento

    def predict(self, data):
        z_scores = (data - data.mean()) / data.std()
        threshold = 3  # Umbral para considerar valores como anomalías
        data['anomaly_score'] = z_scores.abs().max(axis=1)
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x > threshold else "Normal")
        return data
