"""
Nombre: Yuli del Carmen Gutiérrez Rodríguez
Código: 211501982
Clase: Programación III
Profesor: Diego Ayala
Este programa define lo que es un nodo y una grafo como clases
"""


import csv


class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}


class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodos(self, nombre):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_conexion(self, origen, destino, peso):
        self.agregar_nodos(origen)
        self.agregar_nodos(destino)

        self.nodos[origen].vecinos[destino] = peso
        self.nodos[destino].vecinos[origen] = peso

    # Leer el grafo desde un archivo CSV
    def cargar_csv(self, archivo):
        with open(archivo, mode="r", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            for fila in lector:
                origen = fila["origen"]
                destino = fila["destino"]
                peso = float(fila["peso"])

                self.agregar_conexion(origen, destino, peso)

    # Algoritmo de Dijkstra
    def dijkstra(self, inicio, destino):
        if inicio not in self.nodos:
            raise ValueError(f"El nodo {inicio} no existe")
        if destino not in self.nodos:
            raise ValueError(f"El nodo {destino} no existe")

        distancias = {}
        anteriores = {}
        visitados = set()

        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):

            nodo_actual = None
            menor_distancia = float("inf")

            # Buscar el nodo más cercano
            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            if nodo_actual is None:
                break

            if nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            nodo = self.nodos[nodo_actual]

            for vecino, peso in nodo.vecinos.items():

                if vecino not in visitados:

                    nueva_distancia = (
                        distancias[nodo_actual] + peso
                    )

                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        anteriores[vecino] = nodo_actual

        # Construir el camino
        if distancias[destino] == float("inf"):
            return float("inf"), []

        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]

        camino.reverse()

        return distancias[destino], camino
