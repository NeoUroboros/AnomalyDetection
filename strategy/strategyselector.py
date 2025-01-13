from sklearn.decomposition import PCA
from algorythm.autoencoders import AutoencodersStrategy
from algorythm.dbscan import DBSCANStrategy
from algorythm.isolation_forest import IsolationForestStrategy
from algorythm.zscore import ZScoreStrategy
from scipy.stats import normaltest
from sklearn.neighbors import NearestNeighbors

class StrategySelector:
    def __init__(self, data, requirements=None):
        self.data = data
        self.requirements = requirements
        self.num_rows, self.num_columns = data.shape
        self.missing_percentage = data.isnull().mean().mean()

    def _get_temporary_numeric_columns(self):
        """
        Filtra columnas numéricas en el DataFrame sin modificar el original.
        """
        numeric_data = self.data.select_dtypes(include=['number'])
        if numeric_data.empty:
            print("No se encontraron columnas numéricas en los datos.")
        return numeric_data

    def check_dimensionality(self):
        # Verifica si los datos tienen más de una columna
        if self.data.shape[1] <= 50:
            return None  # No tiene sentido aplicar PCA si hay menos de 50 columnas

        # Aplica PCA a los datos
        pca = PCA()
        pca.fit(self.data)

        # Calcula la varianza explicada acumulada
        explained_variance = pca.explained_variance_ratio_.cumsum()

        # Verifica si tenemos al menos 10 componentes y si la varianza acumulada supera el 85% en el componente 10
        if len(explained_variance) >= 10 and explained_variance[9] >= 0.85:  # Cambia índice y relaja el criterio
            return AutoencodersStrategy(input_dim=self.num_columns)

        return None


    def check_data_volume(self):
        if self.num_rows > 1_000_000:
            return IsolationForestStrategy()
        return None
    
    def check_distribution(self):
        sampled_data = self.data.sample(min(550000, len(self.data)))
        p_values = sampled_data.apply(normaltest, axis=0).iloc[1]
    
        print("P-values por columna:", p_values)

        # Relajamos el criterio al usar el promedio de los p-values
        if p_values.mean() > 0.05:  # Condición basada en el promedio
            print("Seleccionado: ZScoreStrategy (distribución normal detectada).")
            return ZScoreStrategy()

        print("No se seleccionó ZScoreStrategy (distribución no completamente normal).")
        return None


    def check_density(self):
        numeric_data = self._get_temporary_numeric_columns()
        if len(numeric_data) <= 15000:
            # Calcular las distancias a los 5 vecinos más cercanos
            neighbors = NearestNeighbors(n_neighbors=5).fit(self.data)
            distances, _ = neighbors.kneighbors(self.data)

            # Calculamos la densidad basada en la distancia promedio a los vecinos
            avg_density = distances.mean()
            std_density = distances.std()  # También evaluamos la dispersión

            print(f"Promedio de densidad: {avg_density}, Desviación estándar: {std_density}")

            # Condición mejorada para determinar si DBSCAN es apropiado
            if avg_density < 4 and std_density < 3:  # Ajusta estos umbrales según tus datos
                print("DBSCANStrategy seleccionado debido a alta densidad en los datos.")
                return DBSCANStrategy(eps=1.05, min_samples=17)

            # Si no se cumplen las condiciones, devuelve None
        return None

    def select(self):
        for check in [
            self.check_dimensionality,
            self.check_data_volume,
            self.check_distribution,
            self.check_density,
        ]:
            strategy = check()
            if strategy is not None:
                return strategy

        # Caso por defecto
        return IsolationForestStrategy()
