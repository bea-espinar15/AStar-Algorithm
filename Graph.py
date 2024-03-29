
#
#   CLASE GRAFO
#   -----------
#   Sea G el grafo (= tablero) que representa el problema,
#   · G.gap = tamaño de una casilla de G (todas son cuadradas e iguales)
#   · G.total_rows = nº filas del tablero
#   · G.total_cols = nº columnas del tablero
#   · G.pad_rows = espacio entre el borde (horizontal) del tablero y el de la pantalla
#   · G.pad_cols = espacio entre el borde (vertical) del tablero y el de la pantalla
#   · G.nodes = lista de nodos que contiene el grafo
#


import pygame
from Node import Node
import Utilities


class Graph:

    # Constructor:
    def __init__(self, total_rows, total_cols):
        self.gap = Utilities.DIM // max(total_rows, total_cols)
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.pad_rows = (Utilities.DIM - self.gap * total_rows) // 2
        self.pad_cols = (Utilities.DIM - self.gap * total_cols) // 2
        self.nodes = []
        self.create_graph()

    # MÉTODOS PRIVADOS
    # ----------------

    # Crea la matriz que representa el grafo
    def create_graph(self):
        for i in range(self.total_rows):
            self.nodes.append([])
            for j in range(self.total_cols):
                node = Node(i, j, self.gap, self.total_rows, self.total_cols)
                self.nodes[i].append(node)

    # Dibuja las líneas del tablero
    def draw_grid(self, win):
        for i in range(self.total_rows + 1):
            pygame.draw.line(win, Utilities.GREY, (Utilities.MARGIN + self.pad_cols, Utilities.HEADER + i * self.gap + self.pad_rows),
                             (Utilities.MARGIN + Utilities.DIM - self.pad_cols, Utilities.HEADER + i * self.gap + self.pad_rows))
            for j in range(self.total_cols + 1):
                pygame.draw.line(win, Utilities.GREY, (Utilities.MARGIN + j * self.gap + self.pad_cols, Utilities.HEADER + self.pad_rows),
                                 (Utilities.MARGIN + j * self.gap + self.pad_cols, Utilities.HEADER + Utilities.DIM - self.pad_rows))

    # Comprueba si una casilla está dentro de los límites del tablero
    def valid_pos(self, row, col):
        return 0 <= row < self.total_rows and 0 <= col < self.total_cols

    # MÉTODOS PÚBLICOS
    # ----------------

    # Getters
    def get_nodes(self):
        return self.nodes

    def get_total_rows(self):
        return self.total_rows

    def get_total_cols(self):
        return self.total_cols

    # Dibuja el grafo
    def draw(self, win):
        for row in self.nodes:
            for node in row:
                node.draw(self.gap, win)
        self.draw_grid(win)
        pygame.display.update()

    # Generar nodos adyacentes a un nodo dado si no se habían generado ya:
    def update_neighbors(self, pos):
        row, col = pos
        if self.nodes[row][col].no_neighbors():
            neighbors = []
            for d in Utilities.DIRS:
                n_row = row + d[0]
                n_col = col + d[1]
                # Si está dentro de los límites y no es un nodo inalcanzable
                if self.valid_pos(n_row, n_col) and not self.nodes[n_row][n_col].is_barrier():
                    neighbors.append(self.nodes[n_row][n_col])
            self.nodes[row][col].set_neighbors(neighbors)
