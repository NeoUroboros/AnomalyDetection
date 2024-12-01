### **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**

DBSCAN es un algoritmo de agrupamiento basado en densidad, que puede ser utilizado también para la detección de anomalías. A diferencia de métodos como **K-means**, que requieren especificar el número de clusters, DBSCAN no requiere que se defina este parámetro de antemano. En lugar de eso, DBSCAN detecta los clusters basándose en la densidad de los puntos.

### **Principios Fundamentales de DBSCAN**

1. **Puntos centrales y vecinos**: DBSCAN clasifica los puntos en tres categorías:
    
    - **Puntos centrales**: Son puntos que tienen suficientes vecinos cercanos (definidos por un parámetro `min_samples`).
    - **Puntos de borde**: Son puntos que están en el borde de un cluster pero no tienen suficientes vecinos cercanos para ser considerados como puntos centrales.
    - **Ruido o anomalías**: Son puntos que no tienen suficientes vecinos cercanos y no pertenecen a ningún cluster.
2. **Radio de vecindad**: El parámetro `eps` (epsilon) define el radio dentro del cual se buscarán vecinos cercanos.
    
3. **Algoritmo de agrupamiento**:
    
    - DBSCAN empieza con un punto arbitrario no visitado.
    - Se busca un conjunto de vecinos dentro del radio `eps`.
    - Si el punto tiene suficientes vecinos (al menos `min_samples`), se marca como punto central y se forma un cluster.
    - Si un punto tiene menos vecinos de los necesarios, se clasifica como ruido o anomalía.

### **Funcionamiento de DBSCAN para Detección de Anomalías**

En este caso, vamos a usar DBSCAN para la detección de anomalías. Los puntos que son clasificados como **ruido** (código `-1` de DBSCAN) se consideran **anomalías**, mientras que los puntos clasificados en clusters se consideran normales.

### **Implementación de DBSCAN para Detección de Anomalías en Python**

A continuación te dejo una implementación similar a la de Isolation Forest, pero utilizando DBSCAN:

```python
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Crear un conjunto de datos de ejemplo
data = {
    'feature1': [10, 12, 14, 13, 15, 120, 11, 13, 12, 14],
    'feature2': [9, 11, 12, 10, 13, 130, 10, 11, 13, 12]
}
df = pd.DataFrame(data)

# Normalizar los datos antes de aplicar DBSCAN
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Inicializar DBSCAN
dbscan = DBSCAN(eps=3, min_samples=2)

# Ajustar el modelo y predecir las anomalías
labels = dbscan.fit_predict(df_scaled)

# Agregar los resultados al DataFrame
df['anomaly'] = labels
df['anomaly_label'] = df['anomaly'].apply(lambda x: 'Anomalía' if x == -1 else 'Normal')

print(df)
```

### **Explicación del Código:**

1. **Normalización de datos**:
    
    - Antes de aplicar DBSCAN, es importante normalizar los datos. Esto se realiza usando `StandardScaler()`, ya que DBSCAN es sensible a las escalas de las características.
2. **Inicialización de DBSCAN**:
    
    - `eps` es el radio de vecindad. Los puntos que se encuentren dentro de este radio se consideran vecinos.
    - `min_samples` es el número mínimo de puntos requeridos para formar un cluster.
3. **Ajuste y Predicción**:
    
    - `dbscan.fit_predict(df_scaled)` ajusta el modelo a los datos normalizados y predice el label de cada punto.
    - Los puntos clasificados como `-1` se consideran anomalías (ruido).
4. **Resultado**:
    
    - Se añade una columna `anomaly_label` al DataFrame que indica si un punto es una anomalía o no, basándose en la predicción de DBSCAN.

### **Parámetros Importantes de DBSCAN:**

1. **`eps`**: Define el radio de vecindad para encontrar los vecinos de un punto. Si el valor de `eps` es demasiado pequeño, no se formarán clusters, y si es demasiado grande, todo el conjunto de datos podría ser considerado un solo cluster.
    
2. **`min_samples`**: Es el número mínimo de puntos necesarios para formar un cluster. Un valor pequeño de `min_samples` puede resultar en clusters más grandes y menos puntos considerados anomalías.
    
3. **`metric`**: Define la métrica utilizada para calcular la distancia entre puntos. Por defecto, se utiliza la distancia euclidiana, pero puede modificarse para utilizar otras métricas.
    

### **Ventajas de DBSCAN en Detección de Anomalías:**

1. **No requiere predefinir el número de clusters**: A diferencia de algoritmos como K-means, DBSCAN no requiere especificar cuántos clusters esperamos encontrar.
2. **Capaz de encontrar anomalías de forma natural**: Los puntos que no pertenecen a ningún cluster (ruido) son automáticamente considerados anomalías.
3. **No asume una distribución particular de los datos**: Funciona bien con datos que no siguen distribuciones específicas, como las distribuciones normales.

### **Limitaciones de DBSCAN:**

1. **Sensibilidad a los parámetros `eps` y `min_samples`**: Elegir los parámetros adecuados puede ser desafiante, ya que pequeños cambios en los valores pueden tener un gran impacto en los resultados.
2. **Dificultades con datos de alta dimensionalidad**: DBSCAN puede tener problemas para identificar clusters en datos de alta dimensión debido a la "maldita" maldición de la dimensionalidad.

### **Conclusión:**

DBSCAN es un algoritmo potente para la detección de anomalías, especialmente cuando los datos tienen una estructura de densidad variada. Su capacidad para detectar anomalías sin requerir un número predefinido de clusters lo convierte en una opción versátil para este tipo de tareas. Sin embargo, es crucial elegir los parámetros `eps` y `min_samples` adecuados para obtener buenos resultados.