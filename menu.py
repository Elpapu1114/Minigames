import pygame
from button import Button
import os
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650

game_paused = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont("arialblack", 60)

TEXT_COL = (255, 255, 255)

def crear_ruta_img(nombre_imagen):
    return os.path.join(os.path.dirname(__file__), 'img', nombre_imagen)
play_img = pygame.image.load(crear_ruta_img("play.png")).convert_alpha()
options_img = pygame.image.load(crear_ruta_img("options.png")).convert_alpha()
exit_img = pygame.image.load(crear_ruta_img("exit.png")).convert_alpha()
video_img = pygame.image.load(crear_ruta_img("video.png")).convert_alpha()
audio_img = pygame.image.load(crear_ruta_img("audio.png")).convert_alpha()
keys_img = pygame.image.load(crear_ruta_img("keys.png")).convert_alpha()
back_img = pygame.image.load(crear_ruta_img("back.png")).convert_alpha()

play_button = Button(180,125,play_img,10)
options_button = Button(720, 125, options_img,10)
exit_button = Button(455, 375, exit_img,10)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


run = True
while run:
    screen.fill((3, 186, 252))
    

    if game_paused == True:
        if play_button.draw(screen):
            game_paused = False
        if options_button.draw(screen):
            game_paused = False
        if exit_button.draw(screen):
            run = False
    else:
        draw_text("Presiona ESC para pausar", font, TEXT_COL, 160, 250)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True

    pygame.display.update()

pygame.quit()