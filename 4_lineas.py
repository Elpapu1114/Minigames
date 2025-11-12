import pygame
import sys
import random
import os

pygame.init()

from display_config import init_display

ROWS, COLS = 6, 7

# Inicializar pantalla con resolucion desde game_settings.json
SCREEN, WIDTH, HEIGHT = init_display(default_w=700, default_h=700, title="4 en Línea Animado")

# Constantes base y helpers de escalado
BASE_ANCHO = 700
BASE_ALTO = 700
SCALE_X = WIDTH / BASE_ANCHO
SCALE_Y = HEIGHT / BASE_ALTO

def sx(v):
    return int(v * SCALE_X)

def sy(v):
    return int(v * SCALE_Y)

# Tablero escalado dinámicamente según espacio disponible
# Calcular tamaño para que quepa en la pantalla (dejando margen para menús/texto)
_available_width = WIDTH - sx(50)  # Margen izquierdo/derecho
_available_height = HEIGHT - sy(150)  # Margen superior/inferior
SQUARE_SIZE = min(int(_available_width / COLS), int(_available_height / ROWS))
# Asegurar que no sea demasiado pequeño
SQUARE_SIZE = max(40, SQUARE_SIZE)
RADIUS = SQUARE_SIZE // 2 - 5

# Calcular offset para centrar el tablero
BOARD_WIDTH = SQUARE_SIZE * COLS
BOARD_HEIGHT = SQUARE_SIZE * ROWS
BOARD_OFFSET_X = (WIDTH - BOARD_WIDTH) // 2
BOARD_OFFSET_Y = (HEIGHT - BOARD_HEIGHT) // 2 - sy(20)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
YELLOW= (255, 255, 0)
GRAY  = (180, 180, 180)

FPS = 60
clock = pygame.time.Clock()

# Cargar imágenes
def cargar_imagen(nombre_archivo):
    """Intenta cargar una imagen, si falla devuelve None"""
    try:
        ruta = os.path.join("image", nombre_archivo)
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (WIDTH, HEIGHT))
    except:
        return None

# Cargar todas las imágenes
IMG_MENU = cargar_imagen("menu_4_lineas.png")
IMG_MENU_ELECCION = cargar_imagen("menu_eleccion_4_lineas.png")
IMG_MENU_DIFICULTAD = cargar_imagen("menu_seleccion_dificultad_4_lineas.png")
IMG_VICTORIA_J1 = cargar_imagen("victoria_jugador_1_4_lineas.png")
IMG_VICTORIA_J2 = cargar_imagen("victoria_jugador_2_4_lineas.png")
IMG_VICTORIA_CPU = cargar_imagen("victoria_cpu_4_lineas.png")
IMG_EMPATE = cargar_imagen("empate_4_lineas.png")

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            x = BOARD_OFFSET_X + c*SQUARE_SIZE
            y = BOARD_OFFSET_Y + (r+1)*SQUARE_SIZE
            pygame.draw.rect(SCREEN, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(SCREEN, color, (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), RADIUS)
    pygame.display.update()

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1

def drop_piece_animated(board, col, piece):
    """Hace que la ficha caiga animada hasta su posición final."""
    target_row = get_next_open_row(board, col)
    x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE//2
    y = BOARD_OFFSET_Y + SQUARE_SIZE//2
    color = RED if piece == 1 else YELLOW
    while y < BOARD_OFFSET_Y + (target_row+1)*SQUARE_SIZE + SQUARE_SIZE//2:
        SCREEN.fill(BLACK)
        draw_board(board)
        pygame.draw.circle(SCREEN, color, (x, int(y)), RADIUS)
        pygame.display.update()
        y += sy(20)  
        clock.tick(FPS)
    board[target_row][col] = piece

def winning_move(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Diagonal positiva
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    # Diagonal negativa
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    return False

def is_board_full(board):
    """Verifica si el tablero está lleno (empate)"""
    return all(board[0][c] != 0 for c in range(COLS))

def menu_jugadores(screen):
    """Menú para seleccionar número de jugadores"""
    while True:
        if IMG_MENU_ELECCION:
            screen.blit(IMG_MENU_ELECCION, (0, 0))
        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 40)
            lines = [
                "Elige número de jugadores:",
                "1) 2 Jugadores",
                "2) 1 Jugador vs CPU",
                "Presiona 1 o 2"
            ]
            for i, line in enumerate(lines):
                txt = font.render(line, True, GRAY)
                screen.blit(txt, (40, 80 + i*50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == "1":
                    return 2  # 2 jugadores
                elif event.unicode == "2":
                    return 1  # 1 jugador vs CPU
                if event.key == pygame.K_ESCAPE:
                    return None

def menu_dificultad(screen):
    """Menú para seleccionar dificultad de la CPU"""
    while True:
        if IMG_MENU_DIFICULTAD:
            screen.blit(IMG_MENU_DIFICULTAD, (0, 0))
        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 40)
            lines = [
                "Elige dificultad CPU:",
                "1) Fácil",
                "2) Media",
                "3) Difícil",
                "Presiona 1, 2 o 3"
            ]
            for i, line in enumerate(lines):
                txt = font.render(line, True, GRAY)
                screen.blit(txt, (40, 80 + i*50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ("1","2","3"):
                    factor = {"1":0.4,"2":0.7,"3":1.0}[event.unicode]
                    return factor
                if event.key == pygame.K_ESCAPE:
                    return None

def mostrar_pantalla_victoria(screen, winner, players):
    """Muestra la pantalla de victoria con la imagen correspondiente"""
    # Seleccionar imagen según el ganador
    if winner == "Empate":
        imagen = IMG_EMPATE
    elif winner == "Jugador 1":
        imagen = IMG_VICTORIA_J1
    elif winner == "CPU":
        imagen = IMG_VICTORIA_CPU
    else:  # Jugador 2
        imagen = IMG_VICTORIA_J2
    
    # Mostrar imagen o texto de respaldo
    if imagen:
        screen.blit(imagen, (0, 0))
    else:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        msg_txt = font.render(f"{winner} gana!", True, RED if winner=="Jugador 1" else YELLOW)
        screen.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, HEIGHT//2 - msg_txt.get_height()//2))
    
    pygame.display.flip()
    pygame.time.wait(3000)

def run_game(screen, players=2, cpu_factor=0.5):
    board = create_board()
    game_over = False
    turn = 0
    winner = None

    while True:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Volver al menú principal
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_pos = event.pos[0]
                # Restar el offset para obtener la columna correcta
                col = (x_pos - BOARD_OFFSET_X) // SQUARE_SIZE
                # Verificar que el clic esté dentro del tablero
                if 0 <= col < COLS:
                    if (players == 2) or (players==1 and turn==0):
                        if is_valid_location(board, col):
                            piece = 1 if turn==0 else 2
                            drop_piece_animated(board, col, piece)
                            if winning_move(board, piece):
                                game_over = True
                                winner = "Jugador 1" if piece==1 else ("CPU" if players==1 else "Jugador 2")
                            elif is_board_full(board):
                                game_over = True
                                winner = "Empate"
                            turn = (turn+1)%2

        # Turno de la CPU
        if players==1 and turn==1 and not game_over:
            pygame.time.delay(1000)  
            valid_cols = [c for c in range(COLS) if is_valid_location(board,c)]
            if valid_cols:
                col = random.choice(valid_cols)
                drop_piece_animated(board, col, 2)
                if winning_move(board, 2):
                    game_over = True
                    winner = "CPU"
                elif is_board_full(board):
                    game_over = True
                    winner = "Empate"
                turn = 0

        if game_over:
            draw_board(board)  
            pygame.time.delay(1000) 
            mostrar_pantalla_victoria(screen, winner, players)
            return

        pygame.display.update()

def menu_principal(screen):
    """Menú principal del juego"""
    while True:
        if IMG_MENU:
            screen.blit(IMG_MENU, (0, 0))
        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 60)
            title = font.render("4 EN LÍNEA", True, (255, 165, 0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
            
            font_small = pygame.font.SysFont(None, 35)
            play_text = font_small.render("ESPACIO PARA JUGAR", True, GRAY)
            exit_text = font_small.render("ESC PARA SALIR", True, GRAY)
            screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2))
            screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        
        clock.tick(30)

def main():
    while True:
        # Mostrar menú principal
        if not menu_principal(SCREEN):
            break
        
        # Seleccionar número de jugadores
        jugadores = menu_jugadores(SCREEN)
        if jugadores is None:
            continue
        
        # Si es vs CPU, seleccionar dificultad
        cpu_dificultad = 0.5
        if jugadores == 1:
            cpu_dificultad = menu_dificultad(SCREEN)
            if cpu_dificultad is None:
                continue

        # Ejecutar el juego
        run_game(SCREEN, jugadores, cpu_dificultad)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()