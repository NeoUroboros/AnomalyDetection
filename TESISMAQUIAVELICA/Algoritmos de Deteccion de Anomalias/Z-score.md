### **Z-Score**: Detección de anomalías basada en estadísticas

El **Z-score** es un enfoque estadístico simple y efectivo para detectar anomalías en datos univariados o multivariados. La idea central es medir cuán lejos está un punto de datos del promedio del conjunto en términos de desviaciones estándar. Es ideal para datos que siguen una distribución aproximadamente normal.

---

### **Principios Fundamentales del Z-Score**

1. **Definición matemática del Z-score**: Para un punto x, el Z-score se calcula como:
    ![[Pasted image 20241129184938.png]]
    Donde:
    
    - x: El valor de un punto de datos.
    - μ: La media del conjunto de datos.
    - σ: La desviación estándar del conjunto de datos.
    
    El Z-score mide el número de desviaciones estándar que x está por encima o por debajo de la media.
    
2. **Umbrales de anomalía**:
    
    - Valores con un Z-score mayor (en magnitud) a un umbral, como |Z| > 3, son considerados anomalías.
    
    - Este umbral se basa en las propiedades de la **distribución normal**:
        - El 68% de los datos cae dentro de ±1σ.
        - El 95% dentro de ±2σ.
        - El 99.7% dentro de ±3σ.
3. **Suposición de normalidad**: El Z-score funciona mejor cuando los datos tienen una distribución normal. Si los datos no son normales, los resultados pueden ser menos fiables.

### **Distribución Normal**

La **distribución normal**, también conocida como **distribución de Gauss** o **campana de Gauss**, es una de las distribuciones de probabilidad más importantes en estadística. Es ampliamente utilizada porque muchos fenómenos naturales y sociales tienden a seguir este patrón.

---

### **Características Clave de una Distribución Normal**

1. **Forma de campana simétrica**:
    
    - La gráfica de la distribución tiene forma de campana y es perfectamente simétrica respecto a su media.
    - Esto significa que los datos están distribuidos de manera uniforme alrededor de la media.
2. **Media, mediana y moda iguales**:
    - En una distribución normal, estos tres valores coinciden y se encuentran en el centro de la curva.
3. **Desviación estándar y dispersión**:
    
    - La dispersión de los datos está determinada por la **desviación estándar** (σ).
    - Aproximadamente:
        - El 68% de los datos está dentro de ±1σ
        - El 95% de los datos está dentro de ±2σ
        - El 99.7% de los datos está dentro de ±3σ
4. **Función de densidad de probabilidad (PDF)**: La fórmula matemática para la distribución normal es:
    
    ![[Pasted image 20241129190411.png]]
    
    Donde:
    
    - xx: El valor de la variable aleatoria.
    - μ: La media (centro de la distribución).
    - σ: La desviación estándar (ancho de la distribución).
    - e: La base del logaritmo natural.
5. **Colas infinitas**:
    
    - La curva se extiende hacia ambos lados indefinidamente, pero con probabilidades cada vez más pequeñas.

---

### **Ejemplo de Fenómenos que Siguen una Distribución Normal**

1. **Alturas de personas**:
    
    - Si mides la altura de un gran número de personas, la mayoría estará cerca de la media, con pocas personas siendo mucho más altas o mucho más bajas.
2. **Errores de medición**:
    
    - Los errores en instrumentos de medición precisos suelen distribuirse de forma normal.
3. **Notas de exámenes estandarizados**:
    
    - En muchos casos, las calificaciones de pruebas como SAT o IQ tienden a seguir una distribución normal.
---

### **Funcionamiento del Z-Score**

1. **Cálculo de métricas estadísticas**:
    
    - Se calcula la **media** (μ\mu) y la **desviación estándar** (σ\sigma) para el conjunto de datos.
    - Esto se hace generalmente de forma independiente para cada columna si se analizan varias características.
2. **Transformación a Z-scores**:
    
    - Cada punto del conjunto de datos se transforma utilizando la fórmula del Z-score.
    - Esto normaliza los datos para que tengan una media de 0 y una desviación estándar de 1.
3. **Identificación de anomalías**:
    
    - Los puntos con ∣Z∣| mayor que el umbral definido (por ejemplo, 3) se etiquetan como anomalías.
    - En datos multivariados, se puede calcular un Z-score por cada columna o una métrica combinada.

---

### **Implementación en Python**

A continuación, se muestra cómo calcular el Z-score para detectar anomalías en un conjunto de datos:

```python
import numpy as np
import pandas as pd

# Crear un conjunto de datos de ejemplo
data = {'feature1': [10, 12, 14, 13, 15, 120, 11, 13, 12, 14],
        'feature2': [9, 11, 12, 10, 13, 130, 10, 11, 13, 12]}
df = pd.DataFrame(data)

# Calcular la media y la desviación estándar para cada columna
mean = df.mean()
std_dev = df.std()

# Calcular el Z-score para cada valor
z_scores = (df - mean) / std_dev

# Definir un umbral para identificar anomalías (por ejemplo, 3)
threshold = 3
df['anomaly'] = (z_scores.abs() > threshold).any(axis=1)

# Etiquetar las anomalías
df['anomaly_label'] = df['anomaly'].apply(lambda x: 'Anomalía' if x else 'Normal')

print(df)
```

---

### **Ventajas del Z-Score**

1. **Simplicidad**:
    - Fácil de calcular y de interpretar.
    - No requiere parámetros complejos ni entrenamiento.
2. **Rapidez**:
    - Es computacionalmente eficiente y puede aplicarse incluso a conjuntos de datos grandes.
3. **Escalabilidad**:
    - Funciona bien para datos univariados y puede extenderse a datos multivariados calculando Z-scores para cada característica.
4. **Interpretabilidad**:
    - Los valores de Z-score son intuitivos: indican cuán lejos está un punto del promedio.

---

### **Limitaciones del Z-Score**

1. **Dependencia de la distribución normal**:
    - Asume que los datos tienen una distribución aproximadamente normal. Si los datos están sesgados o tienen distribuciones no normales, los Z-scores pueden no ser útiles.

1. **Sensibilidad a valores extremos**:
    - Las anomalías influyen en el cálculo de μ\mu y σ\sigma, lo que puede distorsionar los resultados. En estos casos, el uso de **estadísticas robustas** (como la mediana y la desviación absoluta mediana, MAD) es preferible.
3. **Limitado a relaciones lineales**:
    - No considera correlaciones no lineales entre características en datos multivariados.

---
### **Conclusión**

El Z-score es una técnica rápida, sencilla e intuitiva para la detección de anomalías en datos de baja complejidad y con distribuciones normales. Si los datos presentan características más complejas, como correlaciones no lineales o distribuciones no normales, es mejor considerar algoritmos más avanzados como Isolation Forest o Autoencoders. Sin embargo, su bajo costo computacional lo hace ideal para sistemas en tiempo real o escenarios donde la simplicidad y velocidad son prioritarias.

El valor de Z (también llamado _Z-score_) es el resultado del cálculo para cada dato en función de la fórmula:

![[Pasted image 20241129184938.png]]

Donde:

- xx: el valor individual que estamos evaluando.
- μ\mu: la media de todos los datos en la columna.
- σ\sigma: la desviación estándar de los datos en la columna.

El resultado de ZZ nos dice cuántas desviaciones estándar (σ\sigma) está un valor (xx) por encima o por debajo de la media (μ\mu).

---

### **Interpretación de Z:**

1. Si Z>0, el valor xx está **por encima de la media**.
2. Si Z<0, el valor xx está **por debajo de la media**.
3. Cuanto mayor es el valor absoluto de Z (es decir, ∣Z∣), más lejos está x de la media.


El código que compartiste parece ser parte de una implementación en Python para decidir si los datos en un DataFrame siguen una **distribución normal**, y dependiendo de ese análisis, seleccionar una estrategia específica (`ZScoreStrategy`) para el procesamiento posterior. Vamos a desglosarlo:

---

### **1. ¿Qué hace esta función?**

La función `check_distribution` realiza las siguientes tareas:

1. **Muestra una parte de los datos**:
    
    - Toma un subconjunto aleatorio de los datos, con un límite de 5000 filas, para realizar pruebas estadísticas. Esto reduce el tiempo de cómputo al trabajar con datasets grandes.
2. **Realiza una prueba de normalidad**:
    
    - Aplica la función `normaltest` de `scipy.stats` a cada columna de datos seleccionada.
    - Extrae los **p-valores** de cada columna.
3. **Evalúa los p-valores**:
    
    - Si todas las columnas tienen un **p-valor mayor que 0.05**, asume que los datos en esas columnas siguen una **distribución normal** y devuelve una instancia de `ZScoreStrategy`.
4. **Decisión final**:
    
    - Si alguna columna tiene un **p-valor menor o igual a 0.05**, la función concluye que los datos no son normalmente distribuidos y retorna `None`.

---

### **2. Detalle de cada línea**

#### **Línea 2: Muestra aleatoria**

```python
sampled_data = self.data.sample(min(5000, len(self.data)))
```

- Usa el método `sample` del DataFrame para seleccionar un subconjunto aleatorio de filas.
- Si el DataFrame tiene más de 5000 filas, toma 5000 como límite. Si tiene menos, toma todas las filas.

Esto es útil para reducir la complejidad en datasets muy grandes.

---

#### **Línea 4: Aplicación del `normaltest`**

```python
p_values = sampled_data.apply(normaltest, axis=0).iloc[1]
```

- Aplica la prueba `normaltest` (de `scipy.stats`) a cada columna de datos (se asume que las columnas contienen variables numéricas).
- `normaltest` evalúa si los datos siguen una distribución normal, devolviendo dos valores:
    1. El estadístico de la prueba.
    2. El **p-valor** asociado.

Aquí, el método extrae los p-valores (`iloc[1]`), que serán usados para determinar la normalidad.

---

#### **Línea 6: Evaluación de p-valores**

```python
if (p_values > 0.05).all():
```

- Verifica si **todas las columnas** tienen un p-valor mayor a 0.05:
    - Si es así, no hay evidencia suficiente para rechazar la hipótesis nula de que los datos siguen una distribución normal.
    - Esto indica que **todas las columnas probablemente siguen una distribución normal**.

---

#### **Línea 7: Retorno condicional**

```python
return ZScoreStrategy()
```

- Si los datos siguen una distribución normal, devuelve una instancia de `ZScoreStrategy`. Esto sugiere que esta estrategia está diseñada para trabajar con datos normales, probablemente usando scores Z para detectar anomalías.

```python
return None
```

- Si alguna columna no sigue una distribución normal, retorna `None`, indicando que no se aplicará esta estrategia.

---

### **3. Contexto de la función `normaltest`**

La función `normaltest` combina dos pruebas estadísticas:

- **D’Agostino and Pearson’s test**, que mide:
    - Asimetría (skewness).
    - Curtosis (kurtosis).

Esta combinación es útil para detectar desviaciones significativas de la normalidad.

El p-valor resultante indica:

- **p > 0.05**: Los datos son consistentes con una distribución normal.
- **p ≤ 0.05**: Los datos no siguen una distribución normal.

---

### **4. Aplicación Práctica**

Este enfoque es común en la **detección de anomalías** o en pipelines de datos donde:

- Primero verificas si los datos son normales.
- Si son normales, puedes usar técnicas que asumen normalidad, como scores Z.
- Si no, debes buscar otras estrategias, como Isolation Forest o análisis basados en distribuciones no paramétricas.

---
El **p-valor** no es exactamente una herramienta para calcular la distribución normal, sino una medida estadística que se usa para evaluar la significancia de un resultado frente a una hipótesis nula. Sin embargo, está relacionado con la distribución normal en muchos contextos, especialmente cuando se trabaja con pruebas de hipótesis basadas en datos distribuidos normalmente.

Aquí te explico la relación y el porqué se usa:

---

### **¿Qué es el p-valor?**

El p-valor es la probabilidad de obtener un resultado tan extremo como el observado, o más extremo, bajo la suposición de que la hipótesis nula es verdadera.

Por ejemplo:

- Si estás evaluando si un sistema está funcionando de manera normal (hipótesis nula: no hay anomalías), el p-valor te dice cuán probable es observar el comportamiento actual asumiendo que el sistema efectivamente funciona de forma normal.

---

### **Relación con la Distribución Normal**

En muchas pruebas estadísticas (como la t de Student, z-test o ANOVA), el cálculo del p-valor se basa en una distribución de referencia, que comúnmente es la **distribución normal**. Esto se debe a que, según el **teorema del límite central**, las medias muestrales tienden a seguir una distribución normal cuando el tamaño de la muestra es grande, independientemente de cómo esté distribuida la población original.

Por ejemplo:

1. **Transformación Z**: Si tienes una variable XX con media μ\mu y desviación estándar σ\sigma, puedes estandarizarla con:
    
    Z=X−μσZ = \frac{X - \mu}{\sigma}
    
    El valor de ZZ se compara con la distribución normal estándar (media 0, desviación estándar 1) para calcular un p-valor.
    
2. **Distribución Normal Acumulativa**: El p-valor se obtiene generalmente usando la función acumulativa (CDF) de la distribución normal:
    
    p=P(Z>zobservado)p = P(Z > z_{\text{observado}})
    
    Donde zobservadoz_{\text{observado}} es el valor estandarizado de tu estadístico.
    

---

### **¿Qué tiene que ver con la detección de anomalías?**

En la detección de anomalías, a menudo asumes que los datos normales siguen una distribución conocida (por ejemplo, normal). Entonces:

- Calculas una métrica (como un score Z o una distancia).
- Evaluas qué tan probable es ese valor bajo la distribución normal asumida.
- Si el p-valor es muy bajo, concluyes que es poco probable que el dato provenga de esa distribución, marcándolo como una **anomalía**.

---

### **¿Se puede calcular la distribución normal con el p-valor?**

No exactamente. El p-valor **no calcula** la distribución normal, sino que **usa** la distribución normal (o cualquier otra distribución de referencia) para medir probabilidades. Si lo que necesitas es generar o ajustar una distribución normal a tus datos, eso requiere otros métodos como estimación de parámetros (μ\mu y σ\sigma) usando la media y la desviación estándar.
