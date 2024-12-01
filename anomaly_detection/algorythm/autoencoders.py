from keras.src.callbacks import EarlyStopping
from tensorflow.keras.optimizers import RMSprop
from anomaly_detection.anomaly_detection_strategy import AnomalyDetectionStrategy
import numpy as np
import tensorflow as tf


class AutoencodersStrategy(AnomalyDetectionStrategy):
    def __init__(self, input_dim):
        # Modelo con menos capas y neuronas
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(4, activation='relu', input_dim=input_dim),  # Menos neuronas
            tf.keras.layers.Dense(4, activation='relu'),  # Menos neuronas
            tf.keras.layers.Dense(input_dim, activation='linear')  # Capa de salida
        ])

        # Optimización con RMSprop
        optimizer = RMSprop(learning_rate=0.01)
        self.model.compile(optimizer=optimizer, loss='mse')

    def fit(self, data, epochs=50, batch_size=64):  # Ajuste del tamaño del batch
        early_stopping = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)

        # Entrenamiento con EarlyStopping
        self.model.fit(data, data, epochs=epochs, batch_size=batch_size, verbose=0, callbacks=[early_stopping])

    def predict(self, data):
        reconstructions = self.model.predict(data)
        loss = np.mean((data - reconstructions) ** 2, axis=1)
        threshold = np.percentile(loss, 95)  # Umbral de anomalías
        data['anomaly_score'] = loss
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x > threshold else "Normal")
        return data
