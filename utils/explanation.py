import pandas as pd
import numpy as np

def generate_rules(data_with_anomalies, output_path="anomaly_rules.txt"):
    """
    Genera reglas basadas en las anomalías detectadas.

    :param data_with_anomalies: DataFrame que incluye las anomalías detectadas y la columna 'anomaly'.
    :param output_path: Ruta del archivo donde se guardarán las reglas.
    :return: Lista de reglas generadas.
    """
    print("Generando reglas para las anomalías...")

    # Filtrar solo las filas marcadas como 'Anomaly'
    anomalies = data_with_anomalies[data_with_anomalies['anomaly'] == "Anomaly"]

    # Calcular estadísticas básicas para las columnas del DataFrame procesado
    print("Calculando estadísticas básicas para las columnas...")
    stats = data_with_anomalies.describe()
    print("Estadísticas calculadas:", stats)

    rules = []

    # Iterar sobre las filas anómalas
    for index, row in anomalies.iterrows():
        print(f"Generando regla para la anomalía en la fila {index}...")
        rule_conditions = []

        for col in data_with_anomalies.columns:
            if col in ["anomaly", "anomaly_score"]:  # Ignorar columnas de metadata
                continue

            value = row[col]
            min_val = stats.at["min", col]
            max_val = stats.at["max", col]
            q1 = stats.at["25%", col]
            q3 = stats.at["75%", col]
            iqr = q3 - q1  # Rango intercuartílico
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Crear condiciones de la regla basadas en rangos
            if value < lower_bound:
                rule_conditions.append(f"{col} < {lower_bound:.2f}")
            elif value > upper_bound:
                rule_conditions.append(f"{col} > {upper_bound:.2f}")

        if rule_conditions:
            rule = f"Si {' y '.join(rule_conditions)}, entonces instancia {index} es anómala."
            rules.append(rule)

    # Guardar las reglas en un archivo de texto
    with open(output_path, "w") as file:
        for rule in rules:
            file.write(rule + "\n")

    print(f"Reglas guardadas en: {output_path}")
    