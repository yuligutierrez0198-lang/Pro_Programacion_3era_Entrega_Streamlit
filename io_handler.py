"""
Nombre: Yuli del Carmen Gutiérrez Rodríguez
Código: 211501982
Clase: Programación III
Profesor: Diego Ayala
Este programa implementa el algoritmo de Dijkstra
para encontrar la ruta más corta entre dos nodos en un grafo.
El grafo se construye a partir de un archivo CSV
que contiene las conexiones entre los nodos y sus pesos.
El programa permite al usuario capturar y guardar nuevas conexiones,
así como cargar un grafo existente desde un archivo CSV.
Una vez cargado el grafo, se puede ejecutar el algoritmo de Dijkstra
para determinar la distancia total y el camino más corto entre un nodo de
inicio y un nodo de destino especificados por el usuario.
"""

# Importar CSV
from grafo import Grafo
import csv


# Esta funcion permite capturar y guardar conexiones entre nodos en un CSV.
def capturar_y_guardar_conexiones(ruta):
    print("Registro de conexiones")
    conexiones = []

    while True:
        try:
            origen = input("Nodo origen: ").strip()
            destino = input("Nodo destino: ").strip()
            peso = float(input("Peso:"))

            conexiones.append(
                {"origen": origen, "destino": destino, "peso": peso}
                )

            continuar = input(
                "¿Deseas agregar otra conexión? (s/n): "
                ).strip().lower()
            if continuar not in ("s", "si", "SI"):
                break

        except ValueError:
            print(
                "Error: Debes de ingresar un tipo de dato válido."
                )

    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=["origen", "destino", "peso"]
                )
            escritor.writeheader()
            escritor.writerows(conexiones)
        print("Conexiones guardadas correctamente")
    except FileNotFoundError:
        print("Error: No se encontró el archivo")


def cargar_grafo(ruta):
    grafo = Grafo()
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                origen = fila["origen"]
                destino = fila["destino"]
                peso = float(fila["peso"])
                grafo.agregar_conexion(origen, destino, peso)
    except FileNotFoundError:
        print("Error: No se encontró el archivo")
    return grafo


def guardar_conexion(ruta, origen, destino, peso):
    """
    Guarda una nueva conexión en el archivo CSV
    sin eliminar las conexiones anteriores.
    """

    import os

    # Comprobamos si el archivo existe o está vacío.
    archivo_nuevo = (
        not os.path.exists(ruta)
        or os.path.getsize(ruta) == 0
    )

    # Abrimos el archivo en modo agregar.
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=["origen", "destino", "peso"]
        )

        # Escribimos los encabezados si es necesario.
        if archivo_nuevo:
            escritor.writeheader()

        # Guardamos la conexión.
        escritor.writerow({
            "origen": origen.strip(),
            "destino": destino.strip(),
            "peso": peso
        })
