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
