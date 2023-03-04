
#
#   PRÁCTICA 1 - INGENIERÍA DEL CONOCIMIENTO
#   ----------------------------------------
#   Realizado por:
#   · Beatriz Espinar Aragón
#   · Steven Mallqui Aguilar
#

#    ¡¡ QUÉ FALTA !!
#    1) Revisar algoritmo
#    2) Añadir botones START, RESET, EXIT
#    3) Añadir pantalla inicial elegir dimensiones

import pygame
from Graph import Graph
import Utilities
from AStar import AStar

WIN = pygame.display.set_mode((Utilities.DIM, Utilities.DIM))
pygame.display.set_caption("A Star Algorithm")

def get_clicked_pos(pos, rows, cols):
    gap = Utilities.DIM // max(rows, cols)
    x, y = pos

    row = (y - ((Utilities.DIM - gap * rows) // 2)) // gap
    col = (x - ((Utilities.DIM - gap * cols) // 2)) // gap

    return row, col



def main(win):

    rows = 50
    cols = 50

    g = Graph(rows, cols)

    start = None
    end = None

    run = True
    while run:

        # actualizamos vista
        g.draw(win)

        # capturamos evento
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT

                # Obtenemos casilla en la que ha pulsado el usuario
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, cols)
                node = g.nodes[row][col]

                # El primer click es START
                if not start and node != end:
                    start = node
                    start.make_start()

                # El segundo click es END
                elif not end and node != start:
                    end = node
                    end.make_end()

                # Los demás clicks son nodos barrera
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT

                # Obtenemos casilla en la que ha pulsado el usuario
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, cols)
                node = g.nodes[row][col]

                # La casilla vuelve a ser blanca
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Ejecutamos algoritmo
                    alg = AStar(g)
                    alg.algorithm(start, end)

    pygame.quit()


main(WIN, Utilities.DIM)
