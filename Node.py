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
class Node:

    # Constructor:
    def __init__(self, row, col, gap, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = ((DIM - gap * total_cols) // 2) + col * gap
        self.y = ((DIM - gap * total_rows) // 2) + row * gap
        self.color = WHITE
        self.neighbors = []

    # Getters:
    def get_pos(self):
        return self.row, self.col

    # Conocer estado del nodo:
    def is_closed(self):
        return self.color == BEIGE

    def is_open(self):
        return self.color == BROWN

    def is_barrier(self):
        return self.color == MAROON

    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        return self.color == GREEN

    # Resetear nodo:
    def reset(self):
        self.color = WHITE

    # Cambiar estado del nodo:
    def make_start(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = BEIGE

    def make_open(self):
        self.color = BROWN

    def make_barrier(self):
        self.color = MAROON

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = BLUE

    # Dibujar el nodo
    def draw(self, gap, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, gap, gap))

    # Generar nodos adyacentes:
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Abajo
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Arriba
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Derecha
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Izquierda
            self.neighbors.append(grid[self.row][self.col - 1])

        # /BEA/ AÑADIR DIAGONALES

    # Comparador <
    def __lt__(self, other):
        return False
