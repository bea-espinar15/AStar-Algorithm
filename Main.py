
#
#   PRÁCTICA 1 - INGENIERÍA DEL CONOCIMIENTO
#   ----------------------------------------
#   Realizado por:
#   · Beatriz Espinar Aragón
#   · Steven Mallqui Aguilar
#

#    ¡¡ QUÉ FALTA !!
#    1) Comparar algoritmo con enunciado
#    2) Añadir botones START, RESET, EXIT
#    3) Añadir pantalla inicial elegir dimensiones
#    4) Comprobar pos dentro del tablero dentro de get_clicked_pos
#    5) Mostrar msj error si no hay camino posible
#    6) Terminar función h() en AStar.py
#

import sys
import pygame
import Utilities
from Button import Button
from Graph import Graph
from AStar import AStar


class Main:

    # Constructor
    def __init__(self):
        # Pantalla
        self.win = pygame.display.set_mode((Utilities.DIM, Utilities.DIM))
        # Imágenes
        self.start_img = pygame.image.load('resources/START.png').convert_alpha()
        self.reset_img = pygame.image.load('resources/RESET.png').convert_alpha()
        self.exit_img = pygame.image.load('resources/EXIT.png').convert_alpha()
        # Botones
        self.start_button = Button(300, 500, self.start_img, 0.1)
        self.reset_button = Button(50, 680, self.reset_img, 0.1)
        self.exit_button = Button(580, 680, self.exit_img, 0.1)
        # Fuente de letra
        self.font = None
        # Color
        self.game_started = False
        # Datos del algoritmo
        self.g = None  # Grafo
        self.rows = None
        self.cols = None
        self.startNode = None  # Nodo inicio
        self.endNode = None  # Nodo destino?

    # MÉTODOS PRIVADOS
    # ----------------

    # Dibuja el titulo
    def draw_text(self, text, x, y):
        img = self.font.render(text, True, Utilities.BLACK)
        self.win.blit(img, (x, y))

    # A partir de la posición pos de la pantalla obtiene la fila y columna
    # correspondiente del tablero. False si está fuera de los límites
    def get_clicked_pos(self, pos):
        gap = Utilities.DIM // max(self.rows, self.cols)
        x, y = pos

        row = (y - ((Utilities.DIM - gap * self.rows) // 2)) // gap
        col = (x - ((Utilities.DIM - gap * self.cols) // 2)) // gap

        return True, row, col

    # Inicio de la aplicación
    def start(self):
        pygame.init()
        pygame.display.set_caption("A Star Algorithm")
        self.font = pygame.font.SysFont("lucidaconsole", 120)

        while not self.game_started:
            self.win.fill(Utilities.LIGHT_YELLOW)

            self.draw_text("A-STAR", 200, 150)
            self.game_started = self.start_button.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            pygame.display.update()

        return True

    # Acción botón izq sobre tablero
    def left(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        if valid:
            node = self.g.get_nodes()[row][col]

            # El primer click es START
            if not self.startNode and node != self.endNode:
                self.startNode = node
                node.make_start()

            # El segundo click es END
            elif not self.endNode and node != self.startNode:
                self.endNode = node
                node.make_end()

            # Los demás clicks son nodos barrera
            elif node != self.endNode and node != self.startNode:
                node.make_barrier()

    # Acción boton dcho sobre tablero
    def right(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        if valid:
            node = self.g.get_nodes()[row][col]

            # La casilla vuelve a ser blanca
            node.reset()
            if node == self.startNode:
                self.startNode = None
            elif node == self.endNode:
                self.endNode = None

    # MÉTODOS PÚBLICOS
    # ----------------

    def main(self):

        while True:
            run = self.start()
            if not run:
                break

            self.reset_button.draw(self.win)
            if self.exit_button.draw(self.win):
                break

            self.rows = 50
            self.cols = 50

            self.g = Graph(self.rows, self.cols)

            self.startNode = None
            self.endNode = None

            while True:

                # actualizamos vista
                self.g.draw(self.win)

                # capturamos evento
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        run = False
                        break

                    if pygame.mouse.get_pressed()[0]:  # LEFT
                        self.left()

                    elif pygame.mouse.get_pressed()[2]:  # RIGHT
                        self.right()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.startNode and self.endNode:
                            # Ejecutamos algoritmo
                            alg = AStar(self.g, self.startNode, self.endNode)
                            run, path = alg.algorithm(self.win)
                            if not run:
                                break
                            if not path:
                                pass

                if not run:
                    break

        pygame.quit()
        sys.exit()


# Ejecutamos main
m = Main()
m.main()
