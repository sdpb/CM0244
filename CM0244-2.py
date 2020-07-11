import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import f_oneway, ttest_ind, t, anderson

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


def independent_ttest(data1, data2):
    df = len(data1) + len(data2) - 2
    # calculate means
    mean1, mean2 = np.mean(data1), np.mean(data2)
    # calculate standard errors
    se1, se2 = np.sem(data1), np.sem(data2)
    # standard error on the difference between the samples
    sed = np.sqrt(se1 ** 2.0 + se2 ** 2.0)
    # calculate the t statistic
    t_stat = (mean1 - mean2) / sed
    p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0

    return t_stat, p


def modelo_lineal():
    x = dataSet.puntaje_matematicas.values.reshape((-1, 1))
    x2 = dataSet.puntaje_matematicas.values
    y = dataSet.puntaje_global
    modelo = LinearRegression().fit(x, y)
    r_sq = modelo.score(x, y)
    r2 = modelo.score(x.reshape(-1, 1), y)
    y_pred = modelo.predict(x)
    ttest, af = ttest_ind(y, x)
    stat, p = ttest_ind(x, y)
    """
    print('coefficient of determination:', r_sq)
    print('b_0:', modelo.intercept_)
    print('b_1:', modelo.coef_)
    print('Error cuadrático medio: %.2f' % mean_squared_error(y, y_pred))
    print('Coeficiente de Determinación R2 = {}'.format(r2))
    print(f_oneway(x2, y))
    print(ttest, af)
    print('t=%.3f, p=%.3f' % (stat, p))
    """

    from statsmodels.api import OLS
    OLS(dataSet.puntaje_matematicas, dataSet.puntaje_global).fit().summary()

    plt.scatter(x, y, s=np.pi * 3, alpha=0.5)
    plt.title("MODELO DE REGRESIÓN LINEAL")
    plt.xlabel("PUNTAJE MATEMÁTICAS")
    plt.ylabel("PUNTAJE GLOBAL")
    plt.plot(x, y_pred, color='red')
    plt.show()


if __name__ == '__main__':
    from statsmodels.api import OLS
    print(OLS(dataSet.puntaje_global, dataSet.puntaje_matematicas).fit().summary())
    # modelo_lineal()
    # puntaje_global_año = obtener_muestra(dataSet.año_semestre, 20182, 0.25)  # .puntaje_global
    # resumen(puntaje_global_año.puntaje_global)
    # naturales = obtener_muestra(dataSet.año_semestre, 20182, 0.3)  # .puntaje_naturales
    # print(len(naturales[naturales.puntaje_naturales < 51]))
    # resumen(naturales.puntaje_naturales)
    # print(formula2())
    # print(obtener_media(filtro(dataSet.año_semestre, 20182).puntaje_naturales))
    # print(formula(x_barra, ese, u0, long))
