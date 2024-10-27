import pandas as pd


def preprocess_data(df, columns):
    # Eliminar columnas específicas y manejar valores NaN
    for column in columns:
        df = df.drop(columns=[column], errors='ignore')
    df = df.fillna(0)
    return df


def postprocess_data(df, columns):
    # Reasignar las columnas faltantes
    pass

