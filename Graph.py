#   CLASE GRAFO
#   -----------
#   Sea G el grafo (= tablero) que representa el problema,
#   · G.gap = tamaño de una casilla de G (todas son cuadradas e iguales)
#   · G.total_rows = nº filas del tablero
#   · G.total_cols = nº columnas del tablero
#   · G.pad_rows = espacio entre el borde (horizontal) del tablero y el de la pantalla
#   · G.pad_cols = espacio entre el borde (vertical) del tablero y el de la pantalla
#   · G.nodes = lista de nodos que contiene el grafo
class Graph:

    # Constructor:
    def __init__(self, total_rows, total_cols):
        self.gap = DIM // max(total_rows,total_cols)
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.pad_rows = (DIM - self.gap * total_rows) // 2
        self.pad_cols = (DIM - self.gap * total_cols) // 2
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
            pygame.draw.line(win, GREY, (self.pad_cols, i * self.gap + self.pad_rows),
                             (DIM - self.pad_cols, i * self.gap + self.pad_rows))
            for j in range(self.total_cols + 1):
                pygame.draw.line(win, GREY, (j * self.gap + self.pad_cols, self.pad_rows),
                                 (j * self.gap + (self.pad_cols, DIM - self.pad_rows)))



    # MÉTODOS PÚBLICOS
    # ----------------

    # Dibuja el grafo
    def draw(self, win):
        win.fill(WHITE)
        for row in self.nodes:
            for node in row:
                node.draw(self.gap, win)
        self.draw_grid(self, win)
        pygame.display.update()
