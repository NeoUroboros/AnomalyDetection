from keras.src.callbacks import EarlyStopping
from tensorflow.keras.optimizers import RMSprop
import keras
from strategy.anomaly_detection_strategy import AnomalyDetectionStrategy
import numpy as np
import tensorflow as tf
print(tf.__version__)

class AutoencodersStrategy(AnomalyDetectionStrategy):
    def __init__(self, input_dim):
        # Modelo con menos capas y neuronas
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(4, activation='relu', input_dim=input_dim),  # Menos neuronas
            tf.keras.layers.Dense(4, activation='relu'),  # Menos neuronas
            tf.keras.layers.Dense(input_dim, activation='linear')  # Capa de salida
        ])

        self.model.compile(loss='mse')
        

#Modelo ya entrenado 
    def fit(self, data):
        pass

    def predict(self, data):
        reconstructions = keras.models.load_model("autoencoder_model.h5").predict(data)
        print("Got me here")
        loss = np.mean((data - reconstructions) ** 2, axis=1)
        threshold = np.percentile(loss, 95)  # Umbral de anomalías
        data['anomaly_score'] = loss
        data['anomaly'] = data['anomaly_score'].apply(lambda x: "Anomaly" if x > threshold else "Normal")
        return data

'''Modelo sin entrenar entrenado:
   
'''