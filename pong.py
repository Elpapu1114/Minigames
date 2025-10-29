import pygame
import sys
import random
import math
from dataclasses import dataclass

# ---------------------------
# Configuración general
# ---------------------------
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)
GREEN = (0, 200, 0)
YELLOW= (255, 215, 0)
RED   = (255, 50, 50)
BLUE  = (50, 150, 255)

FPS = 120
W, H = 800, 600
WIN_SCORE = 7

# Dificultades CPU mejoradas (más realistas)
DIFICULTADES = {
    "1": ("Fácil",   {"speed_factor": 0.4, "reaction_time": 0.5, "error_chance": 0.3, "prediction_error": 60}),
    "2": ("Media",   {"speed_factor": 0.6, "reaction_time": 0.25, "error_chance": 0.15, "prediction_error": 30}),
    "3": ("Difícil", {"speed_factor": 0.8, "reaction_time": 0.1, "error_chance": 0.05, "prediction_error": 15})
}

# ---------------------------
# Dataclasses
# ---------------------------
@dataclass
class Paddle:
    x: float
    y: float
    w: int
    h: int
    speed: float

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def move(self, dy: float, min_y: int, max_y: int):
        self.y += dy
        if self.y < min_y:
            self.y = min_y
        if self.y + self.h > max_y:
            self.y = max_y - self.h

@dataclass
class Ball:
    x: float
    y: float
    r: int
    vx: float
    vy: float
    color: tuple = WHITE

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r*2, self.r*2)

@dataclass
class AIState:
    target_y: float = 0
    last_ball_x: float = 0
    reaction_timer: float = 0
    error_offset: float = 0
    next_error_time: float = 0

# ---------------------------
# Carga de imágenes
# ---------------------------
def load_image(filename):
    try:
        return pygame.image.load(f"image/{filename}")
    except:
        print(f"Error cargando {filename}")
        return None

# ---------------------------
# Menús seguros
# ---------------------------
def menu_modo(screen):
    img = load_image("menu_eleccion_pong.png")
    if img:
        img = pygame.transform.scale(img, (W, H))
    while True:
        screen.fill(BLACK)
        if img:
            screen.blit(img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ("1","2"):
                    return int(event.unicode)

def menu_dificultad(screen):
    img = load_image("menu_eleccion_dificultad_pong.png")
    if img:
        img = pygame.transform.scale(img, (W, H))
    while True:
        screen.fill(BLACK)
        if img:
            screen.blit(img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in DIFICULTADES:
                    return DIFICULTADES[event.unicode]

# ---------------------------
# Funciones auxiliares
# ---------------------------
def reset_ball(ball: Ball, direction: int, base_speed: float):
    ball.x = W / 2
    ball.y = H / 2
    ball.vx = base_speed * direction
    ball.vy = (base_speed * 0.5) * (1 if random.random() < 0.5 else -1)
    ball.color = WHITE

def draw_center_line(screen, offset):
    dash_h = 16
    gap = 10
    x = W // 2
    y = -offset
    while y < H:
        pygame.draw.rect(screen, GRAY, (x-2, y, 4, dash_h))
        y += dash_h + gap

def draw_score(screen, score_left, score_right):
    font = pygame.font.SysFont(None, 64)
    txtL = font.render(str(score_left), True, WHITE)
    txtR = font.render(str(score_right), True, WHITE)
    screen.blit(txtL, (W*0.25 - txtL.get_width()/2, 20))
    screen.blit(txtR, (W*0.75 - txtR.get_width()/2, 20))

def predict_ball_y(ball: Ball, paddle_x: float) -> float:
    """Predice dónde estará la pelota cuando llegue al paddle"""
    if ball.vx == 0:
        return ball.y
    
    time_to_paddle = (paddle_x - ball.x) / ball.vx
    if time_to_paddle <= 0:
        return ball.y
    
    future_y = ball.y + ball.vy * time_to_paddle
    
    while future_y < 0 or future_y > H:
        if future_y < 0:
            future_y = -future_y
        elif future_y > H:
            future_y = 2*H - future_y
    
    return future_y

def update_ai(ai_state: AIState, ball: Ball, right: Paddle, difficulty: dict, dt: float):
    """Actualiza el comportamiento de la IA de manera más realista"""
    
    ball_approaching = ball.vx > 0
    ball_direction_changed = (ball.x - ai_state.last_ball_x) * ball.vx < 0
    
    ai_state.reaction_timer -= dt
    
    if ball_approaching and (ball_direction_changed or ai_state.reaction_timer <= 0):
        ai_state.reaction_timer = difficulty["reaction_time"]
        
        predicted_y = predict_ball_y(ball, right.x)
        
        if random.random() < difficulty["error_chance"]:
            error_range = difficulty["prediction_error"]
            ai_state.error_offset = random.uniform(-error_range, error_range)
        else:
            ai_state.error_offset *= 0.9
        
        ai_state.target_y = predicted_y + ai_state.error_offset
    
    elif not ball_approaching:
        center_y = H / 2
        ai_state.target_y = center_y + (ai_state.target_y - center_y) * 0.98
    
    ai_state.last_ball_x = ball.x
    
    paddle_center = right.y + right.h / 2
    distance_to_target = ai_state.target_y - paddle_center
    
    if abs(distance_to_target) < 10:
        return 0
    
    max_speed = right.speed * difficulty["speed_factor"]
    desired_speed = distance_to_target * 3
    
    if desired_speed > max_speed:
        desired_speed = max_speed
    elif desired_speed < -max_speed:
        desired_speed = -max_speed
    
    return desired_speed * dt

def victory_screen(screen, winner_name):
    if winner_name == "Jugador 1":
        img = load_image("victoria_jugador_1_pong.png")
    elif winner_name == "Jugador 2":
        img = load_image("victoria_jugador_2_pong.png")
    else:  # CPU
        img = load_image("victoria_cpu_pong.png")
    
    if img:
        img = pygame.transform.scale(img, (W, H))
    
    waiting = True
    while waiting:
        screen.fill(BLACK)
        if img:
            screen.blit(img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

# ---------------------------
# Juego principal
# ---------------------------
def run_game(screen, modo, dificultad_cpu=("Media", {})):
    clock = pygame.time.Clock()
    pad_w = max(10, W // 80)
    pad_h = max(80, H // 5)
    pad_speed = H * 1.0
    ball_r = max(6, W // 160)
    ball_speed = W * 0.4

    left = Paddle(x=30, y=H/2 - pad_h/2, w=pad_w, h=pad_h, speed=pad_speed)
    right = Paddle(x=W-30-pad_w, y=H/2 - pad_h/2, w=pad_w, h=pad_h, speed=pad_speed)
    ball = Ball(x=W/2, y=H/2, r=ball_r, vx=ball_speed, vy=ball_speed * 0.5)

    score_left = 0
    score_right = 0
    running = True
    paused = False
    cpu_name, cpu_difficulty = dificultad_cpu
    ai_state = AIState()
    center_offset = 0
    colors = [WHITE, RED, BLUE, YELLOW, GREEN]

    while running:
        dt = clock.tick(FPS)/1000.0
        center_offset = (center_offset+200*dt) % (16+10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    return

        if paused:
            screen.fill(BLACK)
            draw_center_line(screen, center_offset)
            draw_score(screen, score_left, score_right)
            font = pygame.font.SysFont(None, 48)
            txt = font.render("PAUSA (P=continuar ESC=salir)", True, YELLOW)
            screen.blit(txt, (W//2 - txt.get_width()//2, H//2 - 20))
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        dy_left = 0
        if keys[pygame.K_w]: dy_left -= left.speed*dt
        if keys[pygame.K_s]: dy_left += left.speed*dt
        left.move(dy_left, 0, H)

        dy_right = 0
        if modo==2:
            if keys[pygame.K_UP]: dy_right -= right.speed*dt
            if keys[pygame.K_DOWN]: dy_right += right.speed*dt
        else:
            dy_right = update_ai(ai_state, ball, right, cpu_difficulty, dt)
        
        right.move(dy_right, 0, H)

        ball.x += ball.vx*dt
        ball.y += ball.vy*dt

        if ball.y - ball.r <=0 or ball.y + ball.r >= H:
            ball.vy*=-1
            ball.color = random.choice(colors)

        if ball.rect().colliderect(left.rect()) and ball.vx<0:
            overlap = (ball.y - (left.y + left.h/2)) / (left.h/2)
            ball.vx = abs(ball.vx) * 1.03
            ball.vy += overlap * (ball_speed*0.6)
            ball.color = random.choice(colors)
        if ball.rect().colliderect(right.rect()) and ball.vx>0:
            overlap = (ball.y - (right.y + right.h/2)) / (right.h/2)
            ball.vx = -abs(ball.vx) * 1.03
            ball.vy += overlap * (ball_speed*0.6)
            ball.color = random.choice(colors)

        punto = 0
        if ball.x + ball.r < 0:
            score_right += 1
            punto = -1
        elif ball.x - ball.r > W:
            score_left += 1
            punto = 1
        if punto!=0:
            reset_ball(ball, -punto, ball_speed)
            ai_state.target_y = H / 2
            ai_state.error_offset = 0

        winner = None
        if score_left>=WIN_SCORE:
            winner = "Jugador 1"
        if score_right>=WIN_SCORE:
            winner = "CPU" if modo==1 else "Jugador 2"
        if winner:
            victory_screen(screen, winner)
            return

        screen.fill(BLACK)
        draw_center_line(screen, center_offset)
        pygame.draw.rect(screen, WHITE, left.rect(), border_radius=6)
        pygame.draw.rect(screen, WHITE, right.rect(), border_radius=6)
        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), ball.r)
        draw_score(screen, score_left, score_right)

        small = pygame.font.SysFont(None, 24)
        if modo==1:
            info = f"CPU: {cpu_name} - P=pausa ESC=menú"
        else:
            info = "2 Jugadores (W/S y ↑/↓) - P=pausa ESC=menú"
        info_txt = small.render(info, True, GRAY)
        screen.blit(info_txt, (W//2 - info_txt.get_width()//2, H-30))
        pygame.display.flip()

# ---------------------------
# Bucle principal
# ---------------------------
def main():
    pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pong - Pygame")
    screen = pygame.display.get_surface()

    while True:
        img_menu = load_image("menu_pong.png")
        if img_menu:
            img_menu = pygame.transform.scale(img_menu, (W, H))
        waiting = True
        while waiting:
            screen.fill(BLACK)
            if img_menu:
                screen.blit(img_menu, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

        modo = menu_modo(screen)
        dificultad = ("Media", DIFICULTADES["2"][1])
        if modo==1:
            dificultad = menu_dificultad(screen)
        run_game(screen, modo, dificultad)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e