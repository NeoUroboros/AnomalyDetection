from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy


class AnomalyDetector:
    def __init__(self, strategy: AnomalyDetectionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: AnomalyDetectionStrategy):
        self.strategy = strategy

    def fit(self, data):
        self.strategy.fit(data)

    def predict(self, data):
        return self.strategy.predict(data)
