import pygame
import sys
import random

if __name__ == "__main__":
    pygame.init()
    

# -------------------
# Configuración
# -------------------
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5

# Resolución (igual que en Pong)
WIDTH, HEIGHT = COLS * SQUARE_SIZE, (ROWS+1) * SQUARE_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 en Línea Animado")

# Colores
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
YELLOW= (255, 255, 0)
GRAY  = (180, 180, 180)

FPS = 60
clock = pygame.time.Clock()

# -------------------
# Funciones del tablero
# -------------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(SCREEN, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(SCREEN, color, (c*SQUARE_SIZE + SQUARE_SIZE//2, (r+1)*SQUARE_SIZE + SQUARE_SIZE//2), RADIUS)
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
    x = col * SQUARE_SIZE + SQUARE_SIZE//2
    y = SQUARE_SIZE//2
    color = RED if piece == 1 else YELLOW
    while y < (target_row+1)*SQUARE_SIZE + SQUARE_SIZE//2:
        SCREEN.fill(BLACK)
        draw_board(board)
        pygame.draw.circle(SCREEN, color, (x, int(y)), RADIUS)
        pygame.display.update()
        y += 20  # velocidad de caída
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
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    return False

# -------------------
# Menús tipo Pong
# -------------------
def menu_jugadores(screen):
    font = pygame.font.SysFont(None, 40)
    while True:
        screen.fill(BLACK)
        lines = [
            "Elige número de jugadores:",
            "1) 1 Jugador vs CPU",
            "2) 2 Jugadores",
            "Presiona 1 o 2"
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, GRAY)
            screen.blit(txt, (40, 80 + i*50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ("1","2"):
                    return int(event.unicode)

def menu_dificultad(screen):
    font = pygame.font.SysFont(None, 40)
    while True:
        screen.fill(BLACK)
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
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ("1","2","3"):
                    factor = {"1":0.4,"2":0.7,"3":1.0}[event.unicode]
                    return factor

# -------------------
# Lógica del juego
# -------------------
def run_game(screen, players=2, cpu_factor=0.5):
    board = create_board()
    game_over = False
    turn = 0
    font = pygame.font.SysFont(None, 50)

    while True:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_pos = event.pos[0]
                col = x_pos // SQUARE_SIZE
                if (players == 2) or (players==1 and turn==0):
                    if is_valid_location(board, col):
                        piece = 1 if turn==0 else 2
                        drop_piece_animated(board, col, piece)
                        if winning_move(board, piece):
                            game_over = True
                            winner = "Jugador 1" if piece==1 else ("CPU" if players==1 else "Jugador 2")
                        turn = (turn+1)%2

        # CPU movimiento si es 1 jugador
        if players==1 and turn==1 and not game_over:
            pygame.time.delay(3000)  # espera 3 segundos antes de jugar
            valid_cols = [c for c in range(COLS) if is_valid_location(board,c)]
            col = random.choice(valid_cols)
            drop_piece_animated(board, col, 2)
            if winning_move(board, 2):
                game_over = True
                winner = "CPU"
            turn = 0

        # Fin de partida
        if game_over:
            draw_board(board)  # mostrar tablero final
            pygame.time.delay(3000)  # 3 segundos mostrando cómo quedó
            SCREEN.fill(BLACK)
            msg_txt = font.render(f"{winner} gana!", True, RED if winner=="Jugador 1" else YELLOW)
            SCREEN.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, HEIGHT//2 - msg_txt.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        pygame.display.update()

# -------------------
# Main
# -------------------
def main():
    while True:
        jugadores = menu_jugadores(SCREEN)
        cpu_dificultad = 0.5
        if jugadores == 1:
            cpu_dificultad = menu_dificultad(SCREEN)

        run_game(SCREEN, jugadores, cpu_dificultad)

if __name__ == "__main__":
    main()
