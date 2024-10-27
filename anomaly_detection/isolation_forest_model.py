from sklearn.ensemble import IsolationForest


class IsolationForestModel:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination)

    def fit_predict(self, data):
        return self.model.fit_predict(data)
