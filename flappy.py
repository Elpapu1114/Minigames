import pygame
import sys
import random


pygame.init()
pygame.display.set_caption("Flappy Bird - Pygame")

from display_config import init_display

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
# BIRD_SIZE will be computed after we know the display size so it scales with resolution

# Inicializar pantalla con resolucion desde game_settings.json
screen, W, H = init_display(default_w=800, default_h=600, title="Flappy Bird - Pygame")

fondo_img = pygame.image.load("image/fondo.png").convert()
bird_img = pygame.image.load("image/pajaro.png").convert_alpha()
pipe_img = pygame.image.load("image/tuberiapro.png").convert_alpha()
menu_img = pygame.image.load("image/menu_flappy.png").convert()
game_over_img = pygame.image.load("image/game_over_flappy.png").convert()

# Scale assets that depend on resolution once (avoid per-frame scaling)
BIRD_SIZE = max(24, int(H * 0.06))
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
PIPE_WIDTH = max(32, int(W * 0.06))

fondo_escalado = pygame.transform.scale(fondo_img, (W, H))
menu_escalado = pygame.transform.scale(menu_img, (W, H))
game_over_escalado = pygame.transform.scale(game_over_img, (W, H))

# Pre-create a font for score (avoid creating every frame)
FONT_SCORE = pygame.font.SysFont(None, max(20, int(H * 0.05)))

def draw_background(screen, W, H):
    # Use the pre-scaled background to avoid costly transforms each frame
    screen.blit(fondo_escalado, (0, 0))

def draw_bird(screen, x, y):
    screen.blit(bird_img, (int(x), int(y)))

def draw_pipes(screen, pipes):
    for pipe in pipes:
        # If surfaces were created at pipe creation, reuse them (much faster)
        if pipe.get("top_surf") is not None:
            top_surf = pipe["top_surf"]
            top_rect = top_surf.get_rect(topleft=(pipe["top"].x, pipe["top"].y))
            screen.blit(top_surf, top_rect)
        else:
            top_height = pipe["top"].height
            top_scaled = pygame.transform.scale(pipe_img, (PIPE_WIDTH, top_height))
            top_flipped = pygame.transform.flip(top_scaled, False, True)
            screen.blit(top_flipped, (pipe["top"].x, pipe["top"].y))

        if pipe.get("bottom_surf") is not None:
            bottom_surf = pipe["bottom_surf"]
            bottom_rect = bottom_surf.get_rect(topleft=(pipe["bottom"].x, pipe["bottom"].y))
            screen.blit(bottom_surf, bottom_rect)
        else:
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
    top_rect = pygame.Rect(W, 0, PIPE_WIDTH, gap_start)
    bottom_rect = pygame.Rect(W, gap_start + PIPE_GAP, PIPE_WIDTH, H - gap_start - PIPE_GAP)

    # Create scaled surfaces for these specific heights once
    top_scaled = pygame.transform.scale(pipe_img, (PIPE_WIDTH, top_rect.height))
    top_flipped = pygame.transform.flip(top_scaled, False, True)
    bottom_scaled = pygame.transform.scale(pipe_img, (PIPE_WIDTH, bottom_rect.height))

    return {
        "top": top_rect,
        "bottom": bottom_rect,
        "top_surf": top_flipped,
        "bottom_surf": bottom_scaled
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
    txt = FONT_SCORE.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(txt, (10, 10))

def countdown_screen(screen, W, H, bird_x, bird_y):
    """Muestra un contador de 3 segundos antes de iniciar el juego"""
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 120)
    
    for count in range(3, 0, -1):
        start_time = pygame.time.get_ticks()
        
        while pygame.time.get_ticks() - start_time < 1000:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            
            draw_background(screen, W, H)
            draw_bird(screen, bird_x, bird_y)
            
            txt = font.render(str(count), True, WHITE)
            txt_rect = txt.get_rect(center=(W//2, H//2))
            
            shadow = font.render(str(count), True, BLACK)
            shadow_rect = shadow.get_rect(center=(W//2 + 3, H//2 + 3))
            screen.blit(shadow, shadow_rect)
            screen.blit(txt, txt_rect)
            
            pygame.display.flip()
    
    return True

def wait_for_start(screen, W, H):
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
        
        # Use pre-scaled menu background
        screen.blit(menu_escalado, (0, 0))
        
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
    
    # Mostrar contador de 3 segundos
    if not countdown_screen(screen, W, H, bird_x, bird_y):
        return score

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vy = JUMP_STRENGTH
                if event.key == pygame.K_ESCAPE:
                    return score

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
            return score

        score = update_score(pipes, bird_x, score)

        draw_background(screen, W, H)
        draw_bird(screen, bird_x, bird_y)
        draw_pipes(screen, pipes)
        draw_score(screen, score)

        pygame.display.flip()

def game_over_screen(screen, W, H, final_score):
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        
        # Use pre-scaled game over background
        screen.blit(game_over_escalado, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():

    while True:
        final_score = run_game(screen, W, H)
        game_over_screen(screen, W, H, final_score)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e