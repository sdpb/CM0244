import matplotlib.pyplot as plt
import numpy as np


def tarta(datos, etiquetas, titulo):
    # Diagrama de torta
    colores = ['gold', 'lightcoral', 'lightskyblue']
    plt.pie(datos, labels=etiquetas, colors=colores,
            autopct='%1.1f%%', shadow=False, startangle=140)
    plt.title(titulo)
    plt.axis('equal')
    plt.show()


def plot_regresion(x, y, etiqueta_x, etiqueta_y, y_pred=None):
    plt.scatter(x, y, s=np.pi * 3, alpha=0.5)
    plt.xlabel('{}'.format(etiqueta_x.upper()))
    plt.ylabel('{}'.format(etiqueta_y.upper()))
    if y_pred is not None:
        plt.plot(x, y_pred, color='red')
        plt.title('MODELO DE REGRESIÓN')
    else:
        plt.title('GRÁFICO DE DISPERSIÓN')
    plt.show()
