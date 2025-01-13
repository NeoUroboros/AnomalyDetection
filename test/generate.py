import numpy as np
import pandas as pd
from scipy.stats import normaltest
from sklearn.datasets import make_blobs

def generate_anomaly_dataset(n_samples=50000, n_features=27, anomaly_ratio=0.05, random_state=42):
    """
    Genera un dataset sintético para detección de anomalías con una separación clara entre normales y anomalías.
    
    :param n_samples: Número total de muestras.
    :param n_features: Número de características.
    :param anomaly_ratio: Proporción de anomalías en el dataset.
    :param random_state: Semilla para reproducibilidad.
    :return: DataFrame con datos generados.
    """
    np.random.seed(random_state)
    
    # Calcular número de anomalías y normales
    n_anomalies = int(n_samples * anomaly_ratio)
    n_normals = n_samples - n_anomalies
    
    # Generar datos normales con distribución normal
    normal_data = np.random.normal(loc=0, scale=1, size=(n_normals, n_features))
    
    # Generar anomalías con valores más extremos o distribuciones diferentes
    anomaly_data = np.random.normal(loc=5, scale=2, size=(n_anomalies, n_features))
    
    # Concatenar datos y etiquetas
    X = np.vstack((normal_data, anomaly_data))
    y = np.array(['Normal'] * n_normals + ['Anomaly'] * n_anomalies)
    
    # Mezclar los datos
    shuffle_indices = np.random.permutation(n_samples)
    X = X[shuffle_indices]
    y = y[shuffle_indices]
    
    # Crear DataFrame
    df = pd.DataFrame(X, columns=[f'Caracteristica_{i+1}' for i in range(n_features)])
    df['Etiqueta'] = y
    
    # Añadir columna ID
    df.insert(0, 'ID', np.arange(n_samples))  # Agregar la columna ID al principio
    
    return df

def generate_enhanced_dataset(n_samples=50000, n_features=27, anomaly_ratio=0.05, random_state=42):
    np.random.seed(random_state)

    # Generar datos estrictamente normales con dispersión mínima
    data = np.random.normal(loc=0, scale=1, size=(n_samples, n_features))
    df = pd.DataFrame(data, columns=[f'Caracteristica_{i+1}' for i in range(n_features)])
    df['Etiqueta'] = 'Normal'

    # Determinar cuántas anomalías crear
    n_anomalies = int(n_samples * anomaly_ratio)
    anomaly_indices = np.random.choice(df.index, size=n_anomalies, replace=False)

    # Introducir anomalías muy destacadas en múltiples características
    for col in np.random.choice(df.columns[:-1], size=5, replace=False):  # Solo 5 columnas afectadas
        df.loc[anomaly_indices, col] += np.random.choice([-10, 10], size=n_anomalies)  # Grandes valores anómalos

    # Asignar etiqueta 'Anomaly'
    df.loc[anomaly_indices, 'Etiqueta'] = 'Anomaly'

    # Insertar columna ID
    df.insert(0, 'ID', np.arange(n_samples))

    return df


import numpy as np
import pandas as pd
from scipy.stats import normaltest

def generate_normal_dataset(n_samples=50000, n_features=27, anomaly_ratio=0.005, random_state=42):
    """
    Genera un dataset con una distribución lo más normal posible para evaluación con Z-score.
    """
    np.random.seed(random_state)

    # Generar datos estrictamente normales con dispersión mínima
    data = np.random.normal(loc=0, scale=0.2, size=(n_samples, n_features))

    # Crear DataFrame
    df = pd.DataFrame(data, columns=[f'Caracteristica_{i+1}' for i in range(n_features)])

    # Etiquetas iniciales: todas normales
    df['Etiqueta'] = 'Normal'

    # Determinar cuántas anomalías crear
    n_anomalies = int(n_samples * anomaly_ratio)
    anomaly_indices = np.random.choice(df.index, size=n_anomalies, replace=False)

    # Introducir anomalías controladas (solo el 5% de las columnas afectadas)
    anomalous_columns = np.random.choice(df.columns[:-1], size=int(n_features * 0.05), replace=False)
    for col in anomalous_columns:
        df.loc[anomaly_indices, col] += np.random.normal(loc=0, scale=0.3, size=n_anomalies)

    # Asignar etiqueta 'Anomaly' a los índices seleccionados
    df.loc[anomaly_indices, 'Etiqueta'] = 'Anomaly'

    # Insertar columna ID
    df.insert(0, 'ID', np.arange(n_samples))

    # Filtrar columnas no normales y regenerar
    df = filter_non_normal_columns(df)

    return df

def filter_non_normal_columns(df):
    """
    Filtra y ajusta columnas que no cumplen con la normalidad.
    """
    for col in df.columns[1:-1]:  # Excluye ID y Etiqueta
        p_value = normaltest(df[col]).pvalue
        if p_value <= 0.05:  # Si no cumple la normalidad
            # Regenerar columna con distribución estrictamente normal
            df[col] = np.random.normal(loc=0, scale=0.2, size=len(df))
    return df

def validate_distribution(df):
    """
    Valida la distribución normal de las características en un DataFrame.
    """
    # Evaluar normalidad en las características (excluyendo las columnas 'ID' y 'Etiqueta')
    p_values = df.iloc[:, 1:-1].apply(lambda col: normaltest(col).pvalue)
    proporcion_normal = (p_values > 0.05).mean()
    print(f"Proporción de características normales: {proporcion_normal:.2%}")
    return proporcion_normal

# Prueba del dataset ajustado
#df = generate_normal_dataset()
#validate_distribution(df)


def generate_dense_dataset(n_samples=10000, n_features=27, random_state=42):
    """
    Genera un dataset con alta densidad para evaluación con DBSCAN.
    """
    from sklearn.datasets import make_blobs

    # Generar datos densos con múltiples clusters compactos
    X, y = make_blobs(
        n_samples=n_samples,
        centers=15,                # Más clusters para mayor densidad global
        n_features=n_features,
        cluster_std=1.5,           # Baja desviación estándar para clusters más compactos
        random_state=random_state
    )

    # Crear DataFrame
    df = pd.DataFrame(X, columns=[f'Caracteristica_{i+1}' for i in range(n_features)])
    
    # Etiquetas: asignar 'Anomaly' aleatoriamente a una pequeña fracción
    df['Etiqueta'] = np.random.choice(['Normal', 'Anomaly'], size=n_samples, p=[0.95, 0.05])

    # Insertar columna ID
    df.insert(0, 'ID', np.arange(len(df)))

    return df



def generate_advanced_dataset(n_samples=50000, n_features=100, anomaly_ratio=0.05, random_state=42):
    np.random.seed(random_state)
    n_anomalies = int(n_samples * anomaly_ratio)
    n_normals = n_samples - n_anomalies

    normal_data = np.random.normal(loc=0, scale=1, size=(n_normals, n_features))
    anomaly_data = np.random.normal(loc=3, scale=1.5, size=(n_anomalies, n_features))
    
    # Añadir interacciones no lineales en anomalías
    anomaly_data[:, :10] = np.power(anomaly_data[:, :10], 2)
    anomaly_data[:, 10:20] += 5 * np.sin(anomaly_data[:, 10:20])

    # Modificar distribución de las primeras características
    var_multiplier = np.linspace(5.0, 20.0, 15)
    for i in range(15):
        normal_data[:, i] *= var_multiplier[i]
        anomaly_data[:, i] *= var_multiplier[i]

    # Combinar datos y mezclar
    X = np.vstack((normal_data, anomaly_data))
    y = np.array(['Normal'] * n_normals + ['Anomaly'] * n_anomalies)
    shuffle_indices = np.random.permutation(n_samples)
    X = X[shuffle_indices]
    y = y[shuffle_indices]

    # Crear DataFrame
    df = pd.DataFrame(X, columns=[f'Feature_{i+1}' for i in range(n_features)])
    df['Label'] = y
    df.insert(0, 'ID', np.arange(n_samples))  # Agregar columna de IDs
    return df


# Generar datasets
#df_normal = generate_enhanced_dataset()
#df_dense = generate_dense_dataset()
df_high_dim = generate_advanced_dataset()

# Guardar datasets en CSV
#df_normal.to_csv('dataset_normal.csv', index=False)
#df_dense.to_csv('dataset_denso.csv', index=False)
df_high_dim.to_csv('dataset_alta_dimensionalidad.csv', index=False)

print("Todos los datasets generados y guardados con éxito.")

# Generar el dataset
#df = generate_anomaly_dataset(n_samples=50000, n_features=27, anomaly_ratio=0.05, random_state=42)

# Guardar en formato CSV
#df.to_csv('datos_sinteticos_mejorado.csv', index=False)
#print("Dataset mejorado con columna ID generado con éxito.")

