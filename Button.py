
#
#   CLASE BOTÓN
#   -----------
#   Representa un botón, lo dibuja y detecta si ha sido pulsado
#

import pygame


class Button:

    # Constructor:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        # Proporciones imagen
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Dibuja el botón y devuelve si ha sido pulsado
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
