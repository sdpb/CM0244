import matplotlib.pyplot as plt


def tarta(datos, etiquetas, titulo):
    # Diagrama de torta
    colores = ['gold', 'lightcoral', 'lightskyblue']
    plt.pie(datos, labels=etiquetas, colors=colores,
            autopct='%1.1f%%', shadow=False, startangle=140)
    plt.title(titulo)
    plt.axis('equal')
    plt.show()


