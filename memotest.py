import pygame
import sys
import random
import time
import math

pygame.init()

pygame.display.set_caption("Memotest Pro - Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 215, 0)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
PURPLE = (138, 43, 226)
ORANGE = (255, 140, 0)
PINK = (255, 20, 147)
CYAN = (0, 206, 209)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)

FPS = 60
W, H = 800, 600

def create_particles(x, y, color):
    particles = []
    for _ in range(15):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        particles.append({
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': 1.0,
            'color': color
        })
    return particles

def update_particles(particles, dt):
    for particle in particles[:]:
        particle['x'] += particle['vx'] * dt * 60
        particle['y'] += particle['vy'] * dt * 60
        particle['vy'] += 5 * dt
        particle['life'] -= dt * 2
        if particle['life'] <= 0:
            particles.remove(particle)

def draw_particles(screen, particles):
    for particle in particles:
        size = max(1, int(particle['life'] * 4))
        try:
            pos = (int(particle['x']), int(particle['y']))
            pygame.draw.circle(screen, particle['color'], pos, size)
        except:
            pass

def create_card(x, y, w, h, color, symbol):
    return {
        'rect': pygame.Rect(x, y, w, h),
        'color': color,
        'symbol': symbol,
        'flipped': False,
        'matched': False,
        'hover': False,
        'flip_progress': 0.0,
        'scale': 1.0,
        'glow_intensity': 0.0
    }

def update_card(card, dt):
    target_flip = 1.0 if (card['flipped'] or card['matched']) else 0.0
    if card['flip_progress'] != target_flip:
        speed = 8.0
        if card['flip_progress'] < target_flip:
            card['flip_progress'] = min(target_flip, card['flip_progress'] + speed * dt)
        else:
            card['flip_progress'] = max(target_flip, card['flip_progress'] - speed * dt)
    
    target_scale = 1.1 if card['hover'] and not card['matched'] else 1.0
    if card['scale'] != target_scale:
        scale_speed = 5.0
        if card['scale'] < target_scale:
            card['scale'] = min(target_scale, card['scale'] + scale_speed * dt)
        else:
            card['scale'] = max(target_scale, card['scale'] - scale_speed * dt)
    
    if card['matched']:
        card['glow_intensity'] = (math.sin(time.time() * 3) + 1) / 2

def draw_card(screen, card):
    center_x = card['rect'].centerx
    center_y = card['rect'].centery
    scaled_w = int(card['rect'].width * card['scale'])
    scaled_h = int(card['rect'].height * card['scale'])
    scaled_rect = pygame.Rect(0, 0, scaled_w, scaled_h)
    scaled_rect.center = (center_x, center_y)
    
    if card['matched'] and card['glow_intensity'] > 0:
        glow_color = tuple(min(255, c + int(50 * card['glow_intensity'])) for c in card['color'])
        glow_rect = scaled_rect.inflate(6, 6)
        pygame.draw.rect(screen, glow_color, glow_rect, border_radius=8)
    
    shadow_rect = scaled_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=8)
    
    if card['flip_progress'] > 0.5:
        card_color = card['color']
        border_color = WHITE
    else:
        card_color = DARK_GRAY if not card['hover'] else GRAY
        border_color = LIGHT_GRAY
    
    pygame.draw.rect(screen, card_color, scaled_rect, border_radius=8)
    pygame.draw.rect(screen, border_color, scaled_rect, width=3, border_radius=8)
    
    if card['flip_progress'] > 0.5 and card['symbol']:
        font_size = min(scaled_w, scaled_h) // 3
        font = pygame.font.Font(None, font_size)
        text = font.render(card['symbol'], True, WHITE)
        text_rect = text.get_rect(center=scaled_rect.center)
        screen.blit(text, text_rect)
    
    elif card['flip_progress'] <= 0.5:
        pattern_color = tuple(min(255, c + 30) for c in card_color)
        for i in range(3):
            for j in range(3):
                dot_x = scaled_rect.x + (i + 1) * scaled_rect.width // 4
                dot_y = scaled_rect.y + (j + 1) * scaled_rect.height // 4
                pygame.draw.circle(screen, pattern_color, (dot_x, dot_y), 3)

def menu_principal(screen):
    try:
        menu_image = pygame.image.load("image/menu_memotest.png")
        use_image = True
    except:
        use_image = False
    
    while True:
        if use_image:
            scaled_image = pygame.transform.scale(menu_image, (W, H))
            screen.blit(scaled_image, (0, 0))
        else:
            for y in range(H):
                color = (0, 0, min(100, y // 6))
                pygame.draw.line(screen, color, (0, y), (W, y))
            
            font_title = pygame.font.Font(None, 72)
            title = font_title.render("MEMOTEST PRO", True, GOLD)
            title_rect = title.get_rect(center=(W//2, H//2 - 100))
            
            shadow = font_title.render("MEMOTEST PRO", True, DARK_GRAY)
            shadow_rect = shadow.get_rect(center=(title_rect.centerx + 3, title_rect.centery + 3))
            screen.blit(shadow, shadow_rect)
            screen.blit(title, title_rect)
            
            font_options = pygame.font.Font(None, 48)
            space_text = font_options.render("ESPACIO = Jugar", True, LIME)
            space_rect = space_text.get_rect(center=(W//2, H//2 + 50))
            screen.blit(space_text, space_rect)
            
            esc_text = font_options.render("ESC = Salir", True, RED)
            esc_rect = esc_text.get_rect(center=(W//2, H//2 + 100))
            screen.blit(esc_text, esc_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def menu_modo(screen):
    font_title = pygame.font.Font(None, 48)
    font_options = pygame.font.Font(None, 36)
    
    while True:
        for y in range(H):
            color = (0, min(100, y // 6), 0)
            pygame.draw.line(screen, color, (0, y), (W, y))
        
        title = font_title.render("SELECCIONAR MODO", True, LIME)
        title_rect = title.get_rect(center=(W//2, 100))
        
        shadow = font_title.render("SELECCIONAR MODO", True, DARK_GRAY)
        shadow_rect = shadow.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
        screen.blit(shadow, shadow_rect)
        screen.blit(title, title_rect)
        
        options = [
            "Elige modo de juego:",
            "",
            "1) Un Jugador (vs CPU)",
            "2) Dos Jugadores",
            "",
            "Presiona 1 o 2"
        ]
        
        for i, option in enumerate(options):
            if option:
                color = CYAN if option.startswith(("1)", "2)")) else WHITE
                text = font_options.render(option, True, color)
                text_rect = text.get_rect(center=(W//2, 180 + i*40))
                screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ("1", "2"):
                    return int(event.unicode)

def create_board(rows=4, cols=5):
    total_cards = rows * cols
    
    card_data = [
        (RED, "♥"), (GREEN, "♠"), (BLUE, "♦"), (PURPLE, "♣"),
        (ORANGE, "★"), (PINK, "●"), (CYAN, "▲"), (LIME, "■"),
        (GOLD, "♪"), (WHITE, "◆")
    ]
    
    pairs = (card_data * 2)[:total_cards]
    random.shuffle(pairs)
    
    margin = 20
    card_w = min(120, (W - margin * (cols + 1)) // cols)
    card_h = min(150, (H - 100 - margin * (rows + 1)) // rows)
    
    board_w = cols * card_w + (cols - 1) * margin
    board_h = rows * card_h + (rows - 1) * margin
    start_x = (W - board_w) // 2
    start_y = (H - board_h) // 2 - 25
    
    cards = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (card_w + margin)
            y = start_y + r * (card_h + margin)
            color, symbol = pairs[idx]
            cards.append(create_card(x, y, card_w, card_h, color, symbol))
            idx += 1
    
    return cards

def draw_hud(screen, modo, score1, score2, turn, moves, time_elapsed):
    hud_rect = pygame.Rect(0, H - 80, W, 80)
    pygame.draw.rect(screen, (20, 20, 40), hud_rect)
    pygame.draw.line(screen, WHITE, (0, H - 80), (W, H - 80), 2)
    
    font = pygame.font.Font(None, 32)
    
    if modo == 1:
        score_text = f"Jugador: {score1}"
        cpu_text = f"CPU: {score2}"
        moves_text = f"Movimientos: {moves}"
        
        texts = [score_text, cpu_text, moves_text]
        spacing = W // len(texts)
        
        for i, text in enumerate(texts):
            color = YELLOW if (i == 0 and turn == 1) or (i == 1 and turn == 2) else WHITE
            rendered = font.render(text, True, color)
            x = spacing * i + spacing // 2 - rendered.get_width() // 2
            screen.blit(rendered, (x, H - 50))
    else:
        p1_text = f"Jugador 1: {score1}"
        p2_text = f"Jugador 2: {score2}"
        turn_text = f"Turno: Jugador {turn}"
        
        color1 = YELLOW if turn == 1 else WHITE
        p1_rendered = font.render(p1_text, True, color1)
        screen.blit(p1_rendered, (20, H - 50))
        
        color2 = YELLOW if turn == 2 else WHITE
        p2_rendered = font.render(p2_text, True, color2)
        screen.blit(p2_rendered, (W - p2_rendered.get_width() - 20, H - 50))
        
        turn_rendered = font.render(turn_text, True, CYAN)
        turn_x = W // 2 - turn_rendered.get_width() // 2
        screen.blit(turn_rendered, (turn_x, H - 50))

class CPUPlayer:
    def __init__(self, difficulty='medium'):
        self.memory = {}
        self.difficulty = difficulty
        self.last_seen = {}
    
    def remember_card(self, card_index, color):
        self.memory[card_index] = color
        self.last_seen[card_index] = time.time()
    
    def choose_card(self, cards, first_card_idx=None):
        available = [i for i, c in enumerate(cards) if not c['flipped'] and not c['matched']]
        
        if not available:
            return None
        
        if first_card_idx is not None:
            first_color = cards[first_card_idx]['color']
            
            for idx in available:
                if idx in self.memory and self.memory[idx] == first_color:
                    if random.random() < 0.8:
                        return idx
        
        known_cards = [idx for idx in available if idx in self.memory]
        if known_cards and random.random() < 0.6:
            return random.choice(known_cards)
        
        return random.choice(available)

def run_game(screen, modo):
    clock = pygame.time.Clock()
    
    rows, cols = 4, 5
    cards = create_board(rows, cols)
    
    first_card = None
    second_card = None
    first_card_idx = None
    second_card_idx = None
    checking = False
    check_time = 0
    matched_count = 0
    moves = 0
    
    score1 = 0
    score2 = 0
    turn = 1
    
    cpu = CPUPlayer() if modo == 1 else None
    cpu_thinking = False
    cpu_think_start = 0
    cpu_first_card = None
    
    all_particles = []
    start_time = time.time()
    
    preview_time = 3.0
    preview_start = time.time()
    for card in cards:
        card['flipped'] = True
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        current_time = time.time()
        time_elapsed = current_time - start_time
        
        if current_time - preview_start > preview_time and preview_time > 0:
            for card in cards:
                if not card['matched']:
                    card['flipped'] = False
            preview_time = 0
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not checking and preview_time == 0:
                if modo == 1 and turn == 2:
                    continue
                
                for i, card in enumerate(cards):
                    if card['rect'].collidepoint(mouse_pos) and not card['flipped'] and not card['matched']:
                        card['flipped'] = True
                        if first_card is None:
                            first_card = card
                            first_card_idx = i
                            if cpu:
                                cpu.remember_card(i, card['color'])
                        elif second_card is None:
                            second_card = card
                            second_card_idx = i
                            if cpu:
                                cpu.remember_card(i, card['color'])
                            checking = True
                            check_time = current_time
                            moves += 1
                        break
        
        if modo == 1 and turn == 2 and not checking and preview_time == 0:
            if not cpu_thinking:
                cpu_thinking = True
                cpu_think_start = current_time
                cpu_first_card = None
            
            elif current_time - cpu_think_start > 1.0:
                if first_card is None:
                    idx = cpu.choose_card(cards)
                    if idx is not None:
                        cards[idx]['flipped'] = True
                        first_card = cards[idx]
                        first_card_idx = idx
                        cpu.remember_card(idx, cards[idx]['color'])
                        cpu_thinking = False
                        cpu_think_start = current_time
                
                elif second_card is None and current_time - cpu_think_start > 1.0:
                    idx = cpu.choose_card(cards, first_card_idx)
                    if idx is not None:
                        cards[idx]['flipped'] = True
                        second_card = cards[idx]
                        second_card_idx = idx
                        cpu.remember_card(idx, cards[idx]['color'])
                        checking = True
                        check_time = current_time
                        moves += 1
                        cpu_thinking = False
        
        for card in cards:
            if modo == 1 and turn == 2:
                card['hover'] = False
            else:
                card['hover'] = card['rect'].collidepoint(mouse_pos) and not card['flipped'] and not card['matched'] and preview_time == 0
        
        if checking and current_time - check_time > 1.0:
            if first_card['color'] == second_card['color']:
                first_card['matched'] = True
                second_card['matched'] = True
                matched_count += 2
                
                particles1 = create_particles(first_card['rect'].centerx, first_card['rect'].centery, first_card['color'])
                particles2 = create_particles(second_card['rect'].centerx, second_card['rect'].centery, second_card['color'])
                all_particles.extend(particles1)
                all_particles.extend(particles2)
                
                if turn == 1:
                    score1 += 1
                else:
                    score2 += 1
            else:
                first_card['flipped'] = False
                second_card['flipped'] = False
                turn = 2 if turn == 1 else 1
            
            first_card = None
            second_card = None
            first_card_idx = None
            second_card_idx = None
            checking = False
            cpu_thinking = False
        
        for card in cards:
            update_card(card, dt)
        
        update_particles(all_particles, dt)
        
        for y in range(H - 80):
            intensity = int(20 + 15 * math.sin(time_elapsed * 0.5 + y * 0.01))
            color = (intensity, intensity // 2, intensity // 3)
            pygame.draw.line(screen, color, (0, y), (W, y))
        
        for card in cards:
            draw_card(screen, card)
        
        draw_particles(screen, all_particles)
        
        draw_hud(screen, modo, score1, score2, turn, moves, time_elapsed)
        
        if preview_time > 0:
            remaining = preview_time - (current_time - preview_start)
            if remaining > 0:
                font = pygame.font.Font(None, 72)
                text = f"Memoriza: {int(remaining) + 1}"
                rendered = font.render(text, True, YELLOW)
                text_rect = rendered.get_rect(center=(W//2, 50))
                
                shadow = font.render(text, True, BLACK)
                shadow_rect = shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))
                screen.blit(shadow, shadow_rect)
                screen.blit(rendered, text_rect)
        
        pygame.display.flip()
        
        if matched_count == len(cards):
            try:
                if modo == 1:
                    victory_image = pygame.image.load("image/menu_memotest.png")
                else:
                    if score1 > score2:
                        victory_image = pygame.image.load("image/jugador_1_victoria_memotest.png")
                    elif score2 > score1:
                        victory_image = pygame.image.load("image/jugador_2_victoria_memotest.png")
                    else:
                        victory_image = None
                use_victory_image = True
            except:
                victory_image = None
                use_victory_image = False
            
            screen.fill(BLACK)
            
            victory_particles = []
            for i in range(20):
                x = random.randint(50, W-50)
                y = random.randint(50, H//2)
                color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE])
                victory_particles.extend(create_particles(x, y, color))
            
            for _ in range(60):
                dt = clock.tick(FPS) / 1000.0
                
                if use_victory_image and victory_image:
                    scaled_image = pygame.transform.scale(victory_image, (W, H))
                    screen.blit(scaled_image, (0, 0))
                else:
                    for y in range(H):
                        intensity = int(30 + 20 * math.sin(time.time() * 2 + y * 0.02))
                        color = (intensity//3, intensity//2, intensity)
                        pygame.draw.line(screen, color, (0, y), (W, y))
                    
                    font_big = pygame.font.Font(None, 96)
                    font_small = pygame.font.Font(None, 48)
                    
                    if modo == 1:
                        if score1 > score2:
                            win_text = "¡GANASTE!"
                        elif score2 > score1:
                            win_text = "¡GANÓ LA CPU!"
                        else:
                            win_text = "¡EMPATE!"
                        stats_text = f"Tú: {score1} - CPU: {score2}"
                    else:
                        if score1 > score2:
                            win_text = "¡GANA JUGADOR 1!"
                        elif score2 > score1:
                            win_text = "¡GANA JUGADOR 2!"
                        else:
                            win_text = "¡EMPATE!"
                        stats_text = f"Jugador 1: {score1} - Jugador 2: {score2}"
                    
                    scale = 1.0 + 0.1 * math.sin(time.time() * 4)
                    win_surface = font_big.render(win_text, True, GOLD)
                    win_w = int(win_surface.get_width() * scale)
                    win_h = int(win_surface.get_height() * scale)
                    win_scaled = pygame.transform.scale(win_surface, (win_w, win_h))
                    win_rect = win_scaled.get_rect(center=(W//2, H//2 - 50))
                    
                    shadow = font_big.render(win_text, True, BLACK)
                    shadow_rect = shadow.get_rect(center=(win_rect.centerx + 4, win_rect.centery + 4))
                    screen.blit(shadow, shadow_rect)
                    screen.blit(win_scaled, win_rect)
                    
                    stats_surface = font_small.render(stats_text, True, WHITE)
                    stats_rect = stats_surface.get_rect(center=(W//2, H//2 + 50))
                    screen.blit(stats_surface, stats_rect)
                
                update_particles(victory_particles, dt)
                draw_particles(screen, victory_particles)
                
                pygame.display.flip()
            
            pygame.time.wait(2000)
            return

def main():
    screen = pygame.display.set_mode((W, H))
    
    while True:
        menu_principal(screen)
        modo = menu_modo(screen)
        run_game(screen, modo)
        
        font = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        waiting = True
        while waiting:
            for y in range(H):
                intensity = int(40 + 20 * math.sin(time.time() + y * 0.01))
                color = (intensity//4, intensity//3, intensity//2)
                pygame.draw.line(screen, color, (0, y), (W, y))
            
            msg1 = font.render("¡Juego Terminado!", True, YELLOW)
            msg1_rect = msg1.get_rect(center=(W//2, H//2 - 60))
            
            shadow1 = font.render("¡Juego Terminado!", True, BLACK)
            shadow1_rect = shadow1.get_rect(center=(msg1_rect.centerx + 3, msg1_rect.centery + 3))
            screen.blit(shadow1, shadow1_rect)
            screen.blit(msg1, msg1_rect)
            
            msg2 = font_small.render("ENTER = Jugar de nuevo", True, LIME)
            msg2_rect = msg2.get_rect(center=(W//2, H//2 + 20))
            screen.blit(msg2, msg2_rect)
            
            msg3 = font_small.render("ESC = Salir", True, RED)
            msg3_rect = msg3.get_rect(center=(W//2, H//2 + 60))
            screen.blit(msg3, msg3_rect)
            
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
        print(f"Error: {e}")
        sys.exit(1)