
#
#   CLASE ALGORITMO A*
#   ------------------
#   Clase para representar el algoritmo:
#   · graph: grafo que representa el tablero
#   · start: nodo origen
#   · end: nodo destino
#   · waypoints: conjunto con todos los waypoints
#   · waypoints_visit: cola de prioridad que mantiene los waypoints que quedan por visitar
#                      en orden creciente de distancia (euclídea)
#   · waypoints_visit_set: conjunto con los waypoints que quedan por visitar
#   · nodes_visited: lista de los nodos que se han ido visitado (en orden inverso)
#   · risk: penalización que suponen las casillas peligrosas
#   · risk_nodes: conjunto con todas las casillas peligrosas
#


import math
import pygame
from queue import PriorityQueue
from IndexPQ import IndexPQ


class AStar:

    # Constructor:
    def __init__(self, graph, start, end, waypoints, risk, risk_nodes):
        self.graph = graph
        self.start = start
        self.end = end
        self.waypoints = waypoints
        self.waypoints_visit = PriorityQueue()
        self.waypoints_visit_set = waypoints.copy()
        self.nodes_visited = []
        self.risk = risk
        self.risk_nodes = risk_nodes

    # MÉTODOS PRIVADOS
    # ----------------

    # Reconstruir el camino entre dos nodos una vez terminado el algoritmo
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
    #   · g(n) = distancia (coste) real de llegar desde o hasta n
    #       -> Moverse en horizontal/vertical tiene coste = 1
    #       -> Moverse en diagonal tiene coste = sqrt(2)
    #   · h(n) = distancia (coste) estimada de llegar desde n hasta o
    #   · f(n) = g(n) + h(n) = función de evaluación de n
    #
    #   NOTA: para estimar la distancia utilizamos la distancia euclídea entre los nodos

    # Función h(n)
    @staticmethod
    def h(n1, n2):
        x1, y1 = n1
        x2, y2 = n2
        return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    # Función g(n)
    @staticmethod
    def g(g_score, n1, n2):
        x1, y1 = n1.get_pos()
        x2, y2 = n2.get_pos()
        dir_pos = abs(x2 - x1), abs(y2 - y1)
        if dir_pos == (1, 0) or dir_pos == (0, 1):  # Vertical/Horizontal
            return g_score[n1] + 1
        else:  # Diagonal
            return g_score[n1] + math.sqrt(2)

    # Devuelve si un nodo es "especial", es decir, no debe pintarse de otro color para poder distinguirse
    def is_special(self, node):
        return node == self.start or node in self.risk_nodes or node in self.waypoints

    #   ALGORITMO
    #   ---------
    #   Se utilizan las siguientes variables:
    #   · f_score: diccionario {nodo: f(nodo)}
    #   · g_score: diccionario {nodo: h(nodo)}
    #   · came_from: diccionario {nodo: nodo anterior en el camino solución}
    #   · opened: cola con prioridades variables que representa la lista ABIERTA (prioridad = f(nodo))
    #   · closed_set: conjunto que representa la lista CERRADA
    #   · count: variable que indica el momento en que cada nodo entra en ABIERTA (decidir entre iguales y representar
    #            el elemento en la IndexPQ)
    #   · count_dict: diccionario {nodo: count del nodo}, para poder actualizar su prioridad en la IndexPQ y saber si un
    #                 nodo está en ABIERTA
    #
    #   Devuelve (run,path,start):
    #   - El usuario no ha pulsado EXIT
    #   - Hay solución
    #   - Siguiente nodo inicial (puede no ser el end_node previsto si el algoritmo encuentra un waypoint inesperado)
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
        count_dict = {start_node: count}
        # Lista ABIERTA: metemos el nodo inicio
        opened = IndexPQ(self.graph.get_total_rows() * self.graph.get_total_cols())
        opened.put(f_score[start_node], start_node, count)
        # Lista CERRADA:
        closed_set = set()
        # El anterior al nodo inicio es sí mismo
        came_from = {start_node: start_node}

        # EMPIEZA EL ALGORITMO:

        while not opened.empty():  # ¿Quedan nodos en ABIERTA?

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False, None

            # Obtenemos nodo más prioritario
            current = opened.top()[1]
            opened.pop()

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
                self.waypoints_visit_set.add(end_node)  # Al final no hemos visitado end_node
                self.waypoints_visit_set.remove(current)  # Hemos visitado un waypoint inesperado
                return True, True, current

            # Generamos nodos adyacentes al que estamos tratando
            self.graph.update_neighbors(current.get_pos())
            for neighbor in current.neighbors:

                if neighbor not in closed_set:

                    # Calculamos coste para llegar a él
                    g_sc = self.g(g_score, current, neighbor)
                    f_sc = g_sc + self.h(neighbor.get_pos(), end_node.get_pos())
                    if neighbor in self.risk_nodes:
                        f_sc += self.risk  # Aplicamos penalización

                    # Si hemos encontrado un camino mejor:
                    if f_sc < f_score[neighbor]:
                        # Actualizamos camino solución
                        came_from[neighbor] = current
                        # Actualizamos g y f del nodo vecino
                        g_score[neighbor] = g_sc
                        f_score[neighbor] = f_sc
                        # Si no estaba, metemos el nodo en ABIERTA
                        if neighbor not in count_dict:
                            count += 1
                            opened.put(f_score[neighbor], neighbor, count)
                            count_dict[neighbor] = count
                            if not self.is_special(neighbor):
                                neighbor.make_open()
                        # Si ya estaba, actualizamos
                        else:
                            opened.update(count_dict[neighbor], f_score[neighbor])

            self.graph.draw(win)

        return True, False, None

    # Calcula la cola de prioridad de los waypoints que quedan por visitar según su distancia a start_node
    def order_waypoints(self, start_node):
        # Reiniciamos la cola
        self.waypoints_visit = PriorityQueue()
        # Ordenamos los waypoints más cercanos
        for node in self.waypoints_visit_set:
            dist = self.h(start_node.get_pos(), node.get_pos())
            self.waypoints_visit.put([dist, node])

    # MÉTODOS PÚBLICOS
    # ----------------

    # Función algoritmo A* general
    # - Return {run,path} = {¿el usuario ha pulsado EXIT?, ¿hay solución?}
    def algorithm(self, win):

        run = True
        path = True

        # Vemos en qué orden se visitarán los waypoints
        self.order_waypoints(self.start)
        start_node = self.start

        # Mientras   queden waypoints por visitar, y no hayamos encontrado un waypoint/end inalcanzable
        while run and path and len(self.waypoints_visit_set) > 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False

            # Obtenemos waypoint más cercano
            end_node = self.waypoints_visit.get()[1]
            self.waypoints_visit_set.remove(end_node)

            # Ejecutamos el algoritmo
            run, path, start = self.astar(win, start_node, end_node)

            if path:
                start_node = start
                # Recalculamos waypoints más cercanos
                self.order_waypoints(start)

        path_made = False
        while run and path and not path_made:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False

            # Algoritmo para el último waypoint (o start, si no hay ninguno) hasta end
            run, path, start = self.astar(win, start_node, self.end)

            if path:
                # Reconstruir camino
                for i in range(len(self.nodes_visited) - 1):
                    self.reconstruct_path(win, self.nodes_visited[i][1], self.nodes_visited[i+1][0], self.nodes_visited[i][0])
                self.reconstruct_path(win, self.nodes_visited[-1][1], self.start, self.nodes_visited[-1][0])
                path_made = True

        return run, path
