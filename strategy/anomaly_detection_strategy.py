from abc import ABC, abstractmethod


class AnomalyDetectionStrategy(ABC):
    @abstractmethod
    def fit(self, data):
        pass

    @abstractmethod
    def predict(self, data):
        pass
