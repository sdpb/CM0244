# Bibliotecas
from numpy import nanmean, nanstd, nanpercentile
from statistics import median

# Locales
from main import DATASET


# Filtra el dataset dado un atributo de datos y un parámetro condicional igual o diferente
def filtro_igual(dataS, atributo_muestra, atributo_param, bool_diferente):
    if bool_diferente:
        return dataS[dataS[atributo_muestra] != atributo_param]
    else:
        return dataS[dataS[atributo_muestra] == atributo_param]


def filtro_periodo(periodo):
    return filtro_igual(DATASET, 'año_semestre', periodo, False)


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


# Retorna la media o promedio de un atributo de una muestra (posiblemente la población)
def obtener_media(atributo_muestra):
    return nanmean(atributo_muestra).round(4)


def obtener_mediana(atributo_muestra):
    return median(atributo_muestra)


# Halla Porcentaje o media relativa dados los parámetros de la muestra y la población
def porcentaje(total_poblacion, total_muestras):
    return (total_muestras / total_poblacion) * 100


# Retorna la desviación estándar de un atributo de una muestra (posiblemente la población)
def obtener_desvEst(atributo_muestra):
    return nanstd(atributo_muestra).round(4)


# Retorna la frecuencia de algún atributo que cumpla con una condición
def obtener_frecuencia(atributo_muestra):
    return len(atributo_muestra)


def obtener_cuartiles(atributo_muestra):
    return [nanpercentile(atributo_muestra, 25), nanpercentile(atributo_muestra, 50),
            nanpercentile(atributo_muestra, 75)]
