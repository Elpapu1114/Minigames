import json
import os
import pygame

GAME_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'game_settings.json')


def load_settings():
    # Load settings, fallback to defaults
    default = {
        "resolution": "800x600",
        "fullscreen": False
    }
    try:
        with open(GAME_SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for k in default:
                if k not in data:
                    data[k] = default[k]
            return data
    except Exception:
        return default


def parse_resolution(res_str, default_w, default_h):
    try:
        w, h = map(int, res_str.split('x'))
        return w, h
    except Exception:
        return default_w, default_h


def init_display(default_w=800, default_h=600, title="Pygame"):
    """Inicializa o reconfigura la ventana de pygame según las configuraciones del archivo game_settings.json.
    Retorna (screen, width, height).
    Uso:
        screen, W, H = init_display(800, 600, "Snake")
    """
    settings = load_settings()
    res = settings.get('resolution', f"{default_w}x{default_h}")
    fullscreen = settings.get('fullscreen', False)

    width, height = parse_resolution(res, default_w, default_h)

    flags = 0
    if fullscreen:
        flags = pygame.FULLSCREEN

    """Asegurar que la pantalla de pygame esté inicializada"""
    if not pygame.get_init():
        pygame.init()

    screen = pygame.display.set_mode((width, height), flags)
    pygame.display.set_caption(title)

    return screen, width, height
