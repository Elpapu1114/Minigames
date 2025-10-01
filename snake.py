import pygame
import random
import sys
import math
import os

pygame.init()

# Tamaño de celda y pantalla
CELL_SIZE = 20
WIDTH, HEIGHT = 600, 400

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)  # Color para la cuadrícula
APPLE_RED = (220, 20, 20)  # Rojo más realista para la manzana
APPLE_GREEN = (34, 139, 34)  # Verde para la hoja
DARK_RED = (139, 0, 0)  # Rojo más oscuro para sombras

# Pantalla y reloj
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 🍎")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Cargar imagen de la manzana
def cargar_imagen_manzana():
    """Carga la imagen de la manzana desde la carpeta img"""
    try:
        # Crear la ruta completa a la imagen
        ruta_imagen = os.path.join(os.path.dirname(__file__), 'img', 'manzana.png')
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_imagen):
            manzana_img = pygame.image.load(ruta_imagen).convert_alpha()
            # Escalar la imagen al tamaño de la celda
            manzana_img = pygame.transform.scale(manzana_img, (CELL_SIZE-2, CELL_SIZE-2))
            print(f"Imagen cargada exitosamente desde: {ruta_imagen}")
            return manzana_img
        else:
            print(f"No se encontró la imagen en: {ruta_imagen}")
            return None
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

# Cargar la imagen al iniciar el programa
manzana_img = cargar_imagen_manzana()

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_apple(pos):
    """Dibuja la manzana usando la imagen cargada o un diseño de respaldo"""
    x, y = pos
    
    if manzana_img:
        # Usar la imagen si está disponible
        screen.blit(manzana_img, (x+1, y+1))
    else:
        # Dibujo de respaldo si no se puede cargar la imagen
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Cuerpo principal de la manzana (círculo rojo)
        pygame.draw.circle(screen, APPLE_RED, (center_x, center_y), radius)
        
        # Sombra/highlight para darle volumen
        pygame.draw.circle(screen, DARK_RED, (center_x + 2, center_y + 2), radius - 3)
        
        # Brillo en la parte superior izquierda
        highlight_pos = (center_x - 3, center_y - 3)
        pygame.draw.circle(screen, (255, 100, 100), highlight_pos, radius // 3)
        
        # Tallo pequeño en la parte superior
        stem_x = center_x
        stem_y = y + 2
        pygame.draw.rect(screen, (101, 67, 33), (stem_x - 1, stem_y, 2, 4))
        
        # Hoja pequeña
        leaf_points = [
            (stem_x + 2, stem_y + 1),
            (stem_x + 6, stem_y - 1),
            (stem_x + 4, stem_y + 3),
            (stem_x + 2, stem_y + 2)
        ]
        pygame.draw.polygon(screen, APPLE_GREEN, leaf_points)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def generate_food(snake_body):
    grid_w = WIDTH // CELL_SIZE
    grid_h = HEIGHT // CELL_SIZE
    while True:
        x = random.randint(0, grid_w - 1) * CELL_SIZE
        y = random.randint(0, grid_h - 1) * CELL_SIZE
        if (x, y) not in snake_body:
            return (x, y)

def get_speed(score):
    base_speed = 10
    increase_every = 5
    max_speed = 35
    return min(base_speed + (score // increase_every) * 2, max_speed)

def wait_for_start():
    """Pantalla de inicio - espera que el jugador presione ESPACIO"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
        
        # Dibujar pantalla de inicio
        screen.fill(BLACK)
        draw_grid()
        
        # Título grande
        title_text = "SNAKE GAME 🍎"
        title_surface = font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(title_surface, title_rect)
        
        # Instrucciones
        instruction_text = "Presiona ESPACIO para empezar"
        instruction_surface = font.render(instruction_text, True, GREEN)
        instruction_rect = instruction_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(instruction_surface, instruction_rect)
        
        # Controles
        controls_text = "Usa las flechas para moverte"
        controls_surface = font.render(controls_text, True, WHITE)
        controls_rect = controls_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        screen.blit(controls_surface, controls_rect)
        
        pygame.display.update()
        clock.tick(30)

def main():
    # Mostrar pantalla de inicio
    wait_for_start()
    
    snake_pos = (100, 100)
    snake_body = [snake_pos]
    direction = "RIGHT"
    food_pos = generate_food(snake_body)
    score = 0

    # --- DIBUJAR ESTADO INICIAL ---
    screen.fill(BLACK)
    draw_grid()
    draw_snake(snake_body)
    draw_apple(food_pos)  # Dibujar la manzana
    draw_text("Puntaje: " + str(score), WHITE, 10, 10)
    draw_text("🍎", WHITE, 10, 45)  # Emoji decorativo
    pygame.display.update()

    # Pequeña pausa antes de empezar el movimiento
    pygame.time.wait(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        x, y = snake_pos
        if direction == "UP":
            y -= CELL_SIZE
        elif direction == "DOWN":
            y += CELL_SIZE
        elif direction == "LEFT":
            x -= CELL_SIZE
        elif direction == "RIGHT":
            x += CELL_SIZE

        snake_pos = (x, y)
        snake_body.insert(0, snake_pos)

        if snake_pos == food_pos:
            score += 1
            food_pos = generate_food(snake_body)
        else:
            snake_body.pop()

        if (
            x < 0 or x >= WIDTH or
            y < 0 or y >= HEIGHT or
            snake_pos in snake_body[1:]
        ):
            # Pantalla de Game Over
            screen.fill(BLACK)
            draw_text("GAME OVER!", RED, WIDTH//2 - 100, HEIGHT//2 - 60)
            draw_text("Puntaje Final: " + str(score), WHITE, WIDTH//2 - 120, HEIGHT//2 - 20)
            draw_text("🍎 Manzanas comidas: " + str(score), WHITE, WIDTH//2 - 140, HEIGHT//2 + 20)
            draw_text("Presiona ESPACIO para jugar otra vez", GREEN, WIDTH//2 - 180, HEIGHT//2 + 60)
            pygame.display.update()
            
            # Esperar a que presione ESPACIO para reiniciar
            waiting_restart = True
            while waiting_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting_restart = False
                            main()  # Reiniciar el juego
                clock.tick(30)

        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake_body)
        draw_apple(food_pos)  # Dibujar la manzana en su posición
        draw_text("Puntaje: " + str(score), WHITE, 10, 10)
        draw_text("🍎", WHITE, 10, 45)  # Emoji decorativo
        pygame.display.update()

        clock.tick(get_speed(score))

if __name__ == "__main__":
    main()