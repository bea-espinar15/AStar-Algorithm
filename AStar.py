
#   CLASE ALGORITMO A*
#   ------------------
#   Clase para representar el algoritmo

import math
from queue import PriorityQueue


class AStar:

    # Constructor:
    def __init__(self, graph):
        self.graph = graph

    # MÉTODOS PRIVADOS
    # ----------------

    #   Reconstruir el camino una vez terminado el algoritmo
    def reconstruct_path(self, came_from, current, win):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.graph.draw(win)

    #   FUNCIONES
    #   ---------
    #   Sea o el nodo origen, d el nodo destino, y n un nodo cualquiera del grafo G,
    #   · h(n) = distancia (coste) real de llegar desde o hasta n
    #   · g(n) = distancia (coste) estimada de llegar desde n hasta o
    #   · f(n) = g(n) + h(n) = función de evaluación de n
    #
    #   NOTA: para estimar la distancia utilizamos la distancia euclídea entre los nodos

    # Función g(n)
    def g(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    # MÉTODOS PÚBLICOS
    # ----------------

    # Algoritmo A*
    def algorithm(self, start, end):

        # INICIALIZAMOS VARIABLES:

        # Función f para cada nodo (diccionario)
        f_score = {}
        # Función g para cada nodo (diccionario)
        g_score = {}
        # En qué orden entran los nodos en ABIERTA (para decidir entre iguales)
        count = 0
        # Lista ABIERTA: metemos el nodo inicio
        opened = PriorityQueue()
        opened.put(0, count, start)
        opened_set = {start}  # Para saber si un nodo está en la lista
        # Lista CERRADA
        closed_set = {}



        came_from = {}
        g_score = {node: float("inf") for row in grid for node in row}
        g_score[start] = 0
        f_score = {node: float("inf") for row in grid for node in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())



        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end, draw)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False
