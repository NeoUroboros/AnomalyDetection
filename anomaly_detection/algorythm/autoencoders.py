from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy
import numpy as np
import tensorflow as tf

class AutoencodersStrategy(AnomalyDetectionStrategy):
    def __init__(self, input_dim):
        self.model =  tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_dim=input_dim),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(input_dim, activation='linear')
        ])
        self.model.compile(optimizer='adam', loss='mse')

    def fit(self, data, epochs=50, batch_size=32):
        self.model.fit(data, data, epochs=epochs, batch_size=batch_size, verbose=0)

    def predict(self, data):
        reconstructions = self.model.predict(data)
        loss = np.mean((data - reconstructions) ** 2, axis=1)
        threshold = np.percentile(loss, 95)  # Umbral de anomalías
        data['anomaly_score'] = loss
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x > threshold else "Normal")
        return data
