
#   CLASE NODO
#   ----------
#   Sea n un nodo (= casilla) del grafo (= tablero),
#   · n.row = fila del tablero en la que está n
#   · n.col = columna del tablero en la que está n
#   · n.color = estado actual de n (ver correspondencia de colores)
#   · n.neighbors = lista de nodos adyacentes a n
#   Los siguientes atributos son útiles para dibujar n:
#   · n.x = posición horizontal absoluta de n en la pantalla)
#   · n.y = posición vertical absoluta de n en la pantalla)

import Utilities
import pygame


class Node:

    # Constructor:
    def __init__(self, row, col, gap, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = Utilities.MARGIN + ((Utilities.DIM - gap * total_cols) // 2) + col * gap
        self.y = Utilities.HEADER + ((Utilities.DIM - gap * total_rows) // 2) + row * gap
        self.color = Utilities.WHITE
        self.neighbors = []

    # Getters:
    def get_pos(self):
        return self.row, self.col

    def no_neighbors(self):
        return len(self.neighbors) == 0

    # Conocer estado del nodo:
    def is_closed(self):
        return self.color == Utilities.BEIGE

    def is_open(self):
        return self.color == Utilities.BROWN

    def is_barrier(self):
        return self.color == Utilities.MAROON

    def is_start(self):
        return self.color == Utilities.YELLOW

    def is_end(self):
        return self.color == Utilities.GREEN

    def is_waypoint(self):
        return self.color == Utilities.PURPLE

    def is_risky(self):
        return self.color == Utilities.RED

    # Setters:
    def reset(self):
        self.color = Utilities.WHITE

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    # Cambiar estado del nodo:
    def make_start(self):
        self.color = Utilities.YELLOW

    def make_closed(self):
        self.color = Utilities.BEIGE

    def make_open(self):
        self.color = Utilities.BROWN

    def make_barrier(self):
        self.color = Utilities.MAROON

    def make_end(self):
        self.color = Utilities.GREEN

    def make_waypoint(self):
        self.color = Utilities.PURPLE

    def make_risky(self):
        self.color = Utilities.RED

    def make_path(self):
        self.color = Utilities.BLUE

    # Dibujar el nodo
    def draw(self, gap, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, gap, gap))

    # Comparador <
    def __lt__(self, other):
        return False
