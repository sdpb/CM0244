import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import anderson, t
from statsmodels.api import OLS, qqplot

# Primero importamos nuestra base de datos de saber 11
dataSet = pd.read_csv('saber.csv')

x_barra = 262.0864
ese = 23.8949
u0 = 280
long = 81

# Se definen algunas listas que serán útiles luego
periodos = pd.unique(dataSet.año_semestre).tolist()
comunas = pd.unique(dataSet.comuna).tolist()
tipoPrestacionServicio = pd.unique(dataSet.prestacion_servicio).tolist()  # ['privado', 'oficial', 'contratacion']
materias = ['puntaje_lectura', 'puntaje_matematicas',
            'puntaje_sociales', 'puntaje_naturales', 'puntaje_ingles']


# Filtra el dataset dado un atributo de datos y un parámetro condicional igual o diferente
def filtro_igual(dataS, atributo_muestra, atributo_param, bool_diferente):
    if bool_diferente:
        return dataS[atributo_muestra != atributo_param]
    else:
        return dataS[atributo_muestra == atributo_param]


# Filtra el dataset dado un atributo de datos y un parámetro condicional mayor o igual
def filtro_mayor(dataS, atributo_muestra, atributo_param, bool_mayor_igual):
    if bool_mayor_igual:
        return dataS[dataS[atributo_muestra] >= atributo_param]
    else:
        return dataS[dataS[atributo_muestra] > atributo_param]


# Filtra el dataset dado un atributo de datos y un parámetro condicional menor o igual
def filtro_menor(dataS, atributo_muestra, atributo_param, bool_menor_igual):
    if bool_menor_igual:
        return dataS[dataS[atributo_muestra] <= atributo_param]
    else:
        return dataS[dataS[atributo_muestra] < atributo_param]


# Retorna una muestra dado una función de filtro, su parámetro respectivo
# y un porcentaje como tamaño de la muestra
def obtener_muestra(dataS, filtro_muestra, filtro_param, tam_muestra):
    muestra = filtro_igual(dataS, filtro_muestra, filtro_param, False)
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
    etiquetas = sorted(pd.unique(casos_favorables[atributo_casos_fav]).tolist())

    datos = []
    for _ in etiquetas:
        datos.append(porcentaje(tam_poblacion, len(casos_favorables.loc[casos_favorables[atributo_casos_fav] == _])))
    return datos, etiquetas, atributo_casos_fav


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


def media_periodo(filtro_muestra, periodo, atributo_media, atributo_filtro):
    # Filtro de datos
    filtroDatos = filtro_igual(dataSet, filtro_muestra, periodo, False)
    media = obtener_media(filtroDatos[atributo_media])
    mediaFiltro = filtro_mayor(filtroDatos, atributo_media, media, True)
    datos, etiquetas, titulo = porcentaje_tipo(len(filtroDatos), mediaFiltro, atributo_filtro)
    tarta(datos, etiquetas, '{} {}'.format(titulo.upper(), periodo))


def ecuaRecta():
    x = dataSet.puntaje_matematicas.values.reshape((-1, 1))
    y = dataSet.puntaje_global
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
    plt.title("Q-Q plot")
    plt.show()


if __name__ == '__main__':
    # nuevo_regress()
    # ecuaRecta()
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
