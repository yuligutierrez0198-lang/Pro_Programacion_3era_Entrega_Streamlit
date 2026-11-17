"""
Nombre: Yuli del Carmen Gutiérrez Rodríguez
Código: 211501982
Clase: Programación III
Profesor: Diego Ayala
Este programa ejecuta los programas
"""


from io_handler import capturar_y_guardar_conexiones, cargar_grafo


capturar_y_guardar_conexiones("nodos.csv")

# Nodos y pesos hardcodeados
grafo = cargar_grafo("nodos.csv")

# Inicio y fin de hardcodeados
inicio = "A"
destino = "E"
costo, camino = grafo.dijkstra(inicio, destino)

# Mostrar resultados
print("=== Resultados ===")
if camino:
    print(f"Camino más corto de {inicio} a {destino}: {' -> '.join(camino)}")
    print(f"Costo total: {costo}")
else:
    print(f"No hay camino de {inicio} a {destino}.")
