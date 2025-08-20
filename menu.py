import pygame
import button

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650

game_paused = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont("arialblack", 60)

TEXT_COL = (255, 255, 255)

play_img = pygame.image.load("C:/Users/Usuario/Desktop/pollo/play.png").convert_alpha()
options_img = pygame.image.load("C:/Users/Usuario/Desktop/pollo/options.png").convert_alpha()
exit_img = pygame.image.load("C:/Users/Usuario/Desktop/pollo/exit.png").convert_alpha()

play_button = button.Button(304,125,play_img,1)
options_button = button.Button(297, 250, options_img,1)
exit_button = button.Button(336, 375, exit_img,1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



run = True
while run:
    screen.fill((3, 186, 252))
    

    if game_paused == True:
        if play_button.draw(screen):
            game_paused = False
        play_button.draw(screen)
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
