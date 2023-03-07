
#   CLASE ALGORITMO A*
#   ------------------
#   Clase para representar el algoritmo:
#   · graph: grafo que representa el tablero
#   · start: nodo inicio
#   · end: nodo destino
#   · f_score: diccionario {nodo: f(nodo)}
#   · g_score: diccionario {nodo: h(nodo)}
#   · came_from: diccionario {nodo: nodo anterior en el camino solución}
#   · opened: cola de prioridad que representa la lista ABIERTA (prioridad = f(nodo))
#   · opened_set: conjunto para saber eficientemente si un nodo está en ABIERTA
#   · closed_set: conjunto que representa la lista CERRADA


import math
import pygame
from queue import PriorityQueue


class AStar:

    # Constructor:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start = start
        self.end = end
        # Datos del algoritmo:
        self.f_score = {}
        self.g_score = {}
        self.came_from = {}
        self.opened = PriorityQueue()
        self.opened_set = {}
        self.closed_set = set()

    # MÉTODOS PRIVADOS
    # ----------------

    #   Reconstruir el camino una vez terminado el algoritmo
    def reconstruct_path(self, win):
        current = self.came_from[self.end]
        while current != self.start:
            current.make_path()
            current = self.came_from[current]
            self.graph.draw(win)

    #   FUNCIONES
    #   ---------
    #   Sea o el nodo origen, d el nodo destino, y n un nodo cualquiera del grafo G,
    #   · h(n) = distancia (coste) real de llegar desde o hasta n
    #   · g(n) = distancia (coste) estimada de llegar desde n hasta o
    #   · f(n) = g(n) + h(n) = función de evaluación de n
    #
    #   NOTA: para estimar la distancia utilizamos la distancia euclídea entre los nodos

    # Función h(n)
    def h(self, p):
        x1, y1 = p
        x2, y2 = self.end.get_pos()
        return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    # Función g(n)
    def g(self, n1, n2):
        x1, y1 = n1.get_pos()
        x2, y2 = n2.get_pos()
        dir_pos = abs(x2 - x1), abs(y2 - y1)
        if dir_pos == (1, 0) or dir_pos == (0, 1):  # Vertical/Horizontal
            return self.g_score[n1] + 1
        else:  # Diagonal
            return self.g_score[n1] + math.sqrt(2)

    # MÉTODOS PÚBLICOS
    # ----------------

    # Función Algoritmo A*
    # - Return {run,path} = {¿el usuario ha pulsado EXIT?, ¿hay solución?}
    def algorithm(self, win):

        # INICIALIZAMOS VARIABLES:

        # Función f: inicializamos con Infinito
        self.f_score = {node: float("inf") for row in self.graph.get_nodes() for node in row}
        self.f_score[self.start] = self.h(self.start.get_pos())
        # Función g: inicializamos con Infinito
        self.g_score = {node: float("inf") for row in self.graph.get_nodes() for node in row}
        self.g_score[self.start] = 0  # el coste de llegar al nodo inicial desde el nodo inicial es 0
        # En qué orden entran los nodos en ABIERTA (para decidir entre iguales)
        count = 0
        # Lista ABIERTA: metemos el nodo inicio
        self.opened.put([self.f_score[self.start], count, self.start])
        self.opened_set = {self.start}
        # El anterior al nodo inicio es sí mismo
        self.came_from[self.start] = self.start

        # EMPIEZA EL ALGORITMO:

        while not self.opened.empty():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False

            # Obtenemos nodo más prioritario
            current = self.opened.get()[2]
            self.opened_set.remove(current)

            # Metemos el nodo en CERRADA
            self.closed_set.add(current)
            if current != self.start:
                current.make_closed()

            # Hemos llegado al nodo destino!!
            if current == self.end:
                print(self.closed_set)
                self.end.make_end()
                self.reconstruct_path(win)
                return True, True

            # Generamos nodos adyacentes al que estamos tratando
            self.graph.update_neighbors(current.get_pos())
            for neighbor in current.neighbors:

                if neighbor not in self.closed_set:

                    # Calculamos coste para llegar a él
                    g_score = self.g(current, neighbor)

                    # Hemos encontrado un camino mejor
                    if g_score < self.g_score[neighbor]:
                        # Actualizamos camino solución
                        self.came_from[neighbor] = current
                        # Actualizamos g y f del nodo vecino
                        self.g_score[neighbor] = g_score
                        self.f_score[neighbor] = g_score + self.h(neighbor.get_pos())
                        # Si no estaba, metemos el nodo en ABIERTA
                        if neighbor not in self.opened_set:
                            count += 1
                            self.opened.put((self.f_score[neighbor], count, neighbor))
                            self.opened_set.add(neighbor)
                            neighbor.make_open()

            self.graph.draw(win)

        return True, False
