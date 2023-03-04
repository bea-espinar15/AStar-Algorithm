import pygame
from Button import Button

pygame.init()

DIM = 800

screen = pygame.display.set_mode((DIM,DIM))
pygame.display.set_caption('A-STAR')

start_img = pygame.image.load('START.png').convert_alpha()
reset_img = pygame.image.load('RESET.png').convert_alpha()
exit_img = pygame.image.load('EXIT.png').convert_alpha()

#Create button instances
start_button = Button(300, 500, start_img, 0.1)
reset_button = Button(50, 680, reset_img, 0.1)
exit_button = Button(580, 680, exit_img, 0.1)

#game variables
game_started = False

#define fonts
font = pygame.font.SysFont("lucidaconsole", 120)

#define color
TEXT_COL = (0, 0, 0)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#game loop
run = True
while run:
    screen.fill((225, 202, 160))

    if game_started == True:
        reset_button.draw(screen)
        if exit_button.draw(screen):
            run = False
    else:
        draw_text("A-STAR", font, TEXT_COL, 200, 150)
        game_started = start_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()