
#
#   PRÁCTICA 1 - INGENIERÍA DEL CONOCIMIENTO
#   ----------------------------------------
#   Realizado por:
#   · Beatriz Espinar Aragón
#   · Steven Mallqui Aguilar
#

#    ¡¡ QUÉ FALTA !!
#    1) Comparar algoritmo con enunciado
#    2) Añadir pantalla inicial elegir dimensiones
#    3) Mostrar msj error si no hay camino posible
#    4) Ampliaciones
#    5) Memoria y manual
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
        self.win = pygame.display.set_mode((Utilities.SCREENWIDTH, Utilities.SCREENWIDTH))
        # Imágenes
        self.start_img = pygame.image.load('resources/START.png').convert_alpha()
        self.reset_img = pygame.image.load('resources/RESET.png').convert_alpha()
        self.exit_img = pygame.image.load('resources/EXIT.png').convert_alpha()
        # Botones
        self.start_button = Button(300, 500, self.start_img, 0.1)
        self.resume_button = Button(310, 680, self.start_img, 0.1)
        self.reset_button = Button(60, 680, self.reset_img, 0.1)
        self.exit_button = Button(550, 680, self.exit_img, 0.1)
        # Color
        self.game_started = False
        # Datos del algoritmo
        self.g = None  # Grafo
        self.rows = ''
        self.cols = ''
        self.startNode = None  # Nodo inicio
        self.endNode = None  # Nodo destino
        self.path = False

    # MÉTODOS PRIVADOS
    # ----------------

    # Dibuja texto
    def draw_text(self, text, x, y, font):
        img = font.render(text, True, Utilities.BLACK)
        self.win.blit(img, (x, y))

    # A partir de la posición pos de la pantalla obtiene la fila y columna
    # correspondiente del tablero. False si está fuera de los límites
    def get_clicked_pos(self, pos):
        x, y = pos
        gap = Utilities.DIM // max(self.rows, self.cols)
        margin_v = Utilities.HEADER + ((Utilities.DIM - gap * self.rows) // 2)
        margin_h = Utilities.MARGIN + ((Utilities.DIM - gap * self.cols) // 2)

        if margin_h < x < margin_h + gap * self.cols and margin_v < y < margin_v + gap * self.rows:
            row = (y - ((Utilities.DIM - gap * self.rows) // 2) - Utilities.HEADER) // gap
            col = (x - ((Utilities.DIM - gap * self.cols) // 2) - Utilities.MARGIN) // gap

            return True, row, col

        return False, -1, -1

    # Inicio de la aplicación
    def start(self):
        pygame.init()
        pygame.display.set_caption("A Star Algorithm")
        font = pygame.font.SysFont("lucidaconsole", 120)
        font_input = pygame.font.SysFont("lucidaconsole", 60)
        rows_rect = pygame.Rect(150,350,200,70)
        cols_rect = pygame.Rect(450,350,200,70)
        color_rect = pygame.Color('Gray')
        active_rows = False
        active_cols = False

        while not self.game_started:
            self.win.fill(Utilities.LIGHT_YELLOW)

            self.draw_text("A-STAR", 200, 150, font)
            self.game_started = self.start_button.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rows_rect.collidepoint(event.pos):
                        active_rows = True
                        active_cols = False
                    elif cols_rect.collidepoint(event.pos):
                        active_rows = False
                        active_cols = True
                if event.type == pygame.KEYDOWN and active_rows:
                    self.rows += event.unicode
                if event.type == pygame.KEYDOWN and active_cols:
                    self.cols += event.unicode
            pygame.draw.rect(self.win, color_rect, rows_rect)
            pygame.draw.rect(self.win, color_rect, cols_rect)
            text_rows = font_input.render(self.rows, True, (255, 255, 255))
            text_cols = font_input.render(self.cols, True, (255, 255, 255))
            self.win.blit(text_rows, (rows_rect.x + 5, rows_rect.y + 5))
            self.win.blit(text_cols, (cols_rect.x + 5, cols_rect.y + 5))
            pygame.display.update()

        return True

    def reset(self):
        self.g = Graph(self.rows, self.cols)
        self.startNode = None
        self.endNode = None
        self.path = False


    # Acción botón izq sobre tablero
    def left(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        if valid and not self.path:
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

        if valid and not self.path:
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

        run = True
        while run:
            run = self.start()
            if not run:
                run = False
                continue

            self.win.fill(Utilities.LIGHT_YELLOW)
            font = pygame.font.SysFont("lucidaconsole", 30)
            self.draw_text("A-STAR", 340, 18, font)

            self.g = Graph(int(self.rows), int(self.cols))

            self.startNode = None
            self.endNode = None

            while run:

                # actualizamos vista
                self.g.draw(self.win)

                # capturamos evento
                for event in pygame.event.get():

                    if event.type == pygame.QUIT or self.exit_button.draw(self.win):
                        run = False
                        break

                    if self.reset_button.draw(self.win):
                        self.reset()

                    if pygame.mouse.get_pressed()[0]:  # LEFT
                        self.left()

                    elif pygame.mouse.get_pressed()[2]:  # RIGHT
                        self.right()

                    if self.resume_button.draw(self.win) and self.startNode and self.endNode:
                        # Ejecutamos algoritmo
                        alg = AStar(self.g, self.startNode, self.endNode)
                        run, self.path = alg.algorithm(self.win)
                        if not run:
                            break
                        if not self.path:
                            pass

        pygame.quit()
        sys.exit()


# Ejecutamos main
m = Main()
m.main()
