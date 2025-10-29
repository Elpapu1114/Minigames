import pygame
from button import Button
import os
import sys
import json
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Variables globales
game_paused = False
menu_state = "main"
game_running = False

# Configuraciones por defecto
default_settings = {
    "resolution": "800x600",
    "fullscreen": False,
    "vsync": True,
    "master_volume": 70,
    "sfx_volume": 80,
    "music_volume": 60,
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

def crear_ruta_img(nombre_imagen):
    """Crea la ruta completa para una imagen"""
    return os.path.join(os.path.dirname(__file__), 'image', nombre_imagen)

def load_image(filename, default_size=(100, 50)):
    """Carga una imagen con manejo de errores mejorado"""
    try:
        img = pygame.image.load(crear_ruta_img(filename)).convert_alpha()
        return img
    except (pygame.error, FileNotFoundError) as e:
        print(f"No se pudo cargar la imagen {filename}: {e}")
        placeholder = pygame.Surface(default_size, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (100, 100, 100, 180), placeholder.get_rect(), border_radius=10)
        pygame.draw.rect(placeholder, (200, 200, 200), placeholder.get_rect(), 2, border_radius=10)
        
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
credit_img = load_image("credistos.png", (120, 50))
back_img = load_image("back.png", (120, 50))
huergo_img = load_image("huergo.png", (300, 300))

# Crear botones principales
play_button = Button(130, 125, play_img, 7)
options_button = Button(450, 125, options_img, 7)
exit_button = Button(300, 375, exit_img, 7)

# Botones del menú de opciones
video_button = Button(200, 150, video_img, 10)
audio_button = Button(650, 150, audio_img, 10)
credit_button = Button(200, 250, credit_img, 10)
back_button = Button(650, 250, back_img, 10)

# Variables para prevenir clics múltiples
last_click_time = 0
click_delay = 200
message_timer = 0
current_message = ""
message_color = TEXT_COL

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
        return True
    
    if options_button.draw(screen) and can_click():
        menu_state = "options"
        return True
    
    if exit_button.draw(screen) and can_click():
        return False
    
    return True

def handle_options_menu():
    """Maneja el menú de opciones"""
    global menu_state
    
    draw_centered_text("OPCIONES", font, TEXT_COL, 20)
    
    if video_button.draw(screen) and can_click():
        menu_state = "video"
    
    if audio_button.draw(screen) and can_click():
        menu_state = "audio"
    
    if credit_button.draw(screen) and can_click():
        menu_state = "credits"
    
    if back_button.draw(screen) and can_click():
        menu_state = "main"

def handle_credits():
    """Maneja la pantalla de créditos"""
    global menu_state
    
    draw_centered_text("CRÉDITOS", font, TEXT_COL, 30)
    
    # Información del desarrollador
    y_pos = 120
    draw_centered_text("Producido por:", medium_font, TEXT_COL, y_pos)
    draw_centered_text("PAPU GAMES INC.", font, (255, 200, 0), y_pos + 50)
    
    # Desarrolladores
    y_pos += 120
    draw_centered_text("Desarrolladores:", medium_font, TEXT_COL, y_pos)
    developers = [
        "Valentin Martinez",
        "Manuel Mañe Mazzieri",
        "Juanjo Shlamovitz Alfonso",
    ]
    
    for i, dev in enumerate(developers):
        draw_centered_text(dev, small_font, (200, 200, 255), y_pos + 40 + (i * 30))
    
    # Logo del instituto
    y_pos += 160
    logo_x = (SCREEN_WIDTH - huergo_img.get_width()) // 2
    screen.blit(huergo_img, (logo_x, y_pos))
    
    # Nombre del instituto
    draw_centered_text("Ins. Ind. Luis A. Huergo", medium_font, TEXT_COL, y_pos + huergo_img.get_height() + 20)
    
    # Año
    draw_centered_text("2025", small_font, TEXT_COL, SCREEN_HEIGHT - 80)
    
    # Botón volver - crear uno nuevo cada vez para evitar conflictos
    back_x = SCREEN_WIDTH // 2 - back_img.get_width() // 2
    back_y = SCREEN_HEIGHT - 70
    back_button_credits = Button(back_x, back_y, back_img, 1)
    
    if back_button_credits.draw(screen) and can_click():
        if game_running:
            game_paused = True
        menu_state = "main"

def handle_video_settings():
    """Maneja las configuraciones de video"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE VIDEO", font, TEXT_COL, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 150
    spacing = 80
    
    # Resolución
    draw_text("Resolución:", medium_font, TEXT_COL, 100, y_start)
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
    
    # Botón back independiente
    back_x = 650
    back_y = 250
    back_button_video = Button(back_x, back_y, back_img, 1)
    if back_button_video.draw(screen) and can_click():
        menu_state = "options"

def handle_audio_settings():
    """Maneja las configuraciones de audio"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE AUDIO", font, TEXT_COL, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    
    y_start = 150
    spacing = 100
    
    def draw_volume_slider(label, key, y_pos):
        """Dibuja un slider de volumen"""
        draw_text(f"{label}:", medium_font, TEXT_COL, 100, y_pos)
        current_volume = game_settings[key]
        
        bar_x, bar_y = 350, y_pos + 15
        bar_width, bar_height = 300, 25
        
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=12)
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=12)
        
        fill_width = int((current_volume / 100) * bar_width)
        if fill_width > 0:
            color = (100, 255, 100) if current_volume > 70 else (255, 255, 100) if current_volume > 30 else (255, 150, 150)
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height), border_radius=12)
        
        handle_x = bar_x + fill_width - 10
        handle_rect = pygame.Rect(handle_x, bar_y - 5, 20, bar_height + 10)
        pygame.draw.rect(screen, (200, 200, 200), handle_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), handle_rect, 2, border_radius=10)
        
        draw_text(f"{current_volume}%", small_font, TEXT_COL, bar_x + bar_width + 20, y_pos + 5)
        
        slider_rect = pygame.Rect(bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 20)
        if slider_rect.collidepoint(mouse_pos) and mouse_pressed:
            relative_x = max(0, min(bar_width, mouse_pos[0] - bar_x))
            new_volume = int((relative_x / bar_width) * 100)
            if new_volume != current_volume:
                game_settings[key] = new_volume
    
    draw_volume_slider("Volumen Maestro", "master_volume", y_start)
    draw_volume_slider("Efectos de Sonido", "sfx_volume", y_start + spacing)
    draw_volume_slider("Música", "music_volume", y_start + spacing * 2)
    
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
    
    # Botón back independiente
    back_x = 650
    back_y = 250
    back_button_audio = Button(back_x, back_y, back_img, 1)
    if back_button_audio.draw(screen) and can_click():
        menu_state = "options"

def draw_game_screen():
    """Dibuja la pantalla del juego"""
    draw_centered_text("¡JUEGO EN FUNCIONAMIENTO!", font, TEXT_COL, 150)
    
    y_pos = 250
    draw_centered_text("CONTROLES ACTUALES:", medium_font, TEXT_COL, y_pos)
    
    controls_info = [
        f"Pausar: {game_settings['pause_key']}",
        "C: Ver créditos",
        "Q: Volver al menú"
    ]
    
    for i, control in enumerate(controls_info):
        draw_centered_text(control, small_font, TEXT_COL, y_pos + 50 + (i * 30))
    
    y_pos = 450
    settings_info = [
        f"Resolución: {game_settings['resolution']} ({'Completa' if game_settings['fullscreen'] else 'Ventana'})",
        f"Audio: Maestro {game_settings.get('master_volume', 70)}% | SFX {game_settings.get('sfx_volume', 80)}% | Música {game_settings.get('music_volume', 60)}%"
    ]
    
    for i, setting in enumerate(settings_info):
        draw_centered_text(setting, tiny_font, TEXT_COL, y_pos + (i * 25))

def handle_events():
    """Maneja todos los eventos de pygame"""
    global game_paused, game_running, menu_state
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            pause_key = game_settings.get("pause_key", "ESCAPE")
            if ((pause_key == "ESCAPE" and event.key == pygame.K_ESCAPE) or 
                (pause_key != "ESCAPE" and get_key_name(event.key) == pause_key)):
                if game_running:
                    game_paused = not game_paused
                    if game_paused:
                        menu_state = "main"
                elif not game_running and menu_state != "credits":
                    return False
            
            elif event.key == pygame.K_c:
                menu_state = "credits"
                if game_running:
                    game_paused = True
            
            elif event.key == pygame.K_q and game_running:
                game_running = False
                game_paused = False
                menu_state = "main"
                show_message("Volviendo al menú...", SUCCESS_COL)
        
        if event.type == pygame.VIDEORESIZE:
            if not game_settings["fullscreen"]:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                game_settings["resolution"] = f"{event.w}x{event.h}"
    
    return True

def save_settings():
    """Guarda las configuraciones en formato JSON"""
    try:
        with open('game_settings.json', 'w', encoding='utf-8') as f:
            json.dump(game_settings, f, indent=4, ensure_ascii=False)
        print("✓ Configuraciones guardadas exitosamente")
    except Exception as e:
        print(f"✗ Error al guardar configuraciones: {e}")

def load_settings():
    """Carga las configuraciones desde JSON"""
    global game_settings
    
    try:
        with open('game_settings.json', 'r', encoding='utf-8') as f:
            loaded_settings = json.load(f)
        
        for key, value in loaded_settings.items():
            if key in default_settings:
                if key == "pause_key":
                    if isinstance(value, str) and len(value) > 0:
                        game_settings[key] = value
                    else:
                        game_settings[key] = default_settings[key]
                
                elif key == "resolution":
                    if isinstance(value, str) and 'x' in value:
                        try:
                            parts = value.split('x')
                            if len(parts) == 2:
                                width, height = int(parts[0]), int(parts[1])
                                if 640 <= width <= 3840 and 480 <= height <= 2160:
                                    game_settings[key] = value
                                else:
                                    game_settings[key] = default_settings[key]
                            else:
                                raise ValueError("Formato incorrecto")
                        except ValueError:
                            game_settings[key] = default_settings[key]
                    else:
                        game_settings[key] = default_settings[key]
                
                elif key in ["master_volume", "sfx_volume", "music_volume"]:
                    if isinstance(value, (int, float)) and 0 <= value <= 100:
                        game_settings[key] = int(value)
                    else:
                        game_settings[key] = default_settings.get(key, 60)
                
                elif key in ["fullscreen", "vsync"]:
                    if isinstance(value, bool):
                        game_settings[key] = value
                    else:
                        game_settings[key] = default_settings[key]
                
                else:
                    if type(value) == type(default_settings[key]):
                        game_settings[key] = value
                    else:
                        game_settings[key] = default_settings[key]
        
        for key in default_settings:
            if key not in game_settings:
                game_settings[key] = default_settings[key]
        
        print("✓ Configuraciones cargadas exitosamente")
        
    except FileNotFoundError:
        print("⚠ No se encontró archivo de configuraciones, usando valores por defecto")
        game_settings = default_settings.copy()
        save_settings()
    except json.JSONDecodeError as e:
        print(f"✗ Error al leer configuraciones (JSON inválido): {e}")
        game_settings = default_settings.copy()
        save_settings()
    except Exception as e:
        print(f"✗ Error inesperado al cargar configuraciones: {e}")
        game_settings = default_settings.copy()
        save_settings()


def main():
    """Función principal del juego"""
    global game_paused, menu_state, game_running, screen
    
    load_settings()
    
    try:
        apply_resolution()
    except:
        print("⚠️ Error aplicando resolución inicial, usando por defecto")
    
    run = True
    
    print("=" * 50)
    print("🎮 MENÚ DE JUEGO - PAPU GAMES INC.")
    print("=" * 50)
    print("📋 CONTROLES:")
    print("   • ESC: Pausar juego / Salir")
    print("   • Q: Volver al menú (desde el juego)")
    print("   • C: Ver créditos")
    print("   • Click: Interactuar con elementos")
    print("=" * 50)
    
    while run:
        clock.tick(FPS)
        
        screen.fill(BACKGROUND_COL)
        
        run = handle_events()
        if not run:
            break
        
        if game_running and not game_paused:
            draw_game_screen()
        
        elif game_paused or not game_running:
            if not game_running:
                pass
            else:
                draw_game_screen()
                draw_pause_overlay()
            
            if menu_state == "main":
                title = "MENÚ PRINCIPAL" if not game_running else "JUEGO PAUSADO"
                draw_centered_text(title, font, TEXT_COL, 20)
                run = handle_main_menu()
            
            elif menu_state == "options":
                handle_options_menu()
            
            elif menu_state == "video":
                handle_video_settings()
            
            elif menu_state == "audio":
                handle_audio_settings()
            
            elif menu_state == "credits":
                handle_credits()
        
        draw_message()
        
        pygame.display.flip()
    
    save_settings()
    
    print("=" * 50)
    print("👋 CERRANDO APLICACIÓN")
    print("💾 Configuraciones guardadas")
    print("🎮 Gracias por jugar - PAPU GAMES INC.")
    print("=" * 50)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()