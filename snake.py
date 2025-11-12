def get_curve_image(dir_from_prev, dir_to_next):
    """Retorna el nombre de la imagen de curva correcta según las direcciones"""
    # Mapear las combinaciones de direcciones a las imágenes de curva
    curve_map = {
        ("RIGHT", "DOWN"): 'curva_derecha_abajo',
        ("RIGHT", "UP"): 'curva_derecha_arriba',
        ("LEFT", "DOWN"): 'curva_izquierda_abajo',
        ("LEFT", "UP"): 'curva_izquierda_arriba',
        ("DOWN", "RIGHT"): 'curva_abajo_derecha',
        ("DOWN", "LEFT"): 'curva_abajo_izquierda',
        ("UP", "RIGHT"): 'curva_arriba_derecha',
        ("UP", "LEFT"): 'curva_arriba_izquierda',
    }
    return curve_map.get((dir_from_prev, dir_to_next), None)
import pygame
import random
import sys
import math
import os


pygame.init()

from display_config import init_display

# Tamaño de celda y pantalla
CELL_SIZE = 20
# Inicializar pantalla usando game_settings.json
screen, WIDTH, HEIGHT = init_display(default_w=800, default_h=600, title="Snake")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
APPLE_RED = (220, 20, 20)
APPLE_GREEN = (34, 139, 34)
DARK_RED = (139, 0, 0)

# Pantalla y reloj
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Cargar imágenes
def cargar_imagenes():
    """Carga todas las imágenes del juego"""
    imagenes = {}
    carpeta_img = os.path.join(os.path.dirname(__file__), 'image')
    
    nombres = {
        'manzana': 'manzana.png',
        'menu': 'menu_snake.png',
        'game_over': 'game_over_snake.png',
        'cabeza': 'snake_head.png',
        'cuerpo': 'snake_body.png',
        'cola': 'snake_tail.png',
        'curva_abajo_izquierda': 'snake_curve_abajo_izquierda.png',
        'curva_abajo_derecha': 'snake_curve_abajo_derecha.png',
        'curva_arriba_izquierda': 'snake_curve_arriba_izquierda.png',
        'curva_arriba_derecha': 'snake_curve_arriba_derecha.png',
        'curva_izquierda_abajo': 'snake_curve_izquierda_abajo.png',
        'curva_izquierda_arriba': 'snake_curve_izquierda_arriba.png',
        'curva_derecha_abajo': 'snake_curve_derecha_abajo.png',
        'curva_derecha_arriba': 'snake_curve_derecha_arriba.png'
    }
    
    for key, nombre in nombres.items():
        try:
            ruta = os.path.join(carpeta_img, nombre)
            if os.path.exists(ruta):
                img = pygame.image.load(ruta).convert_alpha()
                
                # Escalar según el tipo de imagen
                if key in ['menu', 'game_over']:
                    # Escalar fondos exactamente al tamaño de la pantalla
                    imagenes[key] = pygame.transform.scale(img, (WIDTH, HEIGHT))
                else:
                    # Escalar partes de la serpiente y manzana al tamaño de la celda
                    imagenes[key] = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
                print(f"✓ {key} cargada")
            else:
                print(f"✗ No se encontró: {ruta}")
                imagenes[key] = None
        except Exception as e:
            print(f"Error cargando {key}: {e}")
            imagenes[key] = None
    
    return imagenes

# Cargar todas las imágenes
imagenes = cargar_imagenes()

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def get_direction_from_positions(pos1, pos2):
    """Obtiene la dirección desde pos1 hacia pos2"""
    x1, y1 = pos1
    x2, y2 = pos2
    
    if x2 > x1:
        return "RIGHT"
    elif x2 < x1:
        return "LEFT"
    elif y2 > y1:
        return "DOWN"
    elif y2 < y1:
        return "UP"
    return "RIGHT"

def get_direction_angle(direction):
    """Retorna el ángulo de rotación para cada dirección (cabeza mira a la izquierda por defecto)"""
    angles = {
        "RIGHT": 180,
        "DOWN": 270,
        "LEFT": 0,
        "UP": 90
    }
    return angles.get(direction, 0)

def get_tail_angle(direction):
    """Retorna el ángulo de rotación para la cola (mirando al lado contrario)"""
    angles = {
        "RIGHT": 0,
        "DOWN": 90,
        "LEFT": 180,
        "UP": 270
    }
    return angles.get(direction, 0)

def draw_snake(snake_body, current_direction):
    """Dibuja la serpiente con imágenes de cabeza, cuerpo, cola y curvas"""
    if not snake_body:
        return
    
    for i, pos in enumerate(snake_body):
        x, y = pos
        
        if i == 0:  # Cabeza - siempre mira a donde se está moviendo
            if imagenes['cabeza']:
                angle = get_direction_angle(current_direction)
                rotated = pygame.transform.rotate(imagenes['cabeza'], -angle)
                rect = rotated.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                screen.blit(rotated, rect)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        
        elif i == len(snake_body) - 1:  # Cola
            if imagenes['cola'] and len(snake_body) > 1:
                # Dirección desde el penúltimo segmento hacia la cola
                prev_pos = snake_body[i-1]
                tail_direction = get_direction_from_positions(prev_pos, pos)
                angle = get_tail_angle(tail_direction)
                rotated = pygame.transform.rotate(imagenes['cola'], -angle)
                rect = rotated.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                screen.blit(rotated, rect)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        
        else:  # Cuerpo
            if len(snake_body) > 2:
                prev_pos = snake_body[i-1]
                next_pos = snake_body[i+1]
                
                dir_from_prev = get_direction_from_positions(prev_pos, pos)
                dir_to_next = get_direction_from_positions(pos, next_pos)
                
                # Verificar si es una curva
                if dir_from_prev != dir_to_next:
                    # Es una curva
                    curve_key = get_curve_image(dir_from_prev, dir_to_next)
                    if curve_key and imagenes.get(curve_key):
                        screen.blit(imagenes[curve_key], (x, y))
                    else:
                        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    # Es un segmento recto
                    if imagenes['cuerpo']:
                        if dir_from_prev in ["RIGHT", "LEFT"]:
                            angle = 0  # Horizontal
                        else:
                            angle = 90  # Vertical
                        
                        rotated = pygame.transform.rotate(imagenes['cuerpo'], -angle)
                        rect = rotated.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                        screen.blit(rotated, rect)
                    else:
                        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

def draw_apple(pos):
    """Dibuja la manzana usando la imagen cargada o un diseño de respaldo"""
    x, y = pos
    
    if imagenes['manzana']:
        screen.blit(imagenes['manzana'], (x, y))
    else:
        # Dibujo de respaldo
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(screen, APPLE_RED, (center_x, center_y), radius)
        pygame.draw.circle(screen, DARK_RED, (center_x + 2, center_y + 2), radius - 3)
        highlight_pos = (center_x - 3, center_y - 3)
        pygame.draw.circle(screen, (255, 100, 100), highlight_pos, radius // 3)

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
    """Pantalla de inicio con imagen de menú"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        screen.fill(BLACK)
        
        # Si existe la imagen de menú, mostrarla
        if imagenes['menu']:
            screen.blit(imagenes['menu'], (0, 0))
        else:
            # Menú de respaldo
            draw_grid()
            draw_text("SNAKE GAME", WHITE, WIDTH//2 - 100, HEIGHT//2 - 60)
            draw_text("ESPACIO PARA JUGAR", GREEN, WIDTH//2 - 140, HEIGHT//2)
            draw_text("ESC PARA SALIR", WHITE, WIDTH//2 - 100, HEIGHT//2 + 40)
        
        pygame.display.update()
        clock.tick(30)

def main():
    wait_for_start()
    
    snake_pos = (100, 100)
    snake_body = [snake_pos]
    direction = "RIGHT"
    next_direction = "RIGHT"  # Dirección siguiente para cambios suave
    food_pos = generate_food(snake_body)
    score = 0

    # Dibujar estado inicial
    screen.fill(BLACK)
    draw_grid()
    draw_snake(snake_body, direction)
    draw_apple(food_pos)
    draw_text("Puntaje: " + str(score), WHITE, 10, 10)
    pygame.display.update()
    pygame.time.wait(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    next_direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Actualizar dirección
        direction = next_direction

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

        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or snake_pos in snake_body[1:]):
            # Pantalla de Game Over con imagen
            screen.fill(BLACK)
            
            if imagenes['game_over']:
                # Mostrar la imagen de game over
                screen.blit(imagenes['game_over'], (0, 0))
            else:
                # Game Over de respaldo
                draw_text("GAME OVER!", RED, WIDTH//2 - 100, HEIGHT//2 - 60)
                draw_text("Puntaje Final: " + str(score), WHITE, WIDTH//2 - 120, HEIGHT//2 - 20)
                draw_text("ESPACIO PARA JUGAR", GREEN, WIDTH//2 - 140, HEIGHT//2 + 60)
                draw_text("ESC PARA SALIR", WHITE, WIDTH//2 - 100, HEIGHT//2 + 100)
            
            pygame.display.update()
            
            waiting_restart = True
            while waiting_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                clock.tick(30)

        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake_body, direction)
        draw_apple(food_pos)
        draw_text("Puntaje: " + str(score), WHITE, 10, 10)
        pygame.display.update()

        clock.tick(get_speed(score))

if __name__ == "__main__":
    main()