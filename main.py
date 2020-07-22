from pandas import read_csv, unique

# Primero importamos nuestra base de datos de saber 11
DATASET = read_csv('saber.csv')

# Se definen algunas listas que serán útiles luego
PERIODOS = unique(DATASET.año_semestre).tolist()  # [20142, 20152, 20162, 20172, 20182]
PRESTACION_SERVICIO = unique(DATASET.PRESTACION_SERVICIO).tolist()  # ['privado', 'oficial', 'contratacion']
COMUNAS = unique(DATASET.comuna).tolist()
MATERIAS = ['puntaje_lectura', 'puntaje_matematicas', 'puntaje_sociales', 'puntaje_naturales', 'puntaje_ingles']

if __name__ == "__main__":
    pass
