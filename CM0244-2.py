# Bibliotecas
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import anderson, t
from statsmodels.api import OLS, qqplot
import matplotlib.pyplot as plt

# Locales
from utilidades.Basicos import *
from utilidades.Graficas import *

# Primero importamos nuestra base de datos de saber 11
dataSet = pd.read_csv('saber.csv')

x_barra = 262.0864
ese = 23.8949
u0 = 280
long = 81

# Se definen algunas listas que serán útiles luego
periodos = pd.unique(dataSet.año_semestre).tolist()  # [20142, 20152, 20162, 20172, 20182]
prestacion_servicio = pd.unique(dataSet.prestacion_servicio).tolist()  # ['privado', 'oficial', 'contratacion']
comunas = pd.unique(dataSet.comuna).tolist()
materias = ['puntaje_lectura', 'puntaje_matematicas',
            'puntaje_sociales', 'puntaje_naturales', 'puntaje_ingles']


# Retorna una muestra dado una función de filtro, su parámetro respectivo
# y un porcentaje como tamaño de la muestra
def obtener_muestra(dataS, filtro_muestra, filtro_param, tam_muestra):
    muestra = filtro_igual(dataS, filtro_muestra, filtro_param, False)
    muestra = muestra.sample(frac=tam_muestra)
    return muestra


# Retorna una lista que contiene la frecuencia relativa de cada tipo de casos favorables
# dado el tamaño de una población, sus casos favorables y un atributo de estos
def porcentaje_tipo(tam_poblacion, casos_favorables, atributo_casos_fav):
    etiquetas = sorted(pd.unique(casos_favorables[atributo_casos_fav]).tolist())

    datos = []
    for _ in etiquetas:
        datos.append(porcentaje(tam_poblacion, len(casos_favorables.loc[casos_favorables[atributo_casos_fav] == _])))
    return datos, etiquetas, atributo_casos_fav


# Retorna un resumen del atributo de una muestra (media, desviación estándar y tamaño de la muestra)
def resumen(atributo_muestra):
    media = obtener_media(atributo_muestra)
    desviacion_estandar = obtener_desvEst(atributo_muestra)
    longitud_muestra = len(atributo_muestra)
    print("Media: {}\nDesviación estándar: {}\nTamaño muestra: {}".format(media, desviacion_estandar, longitud_muestra))


def formula(x, s, u_0, long_m):
    z_c = (x - u_0) / (s / np.sqrt(long_m))
    return z_c


def formula2():
    p_g = 51 / 97
    p_0 = 0.15
    n = 97
    z = (p_g - p_0) / np.sqrt((p_0 * (1 - p_0)) / n)
    return z.round(3)


def media_periodo(filtro_muestra, periodo, atributo_media, atributo_filtro):
    # Filtro de datos
    filtroDatos = filtro_igual(dataSet, filtro_muestra, periodo, False)
    media = obtener_media(filtroDatos[atributo_media])
    mediaFiltro = filtro_mayor(filtroDatos, atributo_media, media, True)
    datos, etiquetas, titulo = porcentaje_tipo(len(filtroDatos), mediaFiltro, atributo_filtro)
    tarta(datos, etiquetas, '{} {}'.format(titulo.upper(), periodo))


def ecuaRecta(dataSet_ind, var_ind, dataSet_dep, var_dep):
    x = dataSet_ind[var_ind].values.reshape((-1, 1))
    y = dataSet_dep[var_dep].values
    modelo = LinearRegression().fit(x, y)
    y_pred = modelo.predict(x)

    r_2 = modelo.score(x, y).round(3)
    beta_0 = modelo.intercept_.round(3)
    beta_1 = modelo.coef_[0].round(3)
    error_cuadratico = mean_squared_error(y, y_pred).round(3)

    print('Coeficiente de determinación R²: {}'.format(r_2))
    print('Beta_0: {}'.format(beta_0))
    print('Beta_1: {}'.format(beta_1))
    print('Error cuadrático medio: {}'.format(error_cuadratico))

    plot_regresion(x, y, var_ind, var_dep)
    plot_regresion(x, y, var_ind, var_dep, y_pred)


def nuevo_regress():
    modelo = OLS(dataSet.puntaje_global, dataSet.puntaje_matematicas).fit()
    summary = modelo.summary()
    print(summary)
    residual_vals = modelo.resid
    qqplot(residual_vals, t, fit=True, line='45')
    print(anderson(residual_vals))
    plt.title("Q-Q plot")
    plt.show()


if __name__ == '__main__':
    # nuevo_regress()
    # ecuaRecta(dataSet, 'puntaje_matematicas', dataSet, 'puntaje_global')
    # puntaje_global_año = obtener_muestra(dataSet.año_semestre, 20182, 0.25)  # .puntaje_global
    # resumen(puntaje_global_año.puntaje_global)
    # naturales = obtener_muestra(dataSet.año_semestre, 20182, 0.3)  # .puntaje_naturales
    # print(len(naturales[naturales.puntaje_naturales < 51]))
    # resumen(naturales.puntaje_naturales)
    # print(formula2())
    # print(obtener_media(filtro(dataSet.año_semestre, 20182).puntaje_naturales))
    # print(formula(x_barra, ese, u0, long))

    # for _ in periodos:
    #    media_periodo(dataSet.año_semestre, _, 'puntaje_global', 'prestacion_servicio')
    pass
