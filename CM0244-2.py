import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import anderson, t
from statsmodels.api import OLS, qqplot

# Primero importamos nuestra base de datos de saber 11
dataSet = pd.read_csv('saber.csv')
# dataSet = dataSet.fillna(0) # Rellena espacios vacios con 0

x_barra = 262.0864
ese = 23.8949
u0 = 280
long = 81

# Se definen algunas listas que serán útiles luego
pd.unique(dataSet.año_semestre).tolist()
comunas = pd.unique(dataSet.comuna).tolist()
tipoPrestacionServicio = pd.unique(dataSet.prestacion_servicio).tolist()  # ['privado', 'oficial', 'contratacion']
materias = ['puntaje_lectura', 'puntaje_matematicas',
            'puntaje_sociales', 'puntaje_naturales', 'puntaje_ingles']


# Filtra el dataset dado un atributo de datos y un parámetro condicional
def filtro(atributo_muestra, atributo_param):
    return dataSet[atributo_muestra == atributo_param]


# Retorna una muestra dado una función de filtro, su parámetro respectivo
# y un porcentaje como tamaño de la muestra

def obtener_muestra(filtro_muestra, filtro_param, tam_muestra):
    muestra = filtro(filtro_muestra, filtro_param)
    muestra = muestra.sample(frac=tam_muestra)
    return muestra


# Retorna la media o promedio de un atributo de una muestra (posiblemente la población)
def obtener_media(atributo_muestra):
    return np.nanmean(atributo_muestra).round(4)


# Halla Porcentaje o media relativa dados los parámetros de la muestra y la población
def porcentaje(total_poblacion, total_muestras):
    return (total_muestras / total_poblacion) * 100


# Retorna una lista que contiene la frecuencia relativa de cada tipo de casos favorables
# dado el tamaño de una población, sus casos favorables y un atributo de estos
def porcentaje_tipo(tam_poblacion, casos_favorables, atributo_casos_fav):
    lista = sorted(pd.unique(casos_favorables[atributo_casos_fav]).tolist())

    porcentajes = []
    for _ in lista:
        porcentajes.append(porcentaje(tam_poblacion,
                                      len(casos_favorables.loc[casos_favorables[atributo_casos_fav] == _])))
    return porcentajes, lista


# Retorna la desviación estándar de un atributo de una muestra (posiblemente la población)
def obtener_desvEst(atributo_muestra):
    return np.nanstd(atributo_muestra).round(4)


# Retorna un resumen del atributo de una muestra (media, desviación estándar y tamaño de la muestra)
def resumen(atributo_muestra):
    media = obtener_media(atributo_muestra)
    desviacion_estandar = obtener_desvEst(atributo_muestra)
    longitud_muestra = len(atributo_muestra)
    print("Media: {}\nDesviación estándar: {}\nTamaño muestra: {}".format(media, desviacion_estandar, longitud_muestra))


def tarta(datos, etiquetas, titulo):
    # Diagrama de torta
    colores = ['gold', 'lightcoral', 'lightskyblue']
    plt.pie(datos, labels=etiquetas, colors=colores,
            autopct='%1.1f%%', shadow=False, startangle=140)
    plt.title(titulo)
    plt.axis('equal')
    plt.show()


def formula(x, s, u_0, long_m):
    z_c = (x - u_0) / (s / np.sqrt(long_m))
    return z_c


def formula2():
    p_g = 51 / 97
    p_0 = 0.15
    n = 97
    z = (p_g - p_0) / np.sqrt((p_0 * (1 - p_0)) / n)
    return z.round(3)


def media_año(filtro_muestra, año, atributo_media, atributo_filtro):
    # Filtro de datos
    datosAño = filtro(filtro_muestra, año)
    media = obtener_media(datosAño[atributo_media])
    mediaFiltro = datosAño[datosAño[atributo_media] >= media]

    # DEBUG
    """
    print("prueba contratación", len(datosMedia.loc[datosMedia.prestacion_servicio == 'contratacion']))
    print("prueba oficial", len(datosMedia.loc[datosMedia.prestacion_servicio == 'oficial']))
    print("prueba privado", len(datosMedia.loc[datosMedia.prestacion_servicio == 'privado']))
    print("prueba año", len(dfrom sklearn.linear_model import LinearRegressionatosPorYear))
    
    "Colegios por encima de la media del puntaje global del año {}".format(año)
    """

    # Frecuencia relativa por tipo de prestación de servicio
    porcentajes, etiquetas = porcentaje_tipo(len(datosAño), mediaFiltro, atributo_filtro)
    return porcentajes, etiquetas


def ecuaRecta():
    x = dataSet.puntaje_matematicas.values.reshape((-1, 1))
    y = dataSet.puntaje_global
    modelo = LinearRegression().fit(x, y)
    r_sq = modelo.score(x, y)
    y_pred = modelo.predict(x)

    print('coefficient of determination:', r_sq)
    print('b_0:', modelo.intercept_)
    print('b_1:', modelo.coef_)
    print('Error cuadrático medio: %.2f' % mean_squared_error(y, y_pred))
    plots(x, y, y_pred)


def auxplots(x, y, title):
    plt.scatter(x, y, s=np.pi * 3, alpha=0.5)
    plt.title(title)
    plt.xlabel("PUNTAJE MATEMÁTICAS")
    plt.ylabel("PUNTAJE GLOBAL")


def plots(x, y, y_pred):
    auxplots(x, y, "Gráfico de dispersión")
    plt.show()

    auxplots(x, y, "Modelo de regresión")
    plt.plot(x, y_pred, color='red')
    plt.show()


def nuevo_regress():
    modelo = OLS(dataSet.puntaje_global, dataSet.puntaje_matematicas).fit()
    summary = modelo.summary()
    print(summary)
    residual_vals = modelo.resid
    qqplot(residual_vals, t, fit=True, line='45')
    print(anderson(residual_vals))
    plt.show()


if __name__ == '__main__':
    nuevo_regress()
    # ecuaRecta()
    # puntaje_global_año = obtener_muestra(dataSet.año_semestre, 20182, 0.25)  # .puntaje_global
    # resumen(puntaje_global_año.puntaje_global)
    # naturales = obtener_muestra(dataSet.año_semestre, 20182, 0.3)  # .puntaje_naturales
    # print(len(naturales[naturales.puntaje_naturales < 51]))
    # resumen(naturales.puntaje_naturales)
    # print(formula2())
    # print(obtener_media(filtro(dataSet.año_semestre, 20182).puntaje_naturales))
    # print(formula(x_barra, ese, u0, long))
