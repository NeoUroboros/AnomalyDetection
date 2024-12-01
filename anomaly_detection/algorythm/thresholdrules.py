from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy


class ThresholdRulesStrategy(AnomalyDetectionStrategy):
    def __init__(self, thresholds):
        self.thresholds = thresholds  # Diccionario con umbrales por columna

    def fit(self, data):
        pass  # No requiere entrenamiento

    def predict(self, data):
        def check_anomaly(row):
            for column, (low, high) in self.thresholds.items():
                if not low <= row[column] <= high:
                    return "Anomaly"
            return "Normal"

        data['anomaly'] = data.apply(check_anomaly, axis=1)
        return data
