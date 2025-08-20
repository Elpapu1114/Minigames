import pygame
import sys
import random
import time

pygame.init()
pygame.display.set_caption("Flappy Bird - Pygame")

# ---------------------------
# Colores y FPS
# ---------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (255, 50, 50)
BLUE  = (50, 150, 255)
GRAY  = (180, 180, 180)

FPS = 60

# ---------------------------
# Configuración general
# ---------------------------
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_WIDTH = 80
BIRD_SIZE = 40

# ---------------------------
# Menús seguros
# ---------------------------
def menu_resolucion(screen):
    font = pygame.font.SysFont(None, 36)
    while True:
        screen.fill(BLACK)
        lines = [
            "Elige resolución:",
            "1) 800 x 600",
            "2) 960 x 720",
            "3) 1024 x 768",
            "Presiona 1,2 o 3"
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, WHITE)
            screen.blit(txt, (40, 80 + i*40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == "1":
                    return 800, 600
                if event.unicode == "2":
                    return 960, 720
                if event.unicode == "3":
                    return 1024, 768

# ---------------------------
# Funciones auxiliares
# ---------------------------
def draw_bird(screen, x, y):
    pygame.draw.rect(screen, BLUE, (int(x), int(y), BIRD_SIZE, BIRD_SIZE))

def draw_pipes(screen, pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe["top"])
        pygame.draw.rect(screen, GREEN, pipe["bottom"])

def check_collision(bird_rect, pipes, H):
    if bird_rect.top <= 0 or bird_rect.bottom >= H:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return False

def victory_screen(screen, W, H, score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    waiting = True
    while waiting:
        screen.fill(BLACK)
        txt = font_big.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(txt, (W//2 - txt.get_width()//2, H//2 - 50))
        txt2 = font_small.render("ENTER = volver al menú, ESC = salir", True, WHITE)
        screen.blit(txt2, (W//2 - txt2.get_width()//2, H//2 + 30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def start_countdown(screen, W, H):
    font = pygame.font.SysFont(None, 72)
    for i in range(3,0,-1):
        screen.fill(BLACK)
        txt = font.render(str(i), True, WHITE)
        screen.blit(txt, (W//2 - txt.get_width()//2, H//2 - txt.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)
    # GO!
    screen.fill(BLACK)
    txt = font.render("GO!", True, WHITE)
    screen.blit(txt, (W//2 - txt.get_width()//2, H//2 - txt.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(1000)

# ---------------------------
# Juego principal
# ---------------------------
def run_game(screen, W, H):
    clock = pygame.time.Clock()
    bird_x = W//4
    bird_y = H//2
    bird_vy = 0

    pipes = []
    pipe_timer = 0
    score = 0

    # Countdown inicial
    start_countdown(screen, W, H)

    running = True
    while running:
        dt = clock.tick(FPS)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vy = JUMP_STRENGTH
                if event.key == pygame.K_ESCAPE:
                    return

        # --- Física del pájaro ---
        bird_vy += GRAVITY
        bird_y += bird_vy

        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)

        # --- Obstáculos ---
        pipe_timer += 1
        if pipe_timer > 90:
            pipe_timer = 0
            top_height = random.randint(50, H - PIPE_GAP - 50)
            bottom_height = H - top_height - PIPE_GAP
            pipes.append({
                "top": pygame.Rect(W, 0, PIPE_WIDTH, top_height),
                "bottom": pygame.Rect(W, H-bottom_height, PIPE_WIDTH, bottom_height)
            })

        for pipe in pipes:
            pipe["top"].x -= PIPE_SPEED
            pipe["bottom"].x -= PIPE_SPEED

        # Eliminar pipes fuera de pantalla
        pipes = [p for p in pipes if p["top"].right > 0]

        # Chequear colisiones
        if check_collision(bird_rect, pipes, H):
            victory_screen(screen, W, H, score)
            return

        # Chequear si pasó una tubería
        for pipe in pipes:
            if pipe["top"].right < bird_x and not pipe.get("passed", False):
                pipe["passed"] = True
                score += 1

        # --- Render ---
        screen.fill(BLACK)
        draw_bird(screen, bird_x, bird_y)
        draw_pipes(screen, pipes)

        # Puntaje
        font = pygame.font.SysFont(None, 48)
        txt = font.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(txt, (10,10))

        pygame.display.flip()

# ---------------------------
# Bucle principal
# ---------------------------
def main():
    temp_screen = pygame.display.set_mode((800,600))
    W,H = menu_resolucion(temp_screen)
    screen = pygame.display.set_mode((W,H))

    while True:
        run_game(screen, W, H)
        font = pygame.font.SysFont(None,36)
        waiting = True
        while waiting:
            screen.fill(BLACK)
            msg = font.render("Partida finalizada. ENTER = jugar de nuevo, ESC = salir", True, WHITE)
            screen.blit(msg,(W//2 - msg.get_width()//2,H//2 - 20))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e