import pandas as pd
import statistics as stats
import numpy as np
import matplotlib.pyplot as plt

# Primero importamos nuestra base de datos de saber 11
dataSet = pd.read_csv('saber11.csv', sep=';')
# dataSet = dataSet.fillna(0) # Rellena espacios vacios con 0


# Se definen algunas listas que serán útiles luego
comunas = pd.unique(dataSet.comuna).tolist()
materias = ['puntaje_lectura', 'puntaje_matematicas',
            'puntaje_sociales', 'puntaje_naturales', 'puntaje_ingles']

# pd.unique(dataSet.año_semestre).tolist()
años = [20142, 20152, 20162, 20172, 20182]
# ['privado', 'oficial', 'contratacion']
tipoPrestacionServicio = pd.unique(dataSet.prestacion_servicio).tolist()


# Filtra el dataset dado un año
def filtro_año(año):
    return dataSet[dataSet.año_semestre == año]


# Filtra el dataset dado el nombre de la comuna
def filtroComuna(comuna):
    return dataSet[dataSet.comuna == comuna]


# Halla Porcentaje o media relativa dados los parámetros de la muestra y la población
def porcentaje(total_poblacion, total_muestras):
    return (total_muestras / total_poblacion) * 100


# Grafica de la frecuencia relativa de datos que cumplen la condición
# de ser mayores o iguales a la media del puntaje global por año
def tarta_tipo_instXaño(año):
    # Filtro de datos
    datosAño = filtro_año(año)
    media = np.nanmean(datosAño.puntaje_global)
    mediaFiltro = datosAño[datosAño.puntaje_global >= media]

    # DEBUG
    """
    print("prueba contratación", len(datosMedia.loc[datosMedia.prestacion_servicio == 'contratacion']))
    print("prueba oficial", len(datosMedia.loc[datosMedia.prestacion_servicio == 'oficial']))
    print("prueba privado", len(datosMedia.loc[datosMedia.prestacion_servicio == 'privado']))
    print("prueba año", len(datosPorYear))
    """

    colores = ['gold', 'lightcoral', 'lightskyblue']

    # Frecuencia relativa por tipo de prestación de servicio
    porcentajes = []
    for _ in tipoPrestacionServicio:
        porcentajes.append(porcentaje(len(datosAño),
                                      len(mediaFiltro.loc[mediaFiltro.prestacion_servicio == _])))

    # Diagrama de torta
    plt.pie(porcentajes, labels=tipoPrestacionServicio, colors=colores,
            autopct='%1.1f%%', shadow=False, startangle=140)
    plt.title(
        "Colegios por encima de la media del puntaje global del año {}".format(año))
    plt.axis('equal')
    plt.show()


# Desviacion estandar del puntaje global dado el año
# para los prestadores de servicio y en general
def desvEstandarAño(año):
    datosAño = filtro_año(año)

    privada = datosAño[datosAño.prestacion_servicio == 'privado']
    oficial = datosAño[datosAño.prestacion_servicio == 'oficial']
    contratacion = datosAño[datosAño.prestacion_servicio == 'contratacion']

    desvGeneral = np.nanstd(datosAño.puntaje_global).round(3)
    desvPrivada = np.nanstd(privada.puntaje_global).round(3)
    desvOficial = np.nanstd(oficial.puntaje_global).round(3)
    desvContratacion = np.nanstd(contratacion.puntaje_global).round(3)

    print("{}: General {}".format(año, desvGeneral))
    print("{}: Privado {}".format(año, desvPrivada))
    print("{}: Oficial {}".format(año, desvOficial))
    print("{}: Contratación {}".format(año, desvContratacion))


# Promedio del puntaje global dado el año
def promedioAño(año):
    datosAño = filtro_año(año)
    # DEBUG
    """
    promed = np.nanmean(datosAño.puntaje_global)
    print("{} = {}".format(año, promed))
    return promed
    """
    return np.nanmean(datosAño.puntaje_global)


# Frecuencia absoluta dado un año
def frecuenciasAño(año):
    datosAño = filtro_año(año)
    return len(datosAño)


# Diagrama de barras dado un año y un método o función
def barras_año(metodo, titulo):
    # Definiendo ejes
    eje_x = list(map(str, años))  # Etiquetas eje x
    eje_y = [metodo(int(_)) for _ in eje_x]  # Valores eje y
    etiquetas = ["%d" % i for i in eje_y]  # Etiquetas eje y

    # Grafica de barras
    fig, ax = plt.subplots()
    ax.set_title(titulo)
    ax.bar(eje_x, eje_y)
    plt.yticks(np.arange(0, 376, 25))
    barras = ax.patches

    # Asigna el valor correspondiente a cada barra
    for barra, etiqueta in zip(barras, etiquetas):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura + 5, etiqueta,
                ha='center', va='bottom')

    plt.show()


# Grafica una tabla dados los datos en forma de matriz y recibiendo
# las etiquetas de columna y fila más el titulo de la grafica
def graficar_tabla(datos, etiqueta_columna, etiqueta_fila, titulo):
    fig, ax = plt.subplots()
    ax.set_title(titulo)
    ax.axis('off')
    ax.table(cellText=datos, rowLabels=etiqueta_fila,
             colLabels=etiqueta_columna, loc='center')
    plt.show()


# Realiza una tabla que compara la media y la mediana de
# todas las comunas con respecto a alguna materia
def tabla_comuna_materia(materia):
    cellText = []  # Texto de las celdas
    for comuna in comunas:
        dataset_ordenado_punt = filtroComuna(comuna).sort_values(materia)
        mediana = int(stats.median(dataset_ordenado_punt[materia]))
        media = np.nanmean(dataset_ordenado_punt[materia]).round(3)
        cellText.append([media, mediana])
    graficar_tabla(cellText, ["Media", "Mediana"], [
        str(_).strip().upper() for _ in comunas], materia.upper())


# Grafica una tabla de frecuencia dada una columna
# del dataset y el título de la grafica
def tabla_frecuencia(columna, titulo):
    fig, ax = plt.subplots()
    columna.value_counts().plot(kind='bar', title=titulo.upper())
    plt.yticks(np.arange(0, 1201, 100))
    fig.show()
    # Debug
    # print("Frecuencia\n{}".format(type(cellText), cellText))


# Grafica una tabla de frecuencia de alguna columna del dataset
# en un año arbitrario
def tabla_frecuencia_rangos(columna, año):
    fig, ax = plt.subplots()
    rangos = range(100, 500 + 1, 100)
    datos = filtro_año(año)
    datos = pd.cut(datos[columna], bins=rangos)
    frecuenciaDatos = datos.value_counts()
    frecuenciaDatos.plot(
        kind='bar', title='{} {}'.format(columna.upper(), año))

    barras = ax.patches
    etiquetas = [str(_) for _ in list(frecuenciaDatos)]  # Etiquetas eje y

    # Asigna el valor correspondiente a cada barra
    for barra, etiqueta in zip(barras, etiquetas):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura + 5, etiqueta,
                ha='center', va='bottom')

    plt.yticks(np.arange(0, 501, 50))
    fig.show()


# Encuentra los cuartiles dada una columna del dataset
def cuartiles(columna):
    return [np.nanpercentile(columna, 25), np.nanpercentile(columna, 50),
            np.nanpercentile(columna, 75)]


# Halla los cuartiles de una materia dado el año
# y el nombre de la materia definido en el dataset
def cuartil_materia(columnaMateria):
    return cuartiles(columnaMateria)


# Grafica una tabla cruzada de datos en forma de diccionario
# recibiendo tambien el titulo de la grafica
def tablacruzada(diccionarioDatos, titulo):
    df = pd.DataFrame.from_dict(diccionarioDatos).transpose()
    df.plot(kind='bar', stacked=False, title=titulo)

    plt.yticks(np.arange(0, 25001, 2000))
    plt.show()


# Encuentra la suma de los estudiantes matriculados, inscritos y presentes
# de las pruebas ICFES dado un año
def presentesICFES_aux(año):
    datosAño = filtro_año(año)
    matriculados = datosAño.matriculados.sum()
    inscritos = datosAño.registros.sum()
    presentes = datosAño.presentes.sum()
    # DEBUG
    # print("Año {}: Inscritos = {} - Presentes = {}".format(año, presentes, inscritos)
    return [matriculados, inscritos, presentes]


# Retorna un diccionario de datos que contiene como llaves los años
# y como valor de la llave es una lista con los matriculados, inscritos y presentes
# de las pruebas ICFES en ese año
def presentesICFES():
    return {str(_): presentesICFES_aux(_) for _ in años}


# Diagrama de bigotes para las materias del dataset dado un año
def bigotes_año_materias(año):
    datosAño = filtro_año(año)

    fig, ax = plt.subplots()
    boxes = []
    for _ in materias:
        aux = datosAño[_]
        boxes.append({
            'label': _[8:].upper(),
            'whislo': min(aux),  # Mínimo
            'q1': cuartil_materia(aux)[0],  # Cuartíl 1 (25)
            'med': cuartil_materia(aux)[1],  # Cuartíl 2 (50)
            'q3': cuartil_materia(aux)[2],  # Cuartíl 3 (75)
            'whishi': max(aux),  # Máximo
            'fliers': []  # Outliers
        })

    plt.yticks(np.arange(0, 121, 10))
    ax.set_title('Distribución percentil por materia {}'.format(año))
    ax.bxp(boxes)
    ax.set_ylabel("Puntos")
    plt.show()


# Descripción general de el dataset crudo (Solo para testeo)
def general_describe():
    for _ in dataSet.columns:
        print(_)
        print()
        print(dataSet[_].describe())


if __name__ == "__main__":
    for _ in años:
        desvEstandarAño(_)
        print("{}: promedio {}".format(_, promedioAño(_)))
        print("Tamaño: {}".format(len(filtro_año(_))))
        tarta_tipo_instXaño(_)
        tabla_frecuencia_rangos('puntaje_global', _)
        bigotes_año_materias(_)

    barras_año(frecuenciasAño, 'Frecuencia años')
    barras_año(promedioAño, 'Promedio años')
    tablacruzada(presentesICFES(),
                 "Matriculados-Inscritos-Presentes ICFES anual")
    for _ in materias:
        tabla_comuna_materia(_)
