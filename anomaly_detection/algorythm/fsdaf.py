import pandas as pd
import numpy as np

# Generar un rango de fechas con milisegundos
dates = pd.date_range(start="2023-11-14 17:11:58", periods=10000, freq="L")  # 'L' es para milisegundos

# Generar valores aleatorios para 'y'
y_values = np.random.randint(0, 100, size=10000)

# Crear el DataFrame
data = pd.DataFrame({
    'ds': dates,
    'y': y_values
})

# Guardar el DataFrame en un archivo CSV
data.to_csv('data.csv', index=False)

# Imprimir mensaje de confirmación
print("El archivo 'data.csv' ha sido guardado exitosamente.")
