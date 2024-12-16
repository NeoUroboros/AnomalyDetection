from prophet import Prophet
import pandas as pd


class ProphetAnomalyDetectionStrategy:
    def __init__(self, threshold=3):
        """
        Estrategia basada en Prophet para detectar anomalías en series temporales.
        """
        self.model = None
        self.threshold = threshold

    def fit(self, data):
        """
        Ajusta el modelo Prophet con los datos proporcionados.
        """
        # Asegúrate de que las columnas están correctas
        print(data.columns)  # Verifica las columnas antes de ajustarse al modelo
        self.model = Prophet()
        self.model.fit(data)

    def predict(self, data):
        """
        Predice y detecta anomalías basadas en los residuos de las predicciones de Prophet.
        """
        future = self.model.make_future_dataframe(periods=len(data))
        forecast = self.model.predict(future)

        # Verifica las primeras filas de las predicciones
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

        # Unir los datos reales y las predicciones
        data = data.merge(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds', how='left')

        # Calcular residuos
        data['residual'] = data['y'] - data['yhat']
        std_dev = data['residual'].std()

        # Etiquetar anomalías
        data['anomaly'] = data['residual'].apply(
            lambda x: 'Anomaly' if abs(x) > self.threshold * std_dev else 'Normal'
        )

        return data


