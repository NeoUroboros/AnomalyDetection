from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.ensemble import IsolationForest
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf

class AutoencodersStrategy:
    def __init__(self, input_dim):
        # Modelo Autoencoder
        self.autoencoder = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_dim=input_dim),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(input_dim, activation='linear')
        ])
        optimizer = Adam(learning_rate=0.001)
        self.autoencoder.compile(optimizer=optimizer, loss='mse')

        # Modelo Isolation Forest
        self.isolation_forest = IsolationForest(contamination=0.05, random_state=42)

    def fit(self, data, epochs=50, batch_size=128):
        # Ajuste del Isolation Forest
        self.isolation_forest.fit(data)

        # Ajuste del Autoencoder
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)
        self.autoencoder.fit(
            train_data, train_data,
            validation_data=(val_data, val_data),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            callbacks=[early_stopping]
        )

    def predict(self, data):
        # Detecciones del Isolation Forest
        if_preds = self.isolation_forest.predict(data)
        prefiltered_data = data[if_preds == 1]  # Solo normales según IF

        # Reconstrucciones del Autoencoder
        reconstructions = self.autoencoder.predict(prefiltered_data)
        loss = np.mean((prefiltered_data - reconstructions) ** 2, axis=1)

        # Calcular umbral dinámico
        threshold = np.percentile(loss, 95)
        data['anomaly_score'] = np.concatenate((loss, np.zeros(len(data) - len(loss))))
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x > threshold else "Normal")
        return data