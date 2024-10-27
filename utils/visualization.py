import matplotlib.pyplot as plt


def plot_anomaly_pie(df):
    plt.figure(figsize=(6, 6))
    df['anomaly'].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'red'], shadow=True, startangle=90)
    plt.title('Proporción de Anomalías')
    plt.ylabel('')
    plt.show()
