import pygame
from button import Button
import os
import sys
import json

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
FPS = 60

# Variables globales del estado del juego
game_paused = False
menu_state = "main"
game_running = False
waiting_for_key = False
key_to_change = None
key_index = None

# Configuraciones por defecto
default_settings = {
    "resolution": "1200x650",
    "fullscreen": False,
    "vsync": True,
    "master_volume": 60,
    "sfx_volume": 60,
    "music_volume": 60,
    "move_keys": ["W", "A", "S", "D"],
    "jump_key": "SPACE",
    "pause_key": "ESCAPE"
}

game_settings = default_settings.copy()

# Resoluciones disponibles
RESOLUTIONS = [
    ("1200x650", 1200, 650),
    ("1920x1080", 1920, 1080),
    ("1280x720", 1280, 720),
    ("1024x768", 1024, 768),
    ("800x600", 800, 600)
]

# Inicialización de pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Fuentes
try:
    font = pygame.font.Font(None, 60)
    medium_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)
    tiny_font = pygame.font.Font(None, 24)
except:
    font = pygame.font.SysFont("arial", 60)
    medium_font = pygame.font.SysFont("arial", 40)
    small_font = pygame.font.SysFont("arial", 30)
    tiny_font = pygame.font.SysFont("arial", 24)

# Colores
TEXT_COL = (255, 255, 255)
BACKGROUND_COL = (3, 186, 252)
BUTTON_HOVER_COL = (100, 200, 255)
SELECTED_COL = (255, 255, 0)
ERROR_COL = (255, 100, 100)
SUCCESS_COL = (100, 255, 100)

# Variables para mensajes y clicks
last_click_time = 0
click_delay = 200
message_timer = 0
current_message = ""
message_color = TEXT_COL

def crear_ruta_img(nombre_imagen):
    """Crea la ruta completa para una imagen"""
    return os.path.join(os.path.dirname(__file__), 'img', nombre_imagen)

def load_image(filename, default_size=(100, 50)):
    """Carga una imagen con manejo de errores mejorado"""
    try:
        img = pygame.image.load(crear_ruta_img(filename)).convert_alpha()
        return img
    except (pygame.error, FileNotFoundError) as e:
        print(f"No se pudo cargar la imagen {filename}: {e}")
        # Crear imagen placeholder más atractiva
        placeholder = pygame.Surface(default_size, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (100, 100, 100, 180), placeholder.get_rect(), border_radius=10)
        pygame.draw.rect(placeholder, (200, 200, 200), placeholder.get_rect(), 2, border_radius=10)
        
        # Agregar texto al placeholder
        text_surface = tiny_font.render(filename.split('.')[0], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=placeholder.get_rect().center)
        placeholder.blit(text_surface, text_rect)
        
        return placeholder

# Cargar imágenes con tamaños apropiados
play_img = load_image("play.png", (150, 60))
options_img = load_image("options.png", (150, 60))
exit_img = load_image("exit.png", (150, 60))
video_img = load_image("video.png", (120, 50))
audio_img = load_image("audio.png", (120, 50))
keys_img = load_image("keys.png", (120, 50))
back_img = load_image("back.png", (120, 50))

# Crear botones principales
play_button = Button(180, 125, play_img, 10)
options_button = Button(720, 125, options_img, 10)
exit_button = Button(455, 375, exit_img, 10)

# Botones del menú de opciones
video_button = Button(200, 150, video_img, 10)
audio_button = Button(650, 150, audio_img, 10)
keys_button = Button(200, 350, keys_img, 10)
options_back_button = Button(650, 350, back_img, 10)

# Botones para los submenús (posición fija en la parte inferior)
settings_back_button = Button(50, SCREEN_HEIGHT - 80, back_img, 10)

def can_click():
    """Previene clics múltiples"""
    global last_click_time
    current_time = pygame.time.get_ticks()
    if current_time - last_click_time > click_delay:
        last_click_time = current_time
        return True
    return False

def show_message(text, color=TEXT_COL, duration=2000):
    """Muestra un mensaje temporal"""
    global current_message, message_color, message_timer
    current_message = text
    message_color = color
    message_timer = pygame.time.get_ticks() + duration

def draw_text(text, font, text_col, x, y):
    """Dibuja texto en posición específica"""
    img = font.render(str(text), True, text_col)
    screen.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))

def draw_centered_text(text, font, text_col, y):
    """Dibuja texto centrado horizontalmente"""
    img = font.render(str(text), True, text_col)
    x = (SCREEN_WIDTH - img.get_width()) // 2
    screen.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))

def draw_clickable_option(text, font, text_col, x, y, selected=False, hover=False):
    """Dibuja una opción clickeable con estados visuales"""
    color = SELECTED_COL if selected else (BUTTON_HOVER_COL if hover else text_col)
    rect = draw_text(text, font, color, x, y)
    
    if selected:
        pygame.draw.rect(screen, SELECTED_COL, rect, 2, border_radius=5)
    elif hover:
        pygame.draw.rect(screen, BUTTON_HOVER_COL, rect, 1, border_radius=5)
    
    return rect

def draw_pause_overlay():
    """Dibuja overlay semitransparente para el menú de pausa"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

def draw_message():
    """Dibuja mensajes temporales"""
    global current_message, message_timer
    
    if current_message and pygame.time.get_ticks() < message_timer:
        draw_centered_text(current_message, small_font, message_color, SCREEN_HEIGHT - 50)
    elif pygame.time.get_ticks() >= message_timer:
        current_message = ""

def apply_resolution():
    """Aplica la resolución seleccionada"""
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT
    
    try:
        res_str = game_settings["resolution"]
        width, height = map(int, res_str.split('x'))
        
        if game_settings["fullscreen"]:
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((width, height))
        
        SCREEN_WIDTH, SCREEN_HEIGHT = width, height
        show_message(f"Resolución aplicada: {res_str}", SUCCESS_COL)
        
    except Exception as e:
        show_message(f"Error al aplicar resolución: {str(e)}", ERROR_COL)
        print(f"Error aplicando resolución: {e}")

def get_key_name(key_code):
    """Convierte código de tecla a nombre legible"""
    key_names = {
        pygame.K_SPACE: "SPACE",
        pygame.K_RETURN: "ENTER",
        pygame.K_ESCAPE: "ESCAPE",
        pygame.K_TAB: "TAB",
        pygame.K_LSHIFT: "SHIFT",
        pygame.K_RSHIFT: "SHIFT",
        pygame.K_LCTRL: "CTRL",
        pygame.K_RCTRL: "CTRL",
        pygame.K_LALT: "ALT",
        pygame.K_RALT: "ALT",
        pygame.K_UP: "↑",
        pygame.K_DOWN: "↓",
        pygame.K_LEFT: "←",
        pygame.K_RIGHT: "→",
    }
    
    return key_names.get(key_code, pygame.key.name(key_code).upper())

def handle_main_menu():
    """Maneja la lógica del menú principal"""
    global game_paused, menu_state, game_running
    
    if play_button.draw(screen) and can_click():
        game_paused = False
        game_running = True
        show_message("¡Juego iniciado!", SUCCESS_COL)
    
    if options_button.draw(screen) and can_click():
        menu_state = "options"
    
    if exit_button.draw(screen) and can_click():
        return False
    
    return True

def handle_options_menu():
    """Maneja el menú de opciones"""
    global menu_state
    
    if video_button.draw(screen) and can_click():
        menu_state = "video"
    
    if audio_button.draw(screen) and can_click():
        menu_state = "audio"
    
    if keys_button.draw(screen) and can_click():
        menu_state = "keys"
    
    if back_button.draw(screen) and can_click():
        menu_state = "main"

def handle_video_settings():
    """Maneja las configuraciones de video mejoradas"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE VIDEO", font, TEXT_COL, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 150
    spacing = 80
    
    # Resolución
    draw_text("Resolución:", medium_font, TEXT_COL, 200, y_start)
    current_res = game_settings["resolution"]
    
    for i, (res_str, width, height) in enumerate(RESOLUTIONS):
        x = 300 + (i % 3) * 180
        y = y_start + (i // 3) * 40
        selected = (res_str == current_res)
        hover = pygame.Rect(x, y, 150, 30).collidepoint(mouse_pos)
        
        rect = draw_clickable_option(res_str, small_font, TEXT_COL, x, y, selected, hover)
        
        if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
            game_settings["resolution"] = res_str
            show_message(f"Resolución: {res_str}", SUCCESS_COL)
    
    # Botón aplicar resolución
    apply_rect = pygame.Rect(100, y_start + 100, 120, 35)
    pygame.draw.rect(screen, (100, 150, 100), apply_rect, border_radius=5)
    draw_text("Aplicar", medium_font, TEXT_COL, 110, y_start + 105)
    
    if apply_rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        apply_resolution()
    
    # Pantalla completa
    y_pos = y_start + spacing * 2
    draw_text("Pantalla completa:", medium_font, TEXT_COL, 100, y_pos)
    fullscreen_text = "ACTIVADA" if game_settings["fullscreen"] else "DESACTIVADA"
    hover = pygame.Rect(350, y_pos, 150, 30).collidepoint(mouse_pos)
    
    rect = draw_clickable_option(fullscreen_text, small_font, TEXT_COL, 350, y_pos, 
                                game_settings["fullscreen"], hover)
    
    if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        game_settings["fullscreen"] = not game_settings["fullscreen"]
        status = "activada" if game_settings["fullscreen"] else "desactivada"
        show_message(f"Pantalla completa {status}", SUCCESS_COL)
    
    # V-Sync
    y_pos = y_start + spacing * 3
    draw_text("V-Sync:", medium_font, TEXT_COL, 100, y_pos)
    vsync_text = "ACTIVADO" if game_settings["vsync"] else "DESACTIVADO"
    hover = pygame.Rect(250, y_pos, 150, 30).collidepoint(mouse_pos)
    
    rect = draw_clickable_option(vsync_text, small_font, TEXT_COL, 250, y_pos, 
                                game_settings["vsync"], hover)
    
    if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        game_settings["vsync"] = not game_settings["vsync"]
        status = "activado" if game_settings["vsync"] else "desactivado"
        show_message(f"V-Sync {status}", SUCCESS_COL)
    
    # Botón volver
    if back_button.draw(screen) and can_click():
        menu_state = "options"
    

def handle_audio_settings():
    """Maneja las configuraciones de audio mejoradas"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE AUDIO", font, TEXT_COL, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    
    y_start = 150
    spacing = 100
    
    def draw_volume_slider(label, key, y_pos):
        """Dibuja un slider de volumen mejorado"""
        draw_text(f"{label}:", medium_font, TEXT_COL, 100, y_pos)
        current_volume = game_settings[key]
        
        # Dimensiones del slider
        bar_x, bar_y = 350, y_pos + 15
        bar_width, bar_height = 300, 25
        
        # Fondo del slider
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=12)
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=12)
        
        # Barra de progreso
        fill_width = int((current_volume / 100) * bar_width)
        if fill_width > 0:
            color = (100, 255, 100) if current_volume > 70 else (255, 255, 100) if current_volume > 30 else (255, 150, 150)
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height), border_radius=12)
        
        # Handle del slider
        handle_x = bar_x + fill_width - 10
        handle_rect = pygame.Rect(handle_x, bar_y - 5, 20, bar_height + 10)
        pygame.draw.rect(screen, (200, 200, 200), handle_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), handle_rect, 2, border_radius=10)
        
        # Texto del volumen
        draw_text(f"{current_volume}%", small_font, TEXT_COL, bar_x + bar_width + 20, y_pos + 5)
        
        # Detectar interacción
        slider_rect = pygame.Rect(bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 20)
        if slider_rect.collidepoint(mouse_pos) and mouse_pressed:
            relative_x = max(0, min(bar_width, mouse_pos[0] - bar_x))
            new_volume = int((relative_x / bar_width) * 100)
            if new_volume != current_volume:
                game_settings[key] = new_volume
                show_message(f"{label}: {new_volume}%", SUCCESS_COL)
    
    # Sliders de volumen
    draw_volume_slider("Volumen Maestro", "master_volume", y_start)
    draw_volume_slider("Efectos de Sonido", "sfx_volume", y_start + spacing)
    draw_volume_slider("Música", "music_volume", y_start + spacing * 2)
    
    # Botones de prueba de audio
    test_y = y_start + spacing * 3
    draw_text("Prueba de audio:", medium_font, TEXT_COL, 100, test_y)
    
    test_sfx_rect = pygame.Rect(300, test_y, 100, 30)
    test_music_rect = pygame.Rect(420, test_y, 100, 30)
    
    pygame.draw.rect(screen, (100, 100, 150), test_sfx_rect, border_radius=5)
    pygame.draw.rect(screen, (150, 100, 100), test_music_rect, border_radius=5)
    
    draw_text("SFX", small_font, TEXT_COL, 320, test_y + 5)
    draw_text("Música", small_font, TEXT_COL, 430, test_y + 5)
    
    if test_sfx_rect.collidepoint(mouse_pos) and mouse_pressed and can_click():
        show_message("Reproduciendo efecto de sonido", SUCCESS_COL)
    
    if test_music_rect.collidepoint(mouse_pos) and mouse_pressed and can_click():
        show_message("Reproduciendo música", SUCCESS_COL)
    
    # Botón volver
    if back_button.draw(screen) and can_click():
        menu_state = "options"

def handle_keys_settings():
    """Maneja las configuraciones de teclas mejoradas"""
    global menu_state, game_settings, waiting_for_key, key_to_change, key_index
    
    draw_centered_text("CONFIGURACIÓN DE TECLAS", font, TEXT_COL, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 130
    spacing = 50
    
    if waiting_for_key:
        # Mostrar mensaje de espera
        draw_centered_text("Presiona la nueva tecla...", medium_font, SELECTED_COL, 100)
        draw_centered_text("ESC para cancelar", small_font, TEXT_COL, 130)
    
    # Labels y teclas actuales
    key_configs = [
        ("Mover Arriba:", "move_keys", 0),
        ("Mover Izquierda:", "move_keys", 1),
        ("Mover Abajo:", "move_keys", 2),
        ("Mover Derecha:", "move_keys", 3),
        ("Saltar:", "jump_key", None),
        ("Pausar:", "pause_key", None)
    ]
    
    for i, (label, key_type, index) in enumerate(key_configs):
        y_pos = y_start + (i * spacing)
        
        # Dibujar etiqueta
        draw_text(label, medium_font, TEXT_COL, 100, y_pos)
        
        # Obtener valor actual de la tecla
        if key_type == "move_keys":
            current_key = game_settings[key_type][index]
        else:
            current_key = game_settings[key_type]
        
        # Estado visual de la tecla
        is_changing = waiting_for_key and key_to_change == key_type and key_index == index
        key_color = SELECTED_COL if is_changing else TEXT_COL
        
        # Rectángulo de la tecla
        key_rect = pygame.Rect(400, y_pos - 5, 100, 35)
        
        # Hover effect
        if key_rect.collidepoint(mouse_pos) and not waiting_for_key:
            pygame.draw.rect(screen, (80, 80, 80), key_rect, border_radius=8)
        
        pygame.draw.rect(screen, (60, 60, 60), key_rect, border_radius=8)
        pygame.draw.rect(screen, key_color, key_rect, 2, border_radius=8)
        
        # Texto de la tecla
        key_text = f"[{current_key}]"
        text_rect = small_font.get_rect(key_text)
        text_x = key_rect.centerx - text_rect[2] // 2
        text_y = key_rect.centery - text_rect[3] // 2
        draw_text(key_text, small_font, key_color, text_x, text_y)
        
        # Detectar clic para cambiar tecla
        if key_rect.collidepoint(mouse_pos) and mouse_clicked and can_click() and not waiting_for_key:
            waiting_for_key = True
            key_to_change = key_type
            key_index = index
            show_message(f"Cambiando: {label}", SELECTED_COL)
    
    # Botón para resetear a valores por defecto
    reset_rect = pygame.Rect(100, y_start + len(key_configs) * spacing + 20, 200, 35)
    pygame.draw.rect(screen, (150, 100, 100), reset_rect, border_radius=5)
    draw_text("Restablecer por defecto", small_font, TEXT_COL, 110, reset_rect.y + 8)
    
    if reset_rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        game_settings["move_keys"] = default_settings["move_keys"].copy()
        game_settings["jump_key"] = default_settings["jump_key"]
        game_settings["pause_key"] = default_settings["pause_key"]
        show_message("Teclas restablecidas", SUCCESS_COL)
    
    if back_button.draw(screen) and can_click() and not waiting_for_key:
        menu_state = "options"

def handle_key_input(event):
    """Maneja la entrada de nuevas teclas"""
    global waiting_for_key, key_to_change, key_index
    
    if not waiting_for_key:
        return
    
    if event.key == pygame.K_ESCAPE:
        # Cancelar cambio de tecla
        waiting_for_key = False
        key_to_change = None
        key_index = None
        show_message("Cambio cancelado", ERROR_COL)
        return
    
    new_key = get_key_name(event.key)
    
    # Verificar si la tecla ya está en uso
    in_use = False
    for existing_key in game_settings["move_keys"]:
        if existing_key == new_key:
            in_use = True
            break
    
    if game_settings["jump_key"] == new_key or game_settings["pause_key"] == new_key:
        in_use = True
    
    if in_use:
        show_message(f"La tecla {new_key} ya está en uso", ERROR_COL)
        return
    
    # Asignar nueva tecla
    if key_to_change == "move_keys":
        game_settings["move_keys"][key_index] = new_key
    else:
        game_settings[key_to_change] = new_key
    
    show_message(f"Tecla cambiada a: {new_key}", SUCCESS_COL)
    
    # Limpiar estado
    waiting_for_key = False
    key_to_change = None
    key_index = None

def draw_game_screen():
    """Dibuja la pantalla del juego mejorada"""
    draw_centered_text("¡JUEGO EN FUNCIONAMIENTO!", font, TEXT_COL, 150)
    
    # Mostrar controles actuales
    y_pos = 250
    draw_centered_text("CONTROLES ACTUALES:", medium_font, TEXT_COL, y_pos)
    
    controls_info = [
        f"Mover: {'/'.join(game_settings['move_keys'])}",
        f"Saltar: {game_settings['jump_key']}",
        f"Pausar: {game_settings['pause_key']}",
        "Q: Volver al menú"
    ]
    
    for i, control in enumerate(controls_info):
        draw_centered_text(control, small_font, TEXT_COL, y_pos + 50 + (i * 30))
    
    # Mostrar configuración actual
    y_pos = 450
    settings_info = [
        f"Resolución: {game_settings['resolution']} ({'Completa' if game_settings['fullscreen'] else 'Ventana'})",
        f"Audio: Maestro {game_settings['master_volume']}% | SFX {game_settings['sfx_volume']}% | Música {game_settings['music_volume']}%"
    ]
    
    for i, setting in enumerate(settings_info):
        draw_centered_text(setting, tiny_font, TEXT_COL, y_pos + (i * 25))

def handle_events():
    """Maneja todos los eventos de pygame mejorado"""
    global game_paused, game_running, waiting_for_key
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            # Si estamos esperando una nueva tecla
            if waiting_for_key:
                handle_key_input(event)
                continue
            
            # Tecla de pausa configurada
            pause_key = game_settings.get("pause_key", "ESCAPE")
            if ((pause_key == "ESCAPE" and event.key == pygame.K_ESCAPE) or 
                (pause_key != "ESCAPE" and get_key_name(event.key) == pause_key)):
                if game_running:
                    game_paused = True
                elif not game_running:
                    return False
            
            # Volver al menú con Q
            elif event.key == pygame.K_q and game_running:
                game_running = False
                game_paused = False
                show_message("Volviendo al menú...", SUCCESS_COL)
        
        if event.type == pygame.VIDEORESIZE:
            # Manejar redimensionamiento de ventana
            if not game_settings["fullscreen"]:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                game_settings["resolution"] = f"{event.w}x{event.h}"
    
    return True

def save_settings():
    """Guarda las configuraciones en formato JSON"""
    try:
        with open('game_settings.json', 'w', encoding='utf-8') as f:
            json.dump(game_settings, f, indent=4, ensure_ascii=False)
        print("✅ Configuraciones guardadas exitosamente")
    except Exception as e:
        print(f"❌ Error al guardar configuraciones: {e}")

def load_settings():
    """Carga las configuraciones desde JSON con validación robusta"""
    global game_settings
    
    try:
        with open('game_settings.json', 'r', encoding='utf-8') as f:
            loaded_settings = json.load(f)
        
        # Validar y fusionar configuraciones de forma más robusta
        for key, value in loaded_settings.items():
            if key in default_settings:
                # Validación específica por tipo de configuración
                if key == "move_keys":
                    # Validar que sea una lista con 4 elementos string
                    if isinstance(value, list) and len(value) == 4:
                        if all(isinstance(k, str) for k in value):
                            game_settings[key] = value
                        else:
                            game_settings[key] = default_settings[key]
                
                elif key in ["master_volume", "sfx_volume", "music_volume"]:
                    # Validar volúmenes (0-100)
                    if isinstance(value, (int, float)) and 0 <= value <= 100:
                        game_settings[key] = int(value)
                    else:
                        print(f"⚠️ {key} fuera de rango 0-100, usando por defecto")
                        game_settings[key] = default_settings[key]
                
                elif key in ["fullscreen", "vsync"]:
                    # Validar booleanos
                    if isinstance(value, bool):
                        game_settings[key] = value
                    else:
                        print(f"⚠️ {key} no es booleano válido, usando por defecto")
                        game_settings[key] = default_settings[key]
                
                else:
                    # Para otros campos, validar tipo básico
                    if type(value) == type(default_settings[key]):
                        game_settings[key] = value
                    else:
                        print(f"⚠️ Tipo incorrecto para {key}, usando valor por defecto")
                        game_settings[key] = default_settings[key]
        
        # Verificar que todas las configuraciones necesarias estén presentes
        for key in default_settings:
            if key not in game_settings:
                print(f"⚠️ Falta configuración {key}, agregando por defecto")
                game_settings[key] = default_settings[key]
        
        print("✅ Configuraciones cargadas exitosamente")
        
    except FileNotFoundError:
        print("ℹ️ No se encontró archivo de configuraciones, creando uno nuevo...")
        game_settings = default_settings.copy()
        save_settings()
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer configuraciones (JSON inválido): {e}")
        print("ℹ️ Usando configuraciones por defecto")
        game_settings = default_settings.copy()
        save_settings()  # Crear archivo válido
    except Exception as e:
        print(f"❌ Error inesperado al cargar configuraciones: {e}")
        game_settings = default_settings.copy()
        save_settings()  # Crear archivo válido

def main():
    """Función principal mejorada"""
    global game_paused, menu_state, game_running
    
    # Cargar configuraciones
    load_settings()
    
    # Aplicar configuración inicial de pantalla
    try:
        apply_resolution()
    except:
        print("⚠️ Error aplicando resolución inicial, usando por defecto")
    
    run = True
    
    print("=" * 50)
    print("🎮 MENÚ DE JUEGO CON CONFIGURACIONES AVANZADAS")
    print("=" * 50)
    print("📋 CONTROLES:")
    print("   • ESC: Pausar juego / Salir")
    print("   • Q: Volver al menú (desde el juego)")
    print("   • Click: Interactuar con elementos")
    print("   • Configuraciones se guardan automáticamente")
    print("=" * 50)
    
    while run:
        clock.tick(FPS)
        
        # Manejar eventos
        run = handle_events()
        if not run:
            break
        
        # Limpiar pantalla
        screen.fill(BACKGROUND_COL)
        
        # Lógica principal
        if game_running and not game_paused:
            draw_game_screen()
        
        elif game_paused or not game_running:
            if not game_running:
                # Solo menú
                pass
            else:
                # Juego pausado
                draw_game_screen()
                draw_pause_overlay()
            
            # Manejar diferentes estados del menú
            if menu_state == "main":
                title = "MENÚ PRINCIPAL" if not game_running else "JUEGO PAUSADO"
                draw_centered_text(title, font, TEXT_COL, 20)
                run = handle_main_menu()
            
            elif menu_state == "options":
                draw_centered_text("OPCIONES", font, TEXT_COL, 20)
                handle_options_menu()
            
            elif menu_state == "video":
                handle_video_settings()
            
            elif menu_state == "audio":
                handle_audio_settings()
            
            elif menu_state == "keys":
                handle_keys_settings()

        draw_message()
        
        pygame.display.flip()
    
    # Guardar configuraciones al salir
    save_settings()
    
    print("=" * 50)
    print("🔄 CERRANDO APLICACIÓN")
    print("💾 Configuraciones guardadas")
    print("=" * 50)
    
    pygame.quit()
    sys.exit()


main()