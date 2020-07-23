# Bibliotecas
from pandas import cut, DataFrame
from pandas import unique as pd_unique
from scipy.stats import anderson
from statsmodels.api import OLS

# Locales
from utilidades.Basicos import *
from utilidades.Graficas import *


# Retorna una lista que contiene la frecuencia relativa de cada tipo de casos favorables
# dado el tamaño de una población, sus casos favorables y un atributo de estos
def porcentaje_tipo(tam_poblacion, casos_favorables, atributo_casos_fav):
    etiquetas = sorted(pd_unique(casos_favorables[atributo_casos_fav]).tolist())

    datos = []
    for _ in etiquetas:
        datos.append(porcentaje(tam_poblacion, len(casos_favorables.loc[casos_favorables[atributo_casos_fav] == _])))
    return datos, etiquetas, atributo_casos_fav


def media_periodo(periodo, atributo_filtro):
    # Filtro de datos
    puntaje_global = 'puntaje_global'
    filtroDatos = filtro_periodo(periodo)
    media = obtener_media(filtroDatos[puntaje_global])
    mediaFiltro = filtro_mayor(filtroDatos, puntaje_global, media, True)
    datos, etiquetas, titulo = porcentaje_tipo(len(filtroDatos), mediaFiltro, atributo_filtro)
    tarta(datos, etiquetas, '{} {}'.format(titulo.upper(), periodo))


# Desviación estándar del puntaje global dado el año
# para los prestadores de servicio y en general
def desv_estandar_periodo(periodo):
    datosPeriodo = filtro_periodo(periodo)

    for _ in PRESTACION_SERVICIO:
        desv = filtro_igual(datosPeriodo, 'prestacion_servicio', _, False)
        desv = obtener_desvEst(desv['puntaje_global'])
        print("{}: {} {}".format(periodo, _.capitalize(), desv))


# Promedio de algún atributo numérico dado el periodo
def promedio_periodo(periodo, atributo):
    datosPeriodo = filtro_periodo(periodo)
    return obtener_media(datosPeriodo[atributo])


# Frecuencia de algún periodo
def frecuencia_periodo(periodo):
    datosPeriodo = filtro_periodo(periodo)
    return obtener_frecuencia(datosPeriodo)


def nuevo_regress():
    modelo = OLS(DATASET.puntaje_global, DATASET.puntaje_matematicas).fit()
    summary = modelo.summary()
    vals_residuales = modelo.resid
    print(summary)
    print(anderson(vals_residuales))
    grafica_qq(vals_residuales)


# Realiza una tabla que compara la media y la mediana de
# todas las comunas con respecto a alguna materia
def tabla_comuna_materia(materia):
    cellText = []  # Texto de las celdas
    for comuna in COMUNAS:
        dataset_ordenado_punt = filtro_igual(DATASET, 'comuna', comuna, False).sort_values(materia)[materia]
        mediana = obtener_mediana(dataset_ordenado_punt)
        media = obtener_media(dataset_ordenado_punt)
        cellText.append([media, mediana])
    grafica_tabla(cellText, ['Media', 'Mediana'], [
        str(_).strip().upper() for _ in COMUNAS], materia.upper())


# Grafica una tabla de frecuencia de alguna columna del dataset
# en un año arbitrario
def tabla_frecuencia_rangos(atributo_muestra, periodo):
    rangos = range(100, 500 + 1, 100)
    datos = filtro_periodo(periodo)
    datos = cut(datos[atributo_muestra], bins=rangos)
    frecuenciaDatos = datos.value_counts()
    titulo = '{} {}'.format(atributo_muestra.upper(), periodo)
    etiquetas = list(map(str, frecuenciaDatos))  # Etiquetas eje y
    grafica_frecuencia_rangos(frecuenciaDatos, etiquetas, titulo)


# Encuentra la suma de los estudiantes matriculados, inscritos y presentes
# de las pruebas ICFES dado un año
def presentesICFES_aux(periodo):
    datosPeriodo = filtro_periodo(periodo)
    matriculados = datosPeriodo.matriculados.sum()
    inscritos = datosPeriodo.registros.sum()
    presentes = datosPeriodo.presentes.sum()
    # DEBUG
    # print("Año {}: Inscritos = {} - Presentes = {}".format(año, presentes, inscritos)
    return [matriculados, inscritos, presentes]


# Retorna un diccionario de datos que contiene como llaves los años
# y como valor de la llave es una lista con los matriculados, inscritos y presentes
# de las pruebas ICFES en ese año
def presentesICFES():
    titulo = 'Matriculados-Inscritos-Presentes ICFES anual'
    diccionarioDatos = {str(_): presentesICFES_aux(_) for _ in PERIODOS}
    df = DataFrame.from_dict(diccionarioDatos).transpose()
    grafica_tablaCruzada(df, titulo)


# Diagrama de bigotes para las materias del dataset dado un año
def bigotes_periodo_materias(periodo):
    datosPeriodo = filtro_periodo(periodo)
    titulo = 'Distribución percentil por materia {}'.format(periodo)
    boxes = []
    for _ in MATERIAS:
        aux = datosPeriodo[_]
        boxes.append({
            'label': _[8:].upper(),
            'whislo': min(aux),  # Mínimo
            'q1': obtener_cuartiles(aux)[0],  # Cuartíl 1 (25)
            'med': obtener_cuartiles(aux)[1],  # Cuartíl 2 (50)
            'q3': obtener_cuartiles(aux)[2],  # Cuartíl 3 (75)
            'whishi': max(aux),  # Máximo
            'fliers': []
        })

    grafica_bigotes(boxes, titulo)


def estadistica_descriptiva():
    for _ in PERIODOS:
        periodo = filtro_periodo(_)
        desv_estandar_periodo(_)
        print("{}: promedio {}".format(_, obtener_media(periodo['puntaje_global'])))
        print("Tamaño: {}".format(len(periodo)))
        media_periodo(_, 'prestacion_servicio')
        bigotes_periodo_materias(_)

    txt_periodos = list(map(str, PERIODOS))  # Etiquetas eje x
    promedio_periodos = [promedio_periodo(int(_), 'puntaje_global') for _ in txt_periodos]  # Valores eje y
    frecuencia_periodos = [frecuencia_periodo(int(_)) for _ in txt_periodos]  # Valores eje y
    grafica_barras(txt_periodos, frecuencia_periodos, 'Frecuencia Años')
    grafica_barras(txt_periodos, promedio_periodos, 'Promedio Años')

    presentesICFES()

    for _ in MATERIAS:
        tabla_comuna_materia(_)

    tabla_frecuencia_rangos('puntaje_global', 20182)


# Descripción general de el dataset crudo (Solo para testeo)
def descripcion_general():
    for _ in DATASET.columns:
        print(_)
        print()
        print(DATASET[_].describe())
