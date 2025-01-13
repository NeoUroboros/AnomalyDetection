import pandas as pd
import numpy as np

def generate_rules(data_with_anomalies, output_path="anomaly_rules.txt"):
    """
    Genera reglas basadas en las anomalías detectadas, evitando duplicados y sin mencionar instancias específicas.

    :param data_with_anomalies: DataFrame que incluye las anomalías detectadas y la columna 'anomaly'.
    :param output_path: Ruta del archivo donde se guardarán las reglas.
    :return: Lista de reglas generadas (sin duplicados).
    """
    print("Generando reglas para las anomalías...")

    # Verifica si el DataFrame está vacío
    if data_with_anomalies.empty:
        print("El DataFrame está vacío. No se generarán reglas.")
        return []

    # Filtrar solo las filas marcadas como 'Anomaly'
    if 'anomaly' not in data_with_anomalies.columns:
        raise ValueError("El DataFrame no contiene una columna 'anomaly'.")

    anomalies = data_with_anomalies[data_with_anomalies['anomaly'] == "Anomaly"]
    if anomalies.empty:
        print("No se encontraron filas marcadas como 'Anomaly'.")
        return []

    print(f"Total de anomalías detectadas: {len(anomalies)}")

    # Calcular estadísticas básicas para las columnas del DataFrame procesado
    stats = data_with_anomalies.describe()
    print("Estadísticas del DataFrame:\n", stats)

    rules_set = set()  # Usamos un conjunto para evitar duplicados

    # Iterar sobre las filas anómalas
    for _, row in anomalies.iterrows():
        rule_conditions = []
        seen_conditions = set()  # Para evitar condiciones repetidas en una misma regla

        for col in data_with_anomalies.columns:
            if col in ["anomaly", "anomaly_score"]:  # Ignorar columnas de metadata
                continue

            if col not in stats.columns:  # Asegurar que las estadísticas existen
                print(f"Columna '{col}' no tiene estadísticas disponibles.")
                continue

            value = row[col]
            q1 = stats.at["25%", col]
            q3 = stats.at["75%", col]
            iqr = q3 - q1  # Rango intercuartílico
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Crear condiciones de la regla basadas en rangos
            if value < lower_bound and f"{col} < {lower_bound:.2f}" not in seen_conditions:
                rule_conditions.append(f"{col} < {lower_bound:.2f}")
                seen_conditions.add(f"{col} < {lower_bound:.2f}")
            elif value > upper_bound and f"{col} > {upper_bound:.2f}" not in seen_conditions:
                rule_conditions.append(f"{col} > {upper_bound:.2f}")
                seen_conditions.add(f"{col} > {upper_bound:.2f}")

        if rule_conditions:
            # Crear una regla genérica sin mencionar instancias
            rule = f"Si {' y '.join(rule_conditions)}, entonces es anómala."
            rules_set.add(rule)  # Agregar la regla al conjunto

    # Convertir el conjunto a una lista para retornar
    rules = list(rules_set)

    # Guardar las reglas en un archivo de texto
    try:
        with open(output_path, "w") as file:
            for rule in rules:
                file.write(rule + "\n")
        print(f"Reglas guardadas en: {output_path}")
    except Exception as e:
        print(f"Error al guardar reglas: {e}")

    return rules
