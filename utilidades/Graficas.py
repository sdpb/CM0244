import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t
from statsmodels.api import qqplot


def tarta(datos, etiquetas, titulo):
    # Diagrama de torta
    colores = ['gold', 'lightcoral', 'lightskyblue']
    plt.pie(datos,
            labels=list(map(str.capitalize, etiquetas)),
            colors=colores,
            autopct='%1.1f%%',
            shadow=False,
            startangle=140)
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


def grafica_qq(valores_residuales):
    qqplot(valores_residuales, t, fit=True, line='45')
    plt.title("Q-Q plot")
    plt.show()


def grafica_barras(eje_x, eje_y, titulo):
    etiquetas = list(map(str, eje_y))
    # Grafica de barras
    fig, ax = plt.subplots()
    ax.set_title(titulo)
    ax.bar(eje_x, eje_y)
    plt.yticks(np.arange(0, 376, 25))
    barras = ax.patches
    valor_barra_aux(ax, barras, etiquetas)
    plt.show()


# Grafica una tabla dados los datos en forma de matriz y recibiendo
# las etiquetas de columna y fila más el titulo de la grafica
def grafica_tabla(datos, etiqueta_columna, etiqueta_fila, titulo):
    fig, ax = plt.subplots()
    ax.set_title(titulo)
    ax.axis('off')
    ax.table(cellText=datos, rowLabels=etiqueta_fila,
             colLabels=etiqueta_columna, loc='center')
    plt.show()


def grafica_frecuencia_rangos(datos, etiquetas, titulo):
    fig, ax = plt.subplots()
    datos.plot(
        kind='bar', title=titulo)

    barras = ax.patches
    valor_barra_aux(ax, barras, etiquetas)

    plt.yticks(np.arange(0, 501, 50))
    fig.show()


# Grafica una tabla cruzada de datos en forma de diccionario
# recibiendo tambien el titulo de la grafica
def grafica_tablaCruzada(dataframe, titulo):
    dataframe.plot(kind='bar', stacked=False, title=titulo)
    plt.yticks(np.arange(0, 25001, 2000))
    plt.show()


def grafica_bigotes(boxes, titulo):
    fig, ax = plt.subplots()
    plt.yticks(np.arange(0, 121, 10))
    ax.set_title(titulo)
    ax.bxp(boxes)
    ax.set_ylabel("Puntos")
    plt.show()


# Asigna el valor correspondiente a cada barra
def valor_barra_aux(ax, barras, etiquetas):
    for barra, etiqueta in zip(barras, etiquetas):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura + 5, etiqueta,
                ha='center', va='bottom')
