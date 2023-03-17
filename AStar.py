
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

import Utilities


class AStar:

    # Constructor:
    def __init__(self, graph, start, end, waypoints, risk_nodes):
        self.graph = graph
        self.start = start
        self.end = end
        self.waypoints = waypoints
        self.waypoints_visit = PriorityQueue()
        self.waypoints_visit_set = waypoints.copy()
        self.nodes_visited = []
        self.risk_nodes = risk_nodes

    # MÉTODOS PRIVADOS
    # ----------------

    #   Reconstruir el camino una vez terminado el algoritmo
    def reconstruct_path(self, win, came_from, start_node, end_node):
        current = came_from[end_node]
        while current != start_node:
            if not self.is_special(current):
                current.make_path()
            current = came_from[current]
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
    def h(self, p, q):
        x1, y1 = p
        x2, y2 = q
        return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    # Función g(n)
    def g(self, g_score, n1, n2):
        x1, y1 = n1.get_pos()
        x2, y2 = n2.get_pos()
        dir_pos = abs(x2 - x1), abs(y2 - y1)
        if dir_pos == (1, 0) or dir_pos == (0, 1):  # Vertical/Horizontal
            return g_score[n1] + 1
        else:  # Diagonal
            return g_score[n1] + math.sqrt(2)

    def is_special(self, node):
        return node == self.start or node in self.risk_nodes or node in self.waypoints

    def astar(self, win, start_node, end_node):

        # INICIALIZAMOS VARIABLES:

        # Función f: inicializamos con Infinito
        f_score = {node: float("inf") for row in self.graph.get_nodes() for node in row}
        f_score[start_node] = self.h(start_node.get_pos(), end_node.get_pos())
        # Función g: inicializamos con Infinito
        g_score = {node: float("inf") for row in self.graph.get_nodes() for node in row}
        g_score[start_node] = 0  # el coste de llegar al nodo inicial desde el nodo inicial es 0
        # En qué orden entran los nodos en ABIERTA (para decidir entre iguales)
        count = 0
        # Lista ABIERTA: metemos el nodo inicio
        opened = PriorityQueue()
        opened.put([f_score[start_node], count, start_node])
        opened_set = {start_node}
        # Lista CERRADA:
        closed_set = set()
        # El anterior al nodo inicio es sí mismo
        came_from = {start_node: start_node}

        # EMPIEZA EL ALGORITMO:

        while not opened.empty():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False

            # Obtenemos nodo más prioritario
            current = opened.get()[2]
            opened_set.remove(current)

            # Metemos el nodo en CERRADA
            closed_set.add(current)
            if current != start_node and not self.is_special(current):
                current.make_closed()

            # Hemos llegado al nodo destino!!
            if current == end_node:
                if current == self.end:
                    current.make_end()
                else:
                    current.make_waypoint()
                self.nodes_visited.insert(0, (current, came_from))
                return True, True, current

            # Hemos encontrado un waypoint
            if current in self.waypoints_visit_set and current != start_node:
                current.make_waypoint()
                self.nodes_visited.insert(0, (current, came_from))
                self.waypoints_visit_set.add(end_node)
                self.waypoints_visit_set.remove(current)
                return True, True, current

            # Generamos nodos adyacentes al que estamos tratando
            self.graph.update_neighbors(current.get_pos())
            for neighbor in current.neighbors:

                if neighbor not in closed_set:

                    # Calculamos coste para llegar a él
                    g_sc = self.g(g_score, current, neighbor)

                    # Hemos encontrado un camino mejor
                    if g_sc < g_score[neighbor]:
                        # Actualizamos camino solución
                        came_from[neighbor] = current
                        # Actualizamos g y f del nodo vecino
                        g_score[neighbor] = g_sc
                        f_score[neighbor] = g_sc + self.h(neighbor.get_pos(), end_node.get_pos())
                        if neighbor in self.risk_nodes:
                            f_score[neighbor] += Utilities.RISK
                        # Si no estaba, metemos el nodo en ABIERTA
                        if neighbor not in opened_set:
                            count += 1
                            opened.put((f_score[neighbor], count, neighbor))
                            opened_set.add(neighbor)
                            if not self.is_special(neighbor):
                                neighbor.make_open()

            self.graph.draw(win)

        return True, False, -1

    def order_waypoints(self, start_node):
        # Reiniciamos la cola
        self.waypoints_visit = PriorityQueue()
        # Ordenamos los waypoints más cercanos
        for node in self.waypoints_visit_set:
            dist = self.h(start_node.get_pos(), node.get_pos())
            self.waypoints_visit.put([dist, node])

    # MÉTODOS PÚBLICOS
    # ----------------

    # Función Algoritmo A*
    # - Return {run,path} = {¿el usuario ha pulsado EXIT?, ¿hay solución?}
    def algorithm(self, win):

        run = True
        path = True

        self.order_waypoints(self.start)
        start_node = self.start

        while run and path and len(self.waypoints_visit_set) > 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            end_node = self.waypoints_visit.get()[1]
            self.waypoints_visit_set.remove(end_node)
            run, path, start = self.astar(win, start_node, end_node)
            self.order_waypoints(start)
            start_node = start

        path_made = False
        while run and path and not path_made:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            run, path, start = self.astar(win, start_node, self.end)
            # Reconstruir camino
            for i in range(len(self.nodes_visited) - 1):
                self.reconstruct_path(win, self.nodes_visited[i][1], self.nodes_visited[i+1][0], self.nodes_visited[i][0])
            self.reconstruct_path(win, self.nodes_visited[-1][1], self.start, self.nodes_visited[-1][0])
            path_made = True

        return run, path
