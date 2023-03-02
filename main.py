
#
#   PRÁCTICA 1 - INGENIERÍA DEL CONOCIMIENTO
#   ----------------------------------------
#   Realizado por:
#   · Beatriz Espinar Aragón
#   · Steven Mallqui Aguilar
#


import pygame
from queue import PriorityQueue
from AStar import AStar
from Graph import Graph
from Node import Node

DIM = 800
WIN = pygame.display.set_mode((DIM, DIM))
pygame.display.set_caption("A Star Algorithm")

BEIGE = (237, 199, 150)     # Nodos en CERRADA
BROWN = (219, 139, 86)      # Nodos en ABIERTA
WHITE = (255, 255, 255)     # Background
MAROON = (132, 44, 48)      # Nodos barrera (inalcanzables)
BLUE = (155, 191, 209)      # Camino solución
YELLOW = (233, 188, 109)    # Nodo origen
GREY = (128, 128, 128)      # Líneas tablero
GREEN = (132, 167, 37)      # Nodo destino

    # /BEA/ AÑADIR MÉTODOS DE LA CLASE Y ARREGLAR CÓDIGO



def get_clicked_pos(pos, rows, cols):
    gap = DIM // max(rows, cols)
    x, y = pos

    row = (y - ((DIM - gap * rows) // 2)) // gap
    col = (x - ((DIM - gap * cols) // 2)) // gap

    return row, col



def main(win):

    # /BEA/ ARREGLAR: LOS DATOS SON INTRODUCIDOS POR EL USUARIO
    rows = 50
    cols = 50

    g = Graph(rows, cols)

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
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, cols, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, cols, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, cols, width)

    pygame.quit()


main(WIN, DIM)
