from sklearn.cluster import DBSCAN

from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy

from sklearn.preprocessing import StandardScaler


class DBSCANStrategy(AnomalyDetectionStrategy):
    def __init__(self, eps=0.5, min_samples=5):
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.scaler = StandardScaler()

    def fit(self, data):
        pass  # DBSCAN no requiere entrenamiento previo

    def predict(self, data):
        # Normaliza los datos antes de aplicar DBSCAN
        normalized_data = self.scaler.fit_transform(data)

        # Aplica DBSCAN sobre los datos normalizados
        labels = self.model.fit_predict(normalized_data)

        # Agrega las columnas de resultados al DataFrame original
        data['anomaly_score'] = labels
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')
        return data

