import numpy as np


def preprocess_data(df, columns_to_drop):
    """
    Preprocesa el DataFrame eliminando columnas específicas y aquellas con valores no numéricos.
    """
    # Eliminar las columnas definidas explícitamente
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Eliminar columnas no numéricas
    df = df.select_dtypes(include=['number'])

    # Llenar valores nulos con 0
    df = df.fillna(0)

    return df


def postprocess_data(df, removed_columns, default_values=None):
    """
    Postprocesa el DataFrame devolviendo las columnas eliminadas.
    
    :param df: DataFrame procesado (sin las columnas eliminadas).
    :param removed_columns: Lista de nombres de columnas eliminadas.
    :param default_values: Diccionario opcional que define los valores por defecto para las columnas eliminadas.
    :return: DataFrame con las columnas restauradas.
    """
    if default_values is None:
        # Si no se especifican valores por defecto, usar NaN
        default_values = {col: np.nan for col in removed_columns}

    # Agregar columnas eliminadas con los valores por defecto
    for col in removed_columns:
        if col not in df.columns:
            df[col] = default_values.get(col, np.nan)

    return df


