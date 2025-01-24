import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Cargar los datasets
df_truth = pd.read_csv("datos_sinteticos_mejorado.csv", delimiter=",")  # Cambiar delimitador si es necesario
#df_pred = pd.read_csv("1.csv", delimiter=",")
df_pred = pd.read_excel("2.xlsx")


# Asegurarnos de que la columna 'ID' existe en ambos DataFrames
if 'ID' not in df_truth.columns:
    print("La columna 'ID' no se encuentra en df_truth")
if 'ID' not in df_pred.columns:
    print("La columna 'ID' no se encuentra en df_pred")

# Unir datasets por la columna común 'ID'
df = pd.merge(df_truth, df_pred, on="ID")

# Extraer las columnas necesarias
y_true = df['Etiqueta']  # Etiquetas reales
#y_pred = df['anomaly']  # Predicciones del modelo
y_pred = df['Prediction_binned']  # Predicciones del modelo

# Calcular métricas
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='binary', pos_label='Anomaly')  # Especificar la clase positiva
recall = recall_score(y_true, y_pred, average='binary', pos_label='Anomaly')
f1 = f1_score(y_true, y_pred, average='binary', pos_label='Anomaly')

# Mostrar resultados
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")

"""
dynamic_thresholds = z_scores.abs().quantile(0.999)
Accuracy: 0.92648
Precision: 0.05789473684210526
Recall: 0.0308
F1-Score: 0.0402088772845953

Accuracy: 0.94582
Precision: 0.035555555555555556
Recall: 0.0032
F1-Score: 0.005871559633027523
"""