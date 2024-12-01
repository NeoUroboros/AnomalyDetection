from sklearn.ensemble import IsolationForest

from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy


# Implementa Isolation Forest como una estrategia
class IsolationForestStrategy(AnomalyDetectionStrategy):
    def __init__(self, contamination=0.1, random_state=42):
        self.model = IsolationForest(contamination=contamination, random_state=random_state)

    def fit(self, data):
        self.model.fit(data)

    def predict(self, data):
        data['anomaly_score'] = self.model.predict(data)
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')
        return data
