import pygame
import sys
import random


pygame.init()
pygame.display.set_caption("Flappy Bird - Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
BIRD_SIZE = 40

fondo_img = pygame.image.load("fondo.png")
bird_img = pygame.image.load("pajaro.png")
pipe_img = pygame.image.load("tuberiapro.png")

bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
PIPE_WIDTH = 60  # Ancho fijo para las tuberías

def draw_background(screen, W, H):
    fondo_escalado = pygame.transform.scale(fondo_img, (W, H))
    screen.blit(fondo_escalado, (0,0))

def draw_bird(screen, x, y):
    screen.blit(bird_img, (int(x), int(y)))

def draw_pipes(screen, pipes):
    for pipe in pipes:
        # Tubo superior - escalar a las dimensiones exactas del rect y voltear
        top_height = pipe["top"].height
        top_scaled = pygame.transform.scale(pipe_img, (PIPE_WIDTH, top_height))
        top_flipped = pygame.transform.flip(top_scaled, False, True)
        screen.blit(top_flipped, (pipe["top"].x, pipe["top"].y))

        # Tubo inferior - escalar a las dimensiones exactas del rect
        bottom_height = pipe["bottom"].height
        bottom_scaled = pygame.transform.scale(pipe_img, (PIPE_WIDTH, bottom_height))
        screen.blit(bottom_scaled, (pipe["bottom"].x, pipe["bottom"].y))

def check_collision(bird_rect, pipes, H):
    if bird_rect.top <= 0 or bird_rect.bottom >= H:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return False

def create_pipe(W, H):
    gap_start = random.randint(50, H - PIPE_GAP - 50)
    return {
        "top": pygame.Rect(W, 0, PIPE_WIDTH, gap_start),
        "bottom": pygame.Rect(W, gap_start + PIPE_GAP, PIPE_WIDTH, H - gap_start - PIPE_GAP)
    }

def move_pipes(pipes):
    for pipe in pipes:
        pipe["top"].x -= PIPE_SPEED
        pipe["bottom"].x -= PIPE_SPEED

def update_score(pipes, bird_x, score):
    for pipe in pipes:
        if pipe["top"].right < bird_x and not pipe.get("passed", False):
            pipe["passed"] = True
            score += 1
    return score

def draw_score(screen, score):
    font = pygame.font.SysFont(None, 48)
    txt = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(txt, (10,10))

def wait_for_start(screen, W, H):
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
        
        draw_background(screen, W, H)
        draw_bird(screen, W//4, H//2)
        
        msg = font.render("Presiona ESPACIO para comenzar", True, WHITE)
        screen.blit(msg, (W//2 - msg.get_width()//2, H//2 + 100))
        
        pygame.display.flip()

def run_game(screen, W, H):
    wait_for_start(screen, W, H)
    
    clock = pygame.time.Clock()
    bird_x = W//4
    bird_y = H//2
    bird_vy = 0
    pipes = []
    pipe_timer = 0
    score = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vy = JUMP_STRENGTH
                if event.key == pygame.K_ESCAPE:
                    return

        bird_vy += GRAVITY
        bird_y += bird_vy
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)

        pipe_timer += 1
        if pipe_timer > 90:
            pipe_timer = 0
            pipes.append(create_pipe(W, H))

        move_pipes(pipes)
        pipes = [p for p in pipes if p["top"].right > 0]

        if check_collision(bird_rect, pipes, H):
            return

        score = update_score(pipes, bird_x, score)

        draw_background(screen, W, H)
        draw_bird(screen, bird_x, bird_y)
        draw_pipes(screen, pipes)
        draw_score(screen, score)

        pygame.display.flip()

def game_over_screen(screen, W, H):
    font = pygame.font.SysFont(None,36)
    while True:
        screen.fill(BLACK)
        msg = font.render("Partida finalizada. ENTER = jugar de nuevo, ESC = salir", True, WHITE)
        screen.blit(msg,(W//2 - msg.get_width()//2,H//2 - 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():
    W,H = 800,600
    screen = pygame.display.set_mode((W,H))

    while True:
        run_game(screen, W, H)
        game_over_screen(screen, W, H)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e