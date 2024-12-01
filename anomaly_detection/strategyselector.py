from sklearn.decomposition import PCA

from anomaly_detection.algorythm.autoencoders import AutoencodersStrategy
from anomaly_detection.algorythm.dbscan import DBSCANStrategy
from anomaly_detection.algorythm.isolation_forest import IsolationForestStrategy
from anomaly_detection.algorythm.thresholdrules import ThresholdRulesStrategy
from anomaly_detection.algorythm.zscore import ZScoreStrategy
from scipy.stats import normaltest


class StrategySelector:
    def __init__(self, data, requirements=None):
        self.data = data
        self.requirements = requirements
        self.num_rows, self.num_columns = data.shape
        self.missing_percentage = data.isnull().mean().mean()

    #    def check_missing_values(self):
    #        if self.missing_percentage > 0.2:
    #            return ThresholdRulesStrategy()
    #        return None

    #    def check_dimensionality(self):
    #        explained_variance = PCA().fit(self.data).explained_variance_ratio_.cumsum()
    #        if explained_variance[10] > 0.9:
    #            return AutoencodersStrategy(input_dim=self.num_columns)
    #        return None

    def check_data_volume(self):
        if self.num_rows > 1_000_000:
            return IsolationForestStrategy()
        return None

    from scipy.stats import normaltest

    def check_distribution(self):
        # Toma un muestreo limitado (máx. 500000 filas) para el test
        sampled_data = self.data.sample(min(500000, len(self.data)))

        # Aplica `normaltest` por columna y toma los p-values
        p_values = sampled_data.apply(normaltest, axis=0).iloc[1]

        # Comprueba si todas las columnas tienen p_value > 0.05
        if (p_values > 0.05).all():
            return ZScoreStrategy()

        return None

    def check_density(self):
        from sklearn.neighbors import NearestNeighbors
        neighbors = NearestNeighbors(n_neighbors=5).fit(self.data)
        distances, _ = neighbors.kneighbors(self.data)
        avg_density = distances.mean()
        if avg_density < 0.1:
            return DBSCANStrategy(eps=0.5, min_samples=5)
        return None

    def select(self):
        for check in [
            #            self.check_missing_values,
            #            self.check_dimensionality,
            #self.check_data_volume,
            self.check_distribution,
            #self.check_density,
        ]:
            strategy = check()
            if strategy is not None:
                return strategy

        # Caso por defecto
        return IsolationForestStrategy()
