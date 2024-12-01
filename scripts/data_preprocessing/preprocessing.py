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


def postprocess_data(df, columns):
    # Reasignar las columnas faltantes
    pass

