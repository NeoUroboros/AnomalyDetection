**Isolation Forest** es un algoritmo de aprendizaje automático no supervisado diseñado específicamente para la detección de anomalías. La idea principal detrás de Isolation Forest es que las anomalías son observaciones que están aisladas o separadas del resto de los datos, lo que las hace más fáciles de identificar. En términos sencillos, el algoritmo intenta "aislar" estos puntos mediante la creación de particiones o cortes en el conjunto de datos.

### Principios Fundamentales de Isolation Forest

1. **Aislamiento por partición**:
   El algoritmo utiliza árboles de decisión para dividir los datos en subgrupos. Los puntos que son anomalías (outliers) suelen necesitar menos cortes (particiones) para ser aislados. Esto se debe a que están más alejados del resto de los datos, lo que significa que se pueden separar rápidamente.

2. **Aleatoriedad**:
   Al construir el bosque de árboles, Isolation Forest selecciona aleatoriamente una característica (una dimensión del conjunto de datos) y luego selecciona un valor dentro del rango de esa característica para dividir el conjunto de datos. Este proceso se repite varias veces hasta que los puntos quedan aislados en nodos hoja.

3. **Profundidad del árbol**:
   El número de particiones necesarias para aislar un punto (la profundidad del árbol) nos da una medida de si es una anomalía o no. Las observaciones normales requerirán más particiones para ser aisladas, mientras que las observaciones anómalas serán aisladas más rápidamente, es decir, con menos particiones.

4. **Bosque de árboles**:
   Isolation Forest utiliza un conjunto (o bosque) de muchos árboles de aislamiento para promediar el número de particiones necesarias para aislar cada observación. Al combinar la información de varios árboles, se mejora la robustez del modelo y se reduce la variabilidad en las decisiones.

### Funcionamiento del Algoritmo

1. **Construcción del bosque**:
   - Se generan varios árboles de aislamiento, donde cada árbol es construido tomando una muestra aleatoria de los datos de entrenamiento.

   - En cada nodo del árbol, se selecciona aleatoriamente una característica (columna del dataset) y un valor de corte aleatorio dentro del rango de esa característica.

   - Los puntos se dividen en dos ramas: los que están por debajo del valor de corte y los que están por encima.

2. **Cálculo del puntaje de anomalía**:
   - El puntaje de anomalía de un punto se calcula basado en la longitud del camino desde la raíz hasta el nodo hoja en el que queda aislado.

   - Los puntos que requieren menos particiones (es decir, tienen caminos más cortos) se consideran más anómalos. Esto se debe a que las anomalías suelen estar dispersas y, por lo tanto, se aíslan rápidamente.

   - Los puntos normales, que están más agrupados, requerirán más divisiones (caminos más largos) para quedar aislados.

3. **Interpreción del puntaje**:
   - El puntaje de anomalía varía entre 0 y 1.
   - Un puntaje cercano a 1 indica una alta probabilidad de que el punto sea una anomalía.
   - Un puntaje cercano a 0 indica que el punto es normal.
   - Los puntos con un valor mayor a un umbral (generalmente cerca de 0.5) son considerados como anomalías.

### Implementación de Isolation Forest en Python

Ahora, vamos a ver cómo se implementa **Isolation Forest** en Python utilizando la biblioteca **scikit-learn**.

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Crear un conjunto de datos de ejemplo
data = {
    'feature1': [10, 12, 14, 13, 15, 120, 11, 13, 12, 14],
    'feature2': [9, 11, 12, 10, 13, 130, 10, 11, 13, 12]
}
df = pd.DataFrame(data)

# Inicializar Isolation Forest
iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

# Ajustar el modelo a los datos
iso_forest.fit(df)

# Predecir anomalías
df['anomaly'] = iso_forest.predict(df[['feature1', 'feature2']])

# Isolation Forest devuelve -1 para anomalías, 1 para puntos normales
df['anomaly_label'] = df['anomaly'].apply(lambda x: 'Anomalía' if x == -1 else 'Normal')

print(df)
```

### Parámetros Importantes en Isolation Forest

1. **`n_estimators`**:
   Este parámetro define cuántos árboles de aislamiento se crearán en el bosque. Un mayor número de árboles puede aumentar la precisión del modelo, pero también incrementa el costo computacional.

2. **`contamination`**:
   Es la proporción de puntos que se esperan como anomalías en el conjunto de datos. El valor predeterminado es `auto`, pero a menudo se especifica manualmente. Si sabes que aproximadamente el 5% de los datos son anomalías, puedes establecer `contamination=0.05`.

3. **`max_samples`**:
   Es el número máximo de muestras que se utilizarán para entrenar cada árbol. Si no se especifica, utiliza el número de muestras en el conjunto de datos. Este parámetro es importante para el rendimiento en conjuntos de datos grandes, ya que permite usar una muestra aleatoria para construir cada árbol.

4. **`random_state`**:
   Controla la aleatoriedad del modelo. Si se establece este valor, los resultados serán reproducibles.

### Ventajas de Isolation Forest

1. **Escalabilidad**:
   Isolation Forest es altamente escalable y eficiente, ya que funciona bien incluso con grandes volúmenes de datos. Al usar una muestra aleatoria de datos y un número limitado de árboles, reduce el costo computacional.

2. **No hace suposiciones de distribución**:
   A diferencia de métodos estadísticos como Z-score, Isolation Forest no asume que los datos sigan una distribución normal o específica. Es adecuado para detectar anomalías en conjuntos de datos de alta dimensionalidad.

3. **Capacidad para detectar anomalías multivariadas**:
   Isolation Forest puede detectar anomalías en conjuntos de datos con múltiples características, mientras que algunos métodos como el IQR o Z-score son principalmente univariados.

4. **Robustez frente a datos ruidosos**:
   Debido a su enfoque basado en aislamiento, puede ser menos sensible al ruido en los datos en comparación con otros métodos.

### Limitaciones de Isolation Forest

1. **Contaminación del dataset**:
   El parámetro `contamination` debe definirse con precaución. Si se elige incorrectamente, el modelo podría etiquetar demasiados puntos como anomalías o pasar por alto algunas anomalías
   reales.

2. **Outliers sutiles**:
   Aunque Isolation Forest es efectivo en encontrar outliers evidentes, podría tener dificultades para detectar anomalías sutiles que no están tan alejadas de la distribución normal.

### Conclusión

Isolation Forest es una herramienta poderosa para la detección de anomalías, especialmente cuando se trabaja con conjuntos de datos grandes y multivariados. Su enfoque basado en la idea de
aislamiento lo hace único y eficiente para identificar puntos de datos que se comportan de manera diferente al resto. Además, es flexible en cuanto a las distribuciones de los datos y tiene una implementación fácil en Python con **scikit-learn**.

Funciona de la sgte manera, al conjunto de datos se le pica usando un valor X de una columna Y, se divide en los que son mayores y menores, se vuelve a aplicar el mismo proceso con otra columna, hasta aislarlos todos o en su defecto llegar a un maximo de profundidad. Se realizan varios arboles para de esta forma conformar el bosque de aislamiento, luego se comparan entre ellos, usando el promedio para determinar que fila puede ser catalogada como anomalia.