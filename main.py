import math
import pygame
from queue import PriorityQueue

DIM = 800
WIN = pygame.display.set_mode((DIM, DIM))
pygame.display.set_caption("A Star Algorithm")

BEIGE = (237, 199, 150)
BROWN = (219, 139, 86)
WHITE = (255, 255, 255)
MAROON = (132, 44, 48)
BLUE = (155, 191, 209)
YELLOW = (233, 188, 109)
GREY = (128, 128, 128)
GREEN = (132, 167, 37)


class Spot:

    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = ((DIM - width * total_cols) // 2) + col * width
        self.y = ((DIM - width * total_rows) // 2) + row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

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

    def reset(self):
        self.color = WHITE

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

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        # FALTA AÑADIR DIAGONALES

    def __lt__(self, other):
        return False


# CAMBIAR POR DISTANCIA EUCLÍDEA
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, cols, width):
    grid = []
    gap = width // max(rows,cols)
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, rows, cols)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, cols, width):
    gap = width // max(rows,cols)
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (((width - gap * cols) // 2), i * gap + ((width - gap * rows) // 2)), (width - ((width - gap * cols) // 2), i * gap + ((width - gap * rows) // 2)))
        for j in range(cols + 1):
            pygame.draw.line(win, GREY, (j * gap + ((width - gap * cols) // 2), ((width - gap * rows) // 2)), (j * gap +((width - gap * cols) // 2), width - ((width - gap * rows) // 2)))


def draw(win, grid, rows, cols, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, cols, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, cols, width):
    gap = width // max(rows, cols)
    x, y = pos

    row = (y - ((width - gap * rows) // 2)) // gap
    col = (x - ((width - gap * cols) // 2)) // gap

    return row, col


def main(win, width):

    # UPDATE: datos introducidos por el usuario
    rows = 50
    cols = 50
    # calculamos tamaño de las casillas
    gap = width // max(rows, cols)
    # calculamos espacio margen
    mg = (width - gap * min(rows, cols)) // 2

    grid = make_grid(rows, cols, width)

    start = None
    end = None

    run = True
    while run:

        # actualizamos vista
        draw(win, grid, rows, cols, width)

        # capturamos evento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, cols, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, cols, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, cols, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, cols, width)

    pygame.quit()


main(WIN, DIM)
