import pygame
from button import Button
import os
import sys

pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
FPS = 60


game_paused = False
menu_state = "main"
game_running = False


game_settings = {
    "resolution": "1200x650",
    "fullscreen": False,
    "vsync": True,
    "master_volume": 100,
    "sfx_volume": 80,
    "music_volume": 60,
    "move_keys": ["W", "A", "S", "D"],
    "jump_key": "SPACE",
    "pause_key": "ESC"
}


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arialblack", 60)
medium_font = pygame.font.SysFont("arialblack", 40)
small_font = pygame.font.SysFont("arialblack", 30)

TEXT_COL = (255, 255, 255)
BACKGROUND_COL = (3, 186, 252)
BUTTON_HOVER_COL = (100, 200, 255)
SELECTED_COL = (255, 255, 0)

def crear_ruta_img(nombre_imagen):
    """Crea la ruta completa para una imagen"""
    return os.path.join(os.path.dirname(__file__), 'img', nombre_imagen)

def load_image(filename):
    """Carga una imagen con manejo de errores"""
    try:
        return pygame.image.load(crear_ruta_img(filename)).convert_alpha()
    except pygame.error as e:
        print(f"No se pudo cargar la imagen {filename}: {e}")
        # Crear una imagen de placeholder
        placeholder = pygame.Surface((100, 50))
        placeholder.fill((200, 200, 200))
        return placeholder

# Cargar imágenes
play_img = load_image("play.png")
options_img = load_image("options.png")
exit_img = load_image("exit.png")
video_img = load_image("video.png")
audio_img = load_image("audio.png")
keys_img = load_image("keys.png")
back_img = load_image("back.png")

# Crear botones principales
play_button = Button(180, 125, play_img, 10)
options_button = Button(720, 125, options_img, 10)
exit_button = Button(455, 375, exit_img, 10)
video_button = Button(200, 60, video_img, 10)
audio_button = Button(650, 60, audio_img, 10)
keys_button = Button(200, 350, keys_img, 10)
back_button = Button(650, 350, back_img, 10)

# Variables para prevenir clics múltiples
last_click_time = 0
click_delay = 200  # milisegundos

def can_click():
    global last_click_time
    current_time = pygame.time.get_ticks()
    if current_time - last_click_time > click_delay:
        last_click_time = current_time
        return True
    return False

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))

def draw_centered_text(text, font, text_col, y):

    img = font.render(text, True, text_col)
    x = (SCREEN_WIDTH - img.get_width()) // 2
    screen.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))

def draw_clickable_option(text, font, text_col, x, y, selected=False):

    color = SELECTED_COL if selected else text_col
    rect = draw_text(text, font, color, x, y)
    if selected:
        pygame.draw.rect(screen, SELECTED_COL, rect, 2)
    return rect

def draw_pause_overlay():

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

def handle_main_menu():
    """Maneja la lógica del menú principal"""
    global game_paused, menu_state, game_running
    
    if play_button.draw(screen) and can_click():
        game_paused = False
        game_running = True
        print("Iniciando juego...")
    
    if options_button.draw(screen) and can_click():
        menu_state = "options"
        print("Abriendo opciones...")
    
    if exit_button.draw(screen) and can_click():
        return False
    
    return True

def handle_options_menu():
    """Maneja la lógica del menú de opciones"""
    global menu_state
    
    if video_button.draw(screen) and can_click():
        menu_state = "video"
        print("Configuración de video")
    
    if audio_button.draw(screen) and can_click():
        menu_state = "audio"
        print("Configuración de audio")
    
    if keys_button.draw(screen) and can_click():
        menu_state = "keys"
        print("Cambiar teclas")
    
    if back_button.draw(screen) and can_click():
        menu_state = "main"
        print("Volviendo al menú principal...")

def handle_video_settings():
    """Maneja las configuraciones de video"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE VIDEO", font, TEXT_COL, 100)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 200
    spacing = 60
    
    # Resolución
    resolutions = ["1200x650", "1920x1080", "1280x720", "800x600"]
    current_res = game_settings["resolution"]
    draw_text("Resolución:", medium_font, TEXT_COL, 200, y_start)
    
    for i, res in enumerate(resolutions):
        x = 400 + (i * 150)
        selected = (res == current_res)
        rect = draw_clickable_option(res, small_font, TEXT_COL, x, y_start, selected)
        
        if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
            game_settings["resolution"] = res
            print(f"Resolución cambiada a: {res}")
    
    # Pantalla completa
    y_pos = y_start + spacing
    draw_text("Pantalla completa:", medium_font, TEXT_COL, 200, y_pos)
    fullscreen_text = "SÍ" if game_settings["fullscreen"] else "NO"
    rect = draw_clickable_option(fullscreen_text, small_font, TEXT_COL, 500, y_pos, game_settings["fullscreen"])
    
    if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        game_settings["fullscreen"] = not game_settings["fullscreen"]
        print(f"Pantalla completa: {'Activada' if game_settings['fullscreen'] else 'Desactivada'}")
    
    # V-Sync
    y_pos = y_start + (spacing * 2)
    draw_text("V-Sync:", medium_font, TEXT_COL, 200, y_pos)
    vsync_text = "SÍ" if game_settings["vsync"] else "NO"
    rect = draw_clickable_option(vsync_text, small_font, TEXT_COL, 350, y_pos, game_settings["vsync"])
    
    if rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
        game_settings["vsync"] = not game_settings["vsync"]
        print(f"V-Sync: {'Activado' if game_settings['vsync'] else 'Desactivado'}")
    
    # Botón volver
    if back_button.draw(screen) and can_click():
        menu_state = "options"

def handle_audio_settings():
    """Maneja las configuraciones de audio"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE AUDIO", font, TEXT_COL, 100)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 200
    spacing = 80
    
    # Función para manejar sliders de volumen
    def draw_volume_slider(label, key, y_pos):
        draw_text(f"{label}:", medium_font, TEXT_COL, 200, y_pos)
        current_volume = game_settings[key]
        
        # Dibujar barra de volumen
        bar_x, bar_y = 450, y_pos + 10
        bar_width, bar_height = 300, 20
        
        # Fondo de la barra
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de volumen actual
        fill_width = int((current_volume / 100) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))
        
        # Texto del volumen
        draw_text(f"{current_volume}%", small_font, TEXT_COL, bar_x + bar_width + 20, y_pos)
        
        # Detectar clic en la barra
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        if bar_rect.collidepoint(mouse_pos) and mouse_clicked:
            # Calcular nuevo volumen basado en posición del mouse
            relative_x = mouse_pos[0] - bar_x
            new_volume = max(0, min(100, int((relative_x / bar_width) * 100)))
            game_settings[key] = new_volume
            print(f"{label} cambiado a: {new_volume}%")
    
    # Sliders de volumen
    draw_volume_slider("Vol. Maestro", "master_volume", y_start)
    draw_volume_slider("Efectos", "sfx_volume", y_start + spacing)
    draw_volume_slider("Música", "music_volume", y_start + (spacing * 2))
    
    # Botón volver
    if back_button.draw(screen) and can_click():
        menu_state = "options"

def handle_keys_settings():
    """Maneja las configuraciones de teclas"""
    global menu_state, game_settings
    
    draw_centered_text("CONFIGURACIÓN DE TECLAS", font, TEXT_COL, 100)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    y_start = 200
    spacing = 60
    
    # Mostrar configuración actual de teclas
    keys_config = [
        ("Mover arriba:", game_settings["move_keys"][0]),
        ("Mover izquierda:", game_settings["move_keys"][1]),
        ("Mover abajo:", game_settings["move_keys"][2]),
        ("Mover derecha:", game_settings["move_keys"][3]),
        ("Saltar:", game_settings["jump_key"]),
        ("Pausar:", game_settings["pause_key"])
    ]
    
    for i, (label, key) in enumerate(keys_config):
        y_pos = y_start + (i * spacing)
        draw_text(label, medium_font, TEXT_COL, 200, y_pos)
        
        # Mostrar tecla actual
        key_rect = draw_clickable_option(f"[{key}]", medium_font, TEXT_COL, 500, y_pos)
        
        # Permitir cambio de tecla (simplificado - solo muestra el concepto)
        if key_rect.collidepoint(mouse_pos) and mouse_clicked and can_click():
            print(f"Cambiar tecla para: {label}")
            # Aquí irían las opciones alternativas de teclas
            alternatives = {
                "W": ["↑", "I", "K"],
                "A": ["←", "J", "Q"],
                "S": ["↓", "K", "X"],
                "D": ["→", "L", "E"],
                "SPACE": ["ENTER", "SHIFT", "CTRL"],
                "ESC": ["P", "TAB", "Q"]
            }
            
            if key in alternatives:
                # Ciclar entre alternativas
                current_index = 0
                if key in alternatives[key]:
                    current_index = alternatives[key].index(key)
                new_index = (current_index + 1) % len(alternatives[key])
                new_key = alternatives[key][new_index]
                
                # Actualizar la configuración
                if i < 4:  # Teclas de movimiento
                    game_settings["move_keys"][i] = new_key
                elif i == 4:  # Saltar
                    game_settings["jump_key"] = new_key
                elif i == 5:  # Pausar
                    game_settings["pause_key"] = new_key
                
                print(f"Tecla cambiada a: {new_key}")
    
    # Botón volver
    if back_button.draw(screen) and can_click():
        menu_state = "options"

def draw_game_screen():
    """Dibuja la pantalla del juego cuando está corriendo"""
    draw_centered_text("¡JUEGO EN FUNCIONAMIENTO!", font, TEXT_COL, 200)
    draw_centered_text("Presiona ESC para pausar", small_font, TEXT_COL, 300)
    draw_centered_text("Presiona Q para volver al menú", small_font, TEXT_COL, 350)
    
    # Mostrar configuración actual en el juego
    y_pos = 400
    draw_centered_text(f"Resolución: {game_settings['resolution']}", small_font, TEXT_COL, y_pos)
    draw_centered_text(f"Vol. Maestro: {game_settings['master_volume']}%", small_font, TEXT_COL, y_pos + 30)

def handle_events():
    """Maneja todos los eventos de pygame"""
    global game_paused, game_running
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_running:
                    game_paused = True
                else:
                    return False
            
            elif event.key == pygame.K_q and game_running:
                game_running = False
                game_paused = False
    
    return True

def save_settings():
    """Guarda las configuraciones en un archivo"""
    try:
        with open('game_settings.txt', 'w') as f:
            for key, value in game_settings.items():
                f.write(f"{key}={value}\n")
        print("Configuraciones guardadas")
    except Exception as e:
        print(f"Error al guardar configuraciones: {e}")

def load_settings():
    """Carga las configuraciones desde un archivo"""
    global game_settings
    try:
        with open('game_settings.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key in game_settings:
                        # Convertir el valor al tipo correcto
                        if isinstance(game_settings[key], bool):
                            game_settings[key] = value.lower() == 'true'
                        elif isinstance(game_settings[key], int):
                            game_settings[key] = int(value)
                        elif isinstance(game_settings[key], list):
                            game_settings[key] = eval(value)
                        else:
                            game_settings[key] = value
        print("Configuraciones cargadas")
    except FileNotFoundError:
        print("No se encontró archivo de configuraciones, usando valores por defecto")
    except Exception as e:
        print(f"Error al cargar configuraciones: {e}")

# Función principal del juego
def main():
    global game_paused, menu_state, game_running
    
    # Cargar configuraciones guardadas
    load_settings()
    
    run = True
    
    print("=== MENÚ CON CONFIGURACIONES FUNCIONALES ===")
    print("Controles:")
    print("- ESC: Pausar juego / Salir de la aplicación")
    print("- Q: Volver al menú (desde el juego)")
    print("- Click: Interactuar con botones y configuraciones")
    print("- Las configuraciones se guardan automáticamente")
    
    while run:
        clock.tick(FPS)
        
        # Manejo de eventos
        run = handle_events()
        if not run:
            break
        
        # Limpiar pantalla
        screen.fill(BACKGROUND_COL)
        
        # Lógica principal del juego
        if game_running and not game_paused:
            draw_game_screen()
        
        elif game_paused or not game_running:
            if not game_running:
                pass
            else:
                draw_game_screen()
                draw_pause_overlay()
            
            # Manejar diferentes estados del menú
            if menu_state == "main":
                draw_centered_text("pausado", font, TEXT_COL, 50)
                run = handle_main_menu()
            
            elif menu_state == "options":
                draw_centered_text("OPCIONES", font, TEXT_COL, 50)
                handle_options_menu()
            
            elif menu_state == "video":
                handle_video_settings()
            
            elif menu_state == "audio":
                handle_audio_settings()
            
            elif menu_state == "keys":
                handle_keys_settings()
        
        pygame.display.update()
    
    # Guardar configuraciones al salir
    save_settings()
    
    print("=== CERRANDO APLICACIÓN ===")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()