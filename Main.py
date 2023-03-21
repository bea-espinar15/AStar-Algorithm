
#
#   PRÁCTICA 1 - INGENIERÍA DEL CONOCIMIENTO
#   ----------------------------------------
#   Realizado por:
#   · Beatriz Espinar Aragón
#   · Steven Mallqui Aguilar
#   · Rogger Huayllasco De la Cruz
#
#   --> Implementación del algoritmo A*
#

#
#   CLASE MAIN
#   ----------
#   Controla el flujo principal de la aplicación:
#   · Genera la pantalla inicial, donde se introducen los parámetros de tamaño del tablero
#   · Genera la pantalla principal, donde se ejecuta el algoritmo.
#
#   --> Controles
#       · 1º click izquierdo: casilla origen
#       · 2º click izquierdo: casilla destino
#       · Siguientes clicks izquierdos: casillas inalcanzables
#       · Click derecho: resetear casilla
#       · Tecla 'W': waypoint
#       · Tecla 'R': casilla peligrosa
#


import sys
import pygame
import Utilities
from Button import Button
from Graph import Graph
from AStar import AStar
from tkinter import messagebox


class Main:

    # Constructor:
    def __init__(self):
        # Pantalla
        self.win = pygame.display.set_mode((Utilities.SCREENWIDTH, Utilities.SCREENWIDTH))
        # Imágenes
        self.start_img = pygame.image.load('resources/START.png').convert_alpha()
        self.reset_img = pygame.image.load('resources/RESET.png').convert_alpha()
        self.exit_img = pygame.image.load('resources/EXIT.png').convert_alpha()
        # Botones
        self.start_button = Button(300, 600, self.start_img, 0.1)
        self.resume_button = Button(310, 680, self.start_img, 0.1)
        self.reset_button = Button(60, 680, self.reset_img, 0.1)
        self.exit_button = Button(550, 680, self.exit_img, 0.1)
        # Datos del algoritmo
        self.g = None  # Grafo
        self.rows = ''
        self.cols = ''
        self.risk = ''
        self.start_node = None  # Nodo inicio
        self.end_node = None  # Nodo destino
        self.waypoints = set()  # Waypoints
        self.risk_nodes = set()  # Casillas peligrosas
        # Otros
        self.game_started = False  # Pantalla inicial
        self.path = False  # ¿Se ha ejecutado el algoritmo?

    # MÉTODOS PRIVADOS
    # ----------------

    # Dibuja el texto "text" en la posición (x,y) con la fuente <font>
    def draw_text(self, text, x, y, font):
        img = font.render(text, True, Utilities.BLACK)
        self.win.blit(img, (x, y))

    # A partir de la posición <pos> de la pantalla obtiene la fila y columna
    # correspondiente del tablero. False si está fuera de los límites
    def get_clicked_pos(self, pos):
        x, y = pos
        gap = Utilities.DIM // max(self.rows, self.cols)  # tamaño casilla
        margin_v = Utilities.HEADER + ((Utilities.DIM - gap * self.rows) // 2)
        margin_h = Utilities.MARGIN + ((Utilities.DIM - gap * self.cols) // 2)

        # Si está dentro de los límites calculamos fila y columna
        if margin_h < x < margin_h + gap * self.cols and margin_v < y < margin_v + gap * self.rows:
            row = (y - ((Utilities.DIM - gap * self.rows) // 2) - Utilities.HEADER) // gap
            col = (x - ((Utilities.DIM - gap * self.cols) // 2) - Utilities.MARGIN) // gap
            return True, row, col

        return False, -1, -1

    # Pantalla inicial de la aplicación
    def start(self):
        pygame.init()
        pygame.display.set_caption("A Star Algorithm")

        # Resetear parámetros
        self.game_started = False
        self.rows = ''
        self.cols = ''
        self.risk = ''

        # Fuente
        font = pygame.font.SysFont("lucidaconsole", 120)
        font_input = pygame.font.SysFont("lucidaconsole", 50)

        # Input fields
        rows_rect = pygame.Rect(130, 320, 200, 70)
        cols_rect = pygame.Rect(470, 320, 200, 70)
        risk_rect = pygame.Rect(300, 480, 200, 70)
        color_rect = pygame.Color('Gray')
        # ¿Se ha pulsado en los input fields?
        active_rows = False
        active_cols = False
        active_risk = False

        # Mientras no se pulse START
        while not self.game_started:

            while not self.game_started:
                self.win.fill(Utilities.LIGHT_YELLOW)  # Background
                self.draw_text("A-STAR", 200, 100, font)  # Título

                self.game_started = self.start_button.draw(self.win)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    # Sólo se puede escribir en los campos si se ha pulsado en ellos
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rows_rect.collidepoint(event.pos):
                            active_rows = True
                            active_cols = False
                            active_risk = False
                        elif cols_rect.collidepoint(event.pos):
                            active_rows = False
                            active_cols = True
                            active_risk = False
                        elif risk_rect.collidepoint(event.pos):
                            active_rows = False
                            active_cols = False
                            active_risk = True

                    # Escribir o borrar texto
                    if event.type == pygame.KEYDOWN:
                        if active_rows:
                            if event.key == pygame.K_BACKSPACE:
                                self.rows = self.rows[:-1]
                            else:
                                self.rows += event.unicode
                        elif active_cols:
                            if event.key == pygame.K_BACKSPACE:
                                self.cols = self.cols[:-1]
                            else:
                                self.cols += event.unicode
                        elif active_risk:
                            if event.key == pygame.K_BACKSPACE:
                                self.risk = self.risk[:-1]
                            else:
                                self.risk += event.unicode

                # Draw input fields
                self.draw_text("ROWS:", 130, 260, font_input)
                self.draw_text("COLS:", 470, 260, font_input)
                self.draw_text("RISK:", 300, 420, font_input)
                pygame.draw.rect(self.win, color_rect, rows_rect)
                pygame.draw.rect(self.win, color_rect, cols_rect)
                pygame.draw.rect(self.win, color_rect, risk_rect)
                text_rows = font_input.render(self.rows, True, (255, 255, 255))
                text_cols = font_input.render(self.cols, True, (255, 255, 255))
                text_risk = font_input.render(self.risk, True, (255, 255, 255))
                self.win.blit(text_rows, (rows_rect.x + 7, rows_rect.y + 12))
                self.win.blit(text_cols, (cols_rect.x + 7, cols_rect.y + 12))
                self.win.blit(text_risk, (risk_rect.x + 7, risk_rect.y + 12))

                pygame.display.update()

            # Comprobamos valores introducidos
            try:
                self.rows = int(self.rows)
                self.cols = int(self.cols)
                self.risk = int(self.risk)
                if self.rows <= 0 or self.cols <= 0 or self.risk < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror('Error', 'Rows and Columns must be integers greater than 0, '
                                              'and Risk must be 0 or more.')
                self.game_started = False
                self.rows = ''
                self.cols = ''
                self.risk = ''

        return True

    # Inicializa la pantalla principal
    def initialize(self):
        self.win.fill(Utilities.LIGHT_YELLOW)
        font = pygame.font.SysFont("lucidaconsole", 30)
        self.draw_text("A-STAR", 340, 18, font)

        self.rows = int(self.rows)
        self.cols = int(self.cols)
        self.risk = int(self.risk)
        self.g = Graph(self.rows, self.cols)  # Creación del grafo

        self.start_node = None
        self.end_node = None
        self.waypoints = set()
        self.risk_nodes = set()
        self.path = False

    def reset(self):
        self.g = Graph(self.rows, self.cols)
        self.start_node = None
        self.end_node = None
        self.waypoints = set()
        self.risk_nodes = set()
        self.path = False

    # Acción botón izq sobre tablero
    def left(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        # Si está dentro de los límites y no se ha ejecutado el algoritmo
        if valid and not self.path:
            node = self.g.get_nodes()[row][col]
            # El primer click es START
            if not self.start_node and node != self.end_node:
                if node in self.waypoints:
                    self.waypoints.remove(node)
                elif node in self.risk_nodes:
                    self.risk_nodes.remove(node)
                self.start_node = node
                node.make_start()
            # El segundo click es END
            elif not self.end_node and node != self.start_node:
                if node in self.waypoints:
                    self.waypoints.remove(node)
                elif node in self.risk_nodes:
                    self.risk_nodes.remove(node)
                self.end_node = node
                node.make_end()
            # Los demás clicks son nodos barrera
            elif node != self.end_node and node != self.start_node:
                if node in self.waypoints:
                    self.waypoints.remove(node)
                elif node in self.risk_nodes:
                    self.risk_nodes.remove(node)
                node.make_barrier()

    # Acción botón dcho sobre tablero
    def right(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        # Si está dentro de los límites y no se ha ejecutado el algoritmo
        if valid and not self.path:
            node = self.g.get_nodes()[row][col]
            # La casilla vuelve a ser blanca
            node.reset()
            if node == self.start_node:
                self.start_node = None
            elif node == self.end_node:
                self.end_node = None
            elif node in self.waypoints:
                self.waypoints.remove(node)
            elif node in self.risk_nodes:
                self.risk_nodes.remove(node)

    # Añadir waypoint
    def add_waypoint(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        # Si está dentro de los límites y no se ha ejecutado el algoritmo
        if valid and not self.path:
            node = self.g.get_nodes()[row][col]
            if node != self.end_node and node != self.start_node:
                if node in self.risk_nodes:
                    self.risk_nodes.remove(node)
                node.make_waypoint()
                self.waypoints.add(node)

    # Añadir casilla peligrosa
    def add_risk(self):
        # Obtenemos casilla en la que ha pulsado el usuario
        pos = pygame.mouse.get_pos()
        valid, row, col = self.get_clicked_pos(pos)

        # Si está dentro de los límites y no se ha ejecutado el algoritmo
        if valid and not self.path:
            node = self.g.get_nodes()[row][col]
            if node != self.end_node and node != self.start_node:
                if node in self.waypoints:
                    self.waypoints.remove(node)
                node.make_risky()
                self.risk_nodes.add(node)

    # MÉTODOS PÚBLICOS
    # ----------------

    def main(self):

        run = True
        while run:
            run = self.start()
            if not run:
                break
            self.initialize()

            while run:

                # Actualizamos vista
                self.g.draw(self.win)

                # Capturamos evento
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        run = False
                        break

                    if self.exit_button.draw(self.win):  # Volvemos a la pantalla inicial
                        run = self.start()
                        if not run:
                            break
                        self.initialize()

                    if self.reset_button.draw(self.win):  # Reseteamos
                        self.reset()

                    if pygame.mouse.get_pressed()[0]:  # Botón izquierdo
                        self.left()

                    elif pygame.mouse.get_pressed()[2]:  # Botón derecho
                        self.right()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:  # Tecla W -> Waypoint
                            self.add_waypoint()
                        elif event.key == pygame.K_r:  # Tecla R -> Risk (casilla peligrosa)
                            self.add_risk()

                    if self.resume_button.draw(self.win) and self.start_node and self.end_node:
                        # Ejecutamos algoritmo
                        alg = AStar(self.g, self.start_node, self.end_node, self.waypoints, self.risk, self.risk_nodes)
                        run, self.path = alg.algorithm(self.win)
                        if not run:
                            break
                        if not self.path:
                            messagebox.showerror('Error', 'No way found')
                            self.reset()

        pygame.quit()
        sys.exit()


# Ejecutamos main
m = Main()
m.main()
 