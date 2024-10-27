import pandas as pd


def preprocess_data(df):
    # Eliminar columnas específicas y manejar valores NaN
    df = df.drop(columns=["Column1.created_date", "Column1.id"], errors='ignore')
    df = df.fillna(0)
    return df
