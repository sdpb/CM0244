# Bibliotecas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import anderson
from statsmodels.api import OLS

# Locales
from utilidades.Basicos import *
from utilidades.Graficas import *


# Retorna una muestra dado una función de filtro, su parámetro respectivo
# y un porcentaje como tamaño de la muestra
def obtener_muestra(dataS, filtro_muestra, filtro_param, tam_muestra):
    muestra = filtro_igual(dataS, filtro_muestra, filtro_param, False)
    muestra = muestra.sample(frac=tam_muestra)
    return muestra


x_barra = 262.0864
ese = 23.8949
u0 = 280
long = 81


# Retorna un resumen del atributo de una muestra (media, desviación estándar y tamaño de la muestra)
def resumen(dataSet, atributo_muestra):
    media = obtener_media(dataSet[atributo_muestra])
    desviacion_estandar = obtener_desvEst(dataSet[atributo_muestra])
    longitud_muestra = len(dataSet[atributo_muestra])
    print("Media: {}\nDesviación estándar: {}\nTamaño muestra: {}".format(media, desviacion_estandar, longitud_muestra))
    return media, desviacion_estandar, longitud_muestra


def Z_c(media, desviacion_estandar, hipotesis, long_muestra):
    return (media - hipotesis) / (desviacion_estandar / np.sqrt(long_muestra))


def Z_c2(media, hipotesis, long_muestra):
    P_g = media / long_muestra
    z = (P_g - hipotesis) / np.sqrt((hipotesis * (1 - hipotesis)) / long_muestra)
    return z.round(3)


def ecuaRecta(dataSet_ind, var_ind, dataSet_dep, var_dep):
    x = dataSet_ind[var_ind].values.reshape((-1, 1))
    y = dataSet_dep[var_dep].values
    regresion = LinearRegression().fit(x, y)
    y_pred = regresion.predict(x)

    r_2 = regresion.score(x, y).round(3)
    beta_0 = regresion.intercept_.round(3)
    beta_1 = regresion.coef_[0].round(3)
    error_cuadratico = mean_squared_error(y, y_pred).round(3)

    print('Coeficiente de determinación R²: {}'.format(r_2))
    print('Beta_0: {}'.format(beta_0))
    print('Beta_1: {}'.format(beta_1))
    print('Error cuadrático medio: {}'.format(error_cuadratico))

    plot_regresion(x, y, var_ind, var_dep)
    plot_regresion(x, y, var_ind, var_dep, y_pred)


def modelo_regresion():
    return OLS(DATASET.puntaje_global, DATASET.puntaje_matematicas).fit()
    summary = modelo.summary()
    vals_residuales = modelo.resid
    print(summary)
    print(anderson(vals_residuales))
    grafica_qq(vals_residuales)


def estadistica_inferencial():
    muestra_periodo_25 = obtener_muestra(DATASET, 'año_semestre', 20182, 0.25)  # Puntaje_global
    media_1, desviacion_estandar_1, longitud_muestra_1 = resumen(muestra_periodo_25, 'puntaje_global')
    print('Se rechaza H_0: {}'.format(Z_c(media_1, desviacion_estandar_1, 280, longitud_muestra_1) < -Z_alfa))
    print('\n{}'.format('*' * 100))

    muestra_periodo_30 = obtener_muestra(DATASET, 'año_semestre', 20182, 0.3)  # Puntaje_naturales
    media_naturales_20182 = obtener_media(filtro_periodo(20182)['puntaje_naturales'])
    media_2, desviacion_estandar_2, longitud_muestra_2 = resumen(muestra_periodo_30, 'puntaje_naturales')

    print('Instituciones debajo de la media: {}'.format(
        len(muestra_periodo_30[muestra_periodo_30['puntaje_naturales'] < media_naturales_20182])))
    print('Se rechaza H_0: {}'.format(Z_c2(media_2, 0.15, longitud_muestra_2) > Z_alfa))
    print('\n{}'.format('*' * 100))

    modelo = modelo_regresion()
    valores_residuales = modelo.resid
    print('Nivel de significancia Anderson Darling {}'.format(anderson(valores_residuales)[2]))
    print('\n{}'.format('*' * 100))
    print(modelo.summary())
    print('\n{}'.format('*' * 100))

    ecuaRecta(DATASET, 'puntaje_matematicas', DATASET, 'puntaje_global')
    grafica_qq(valores_residuales)
