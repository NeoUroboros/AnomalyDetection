import matplotlib.pyplot as plt


def plot_anomaly_pie(df):
    # Obtiene los conteos por categoría
    counts = df['anomaly'].value_counts()  

    # Define los colores basados en las etiquetas
    colors = ['red' if label == "Anomaly" else 'green' for label in counts.index]

    # Genera el gráfico de pastel
    plt.figure(figsize=(6, 6))
    counts.plot.pie(
        autopct='%1.1f%%',
        colors=colors,
        shadow=True,
        startangle=90
    )
    plt.title('Proporción de Anomalías')
    plt.ylabel('')  # Oculta el eje Y
    plt.show()



def plot_anomaly_scatter(df, feature_x, feature_y):

    # Colores basados en la etiqueta 'anomaly'
    colors = df['anomaly'].apply(lambda x: 'red' if x == "Anomaly" else 'green')

    # Crear gráfico de dispersión
    plt.figure(figsize=(8, 6))
    plt.scatter(df[feature_x], df[feature_y], c=colors, alpha=0.8, edgecolors='k', label='Anomaly')
    
    # Etiquetas y título
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.title('Gráfico de Dispersión de Anomalías')
    plt.grid(True)
    plt.show()

# Ejemplo de uso
# Asumiendo que 'df_result' contiene las columnas 'feature_1', 'feature_2', y 'anomaly'
# plot_anomaly_scatter(df_result, 'feature_1', 'feature_2')
