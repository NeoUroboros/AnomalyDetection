from sklearn.svm import OneClassSVM

from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy


class OneClassSVMStrategy(AnomalyDetectionStrategy):
    def __init__(self, kernel="rbf", gamma=0.1, nu=0.1):
        self.model = OneClassSVM(kernel=kernel, gamma=gamma, nu=nu)

    def fit(self, data):
        self.model.fit(data)

    def predict(self, data):
        scores = self.model.predict(data)
        data['anomaly_score'] = scores
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x == -1 else 'Normal')
        return data
