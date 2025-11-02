import pygame
import json
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO = 1200
ALTO = 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fútbol 11 - Clubes")

# Colores
VERDE_OSCURO = (34, 139, 34)
VERDE_CLARO = (50, 205, 50)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (30, 144, 255)
ROJO = (220, 20, 60)
GRIS = (128, 128, 128)
AMARILLO = (255, 215, 0)

# Fuentes
fuente_grande = pygame.font.Font(None, 48)
fuente_mediana = pygame.font.Font(None, 32)
fuente_pequena = pygame.font.Font(None, 24)
fuente_mini = pygame.font.Font(None, 18)

# Cargar datos
with open('basededatos.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    jugadores = datos['jugadores']

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    equipos = config['equipos']

# Formación 4-3-3 (x, y en píxeles relativos al campo)
FORMACION = [
    {'id': 'POR', 'nombre': 'Portero', 'x': 400, 'y': 650},
    {'id': 'LI', 'nombre': 'Lateral Izquierdo', 'x': 250, 'y': 520},
    {'id': 'DC1', 'nombre': 'Defensa Central', 'x': 350, 'y': 500},
    {'id': 'DC2', 'nombre': 'Defensa Central', 'x': 450, 'y': 500},
    {'id': 'LD', 'nombre': 'Lateral Derecho', 'x': 550, 'y': 520},
    {'id': 'MI', 'nombre': 'Mediocampista Izquierdo', 'x': 250, 'y': 350},
    {'id': 'MC', 'nombre': 'Mediocampista Central', 'x': 400, 'y': 330},
    {'id': 'MD', 'nombre': 'Mediocampista Derecho', 'x': 550, 'y': 350},
    {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 250, 'y': 180},
    {'id': 'DEL', 'nombre': 'Delantero Centro', 'x': 400, 'y': 150},
    {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 550, 'y': 180}
]

# Mapeo de posiciones de jugador a posiciones en formación
MAPEO_POSICIONES = {
    'Delantero Centro': ['DEL'],
    'Extremo Izquierdo': ['EI', 'MI'],
    'Extremo Derecho': ['ED', 'MD'],
    'Mediocampista Ofensivo': ['MC', 'MI', 'MD'],
    'Mediocampista Central': ['MC', 'MI', 'MD'],
    'Mediocampista Defensivo': ['MC'],
    'Mediocampista Izquierdo': ['MI', 'EI'],
    'Mediocampista Derecho': ['MD', 'ED'],
    'Defensa Central': ['DC1', 'DC2'],
    'Lateral Izquierdo': ['LI'],
    'Lateral Derecho': ['LD'],
    'Portero': ['POR']
}

class Juego:
    def __init__(self):
        self.posiciones_ocupadas = {}
        self.jugadores_colocados = []
        self.equipo_actual = random.choice(equipos)
        self.busqueda = ""
        self.scroll_y = 0
        self.mensaje = f"Selecciona un jugador de: {self.equipo_actual}"
        self.juego_completo = False
        
    def obtener_posiciones_validas(self, posiciones_jugador):
        if not posiciones_jugador:
            return []
        posiciones_validas = []
        for pos in posiciones_jugador:
            if pos in MAPEO_POSICIONES:
                posiciones_validas.extend(MAPEO_POSICIONES[pos])
        return list(set(posiciones_validas))
    
    def colocar_jugador(self, jugador):
        posiciones_validas = self.obtener_posiciones_validas(jugador.get('posicion', []))
        posiciones_disponibles = [p for p in posiciones_validas if p not in self.posiciones_ocupadas]
        
        if not posiciones_disponibles:
            nombre = jugador.get('apodo', jugador.get('nombre', 'Jugador'))
            self.mensaje = f"❌ {nombre} no puede jugar en ninguna posición disponible"
            return
        
        posicion_elegida = posiciones_disponibles[0]
        self.posiciones_ocupadas[posicion_elegida] = jugador
        self.jugadores_colocados.append({'jugador': jugador, 'posicion': posicion_elegida})
        self.busqueda = ""
        self.scroll_y = 0
        
        if len(self.jugadores_colocados) == 11:
            self.mensaje = "🎉 ¡Felicitaciones! Completaste el equipo"
            self.juego_completo = True
        else:
            self.equipo_actual = random.choice(equipos)
            self.mensaje = f"Selecciona un jugador de: {self.equipo_actual}"
    
    def reiniciar(self):
        self.__init__()
    
    def obtener_jugadores_disponibles(self):
        # Solo mostrar jugadores si hay búsqueda activa
        if not self.busqueda:
            return []
        
        disponibles = []
        for j in jugadores:
            # Usar "club actual" en vez de "clubes totales"
            club_actual = j.get('club actual', '')
            if self.equipo_actual == club_actual:
                if not any(jc['jugador']['id'] == j['id'] for jc in self.jugadores_colocados):
                    nombre = j.get('apodo', j.get('nombre', '')).lower()
                    if self.busqueda.lower() in nombre:
                        disponibles.append(j)
        return disponibles

def dibujar_campo():
    # Fondo del campo
    pygame.draw.rect(pantalla, VERDE_OSCURO, (50, 100, 750, 650))
    
    # Líneas del campo
    pygame.draw.rect(pantalla, BLANCO, (50, 100, 750, 650), 3)
    pygame.draw.line(pantalla, BLANCO, (50, 425), (800, 425), 2)
    pygame.draw.circle(pantalla, BLANCO, (425, 425), 60, 2)
    
    # Área pequeña (arriba)
    pygame.draw.rect(pantalla, BLANCO, (325, 100, 150, 60), 2)
    # Área grande (arriba)
    pygame.draw.rect(pantalla, BLANCO, (250, 100, 300, 120), 2)
    
    # Área pequeña (abajo)
    pygame.draw.rect(pantalla, BLANCO, (325, 690, 150, 60), 2)
    # Área grande (abajo)
    pygame.draw.rect(pantalla, BLANCO, (250, 630, 300, 120), 2)

def dibujar_posicion(pos, jugador=None):
    x, y = pos['x'] + 50, pos['y'] + 100
    
    if jugador:
        # Jugador colocado
        pygame.draw.circle(pantalla, AZUL, (x, y), 35)
        pygame.draw.circle(pantalla, BLANCO, (x, y), 35, 2)
        
        nombre = jugador.get('apodo', jugador.get('nombre', 'Jugador'))
        # Limitar longitud del nombre
        if len(nombre) > 15:
            nombre = nombre[:13] + "..."
        
        texto = fuente_mini.render(nombre, True, BLANCO)
        rect = texto.get_rect(center=(x, y - 5))
        pantalla.blit(texto, rect)
        
        texto_pos = fuente_mini.render(pos['nombre'][:3], True, BLANCO)
        rect_pos = texto_pos.get_rect(center=(x, y + 10))
        pantalla.blit(texto_pos, rect_pos)
    else:
        # Posición vacía
        pygame.draw.circle(pantalla, GRIS, (x, y), 30)
        pygame.draw.circle(pantalla, BLANCO, (x, y), 30, 2)
        
        texto = fuente_mini.render(pos['nombre'][:3], True, BLANCO)
        rect = texto.get_rect(center=(x, y))
        pantalla.blit(texto, rect)

def dibujar_panel_jugadores(juego):
    # Panel de fondo
    pygame.draw.rect(pantalla, (40, 40, 40), (820, 100, 360, 650))
    pygame.draw.rect(pantalla, BLANCO, (820, 100, 360, 650), 2)
    
    # Título
    titulo = fuente_mediana.render("Jugadores", True, BLANCO)
    pantalla.blit(titulo, (900, 110))
    
    if not juego.juego_completo:
        # Cuadro de búsqueda
        pygame.draw.rect(pantalla, (60, 60, 60), (840, 150, 320, 40))
        pygame.draw.rect(pantalla, BLANCO, (840, 150, 320, 40), 2)
        
        # Texto de placeholder si no hay búsqueda
        if juego.busqueda:
            texto_busqueda = fuente_pequena.render(juego.busqueda + "|", True, BLANCO)
        else:
            texto_busqueda = fuente_pequena.render("Escribe para buscar...", True, GRIS)
        pantalla.blit(texto_busqueda, (850, 158))
        
        # Lista de jugadores (solo si hay búsqueda)
        disponibles = juego.obtener_jugadores_disponibles()
        
        if juego.busqueda and len(disponibles) == 0:
            texto = fuente_pequena.render("No hay jugadores", True, GRIS)
            pantalla.blit(texto, (900, 400))
        elif len(disponibles) > 0:
            y_inicial = 210
            altura_item = 70
            max_visible = 7
            
            for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + max_visible]):
                y = y_inicial + i * altura_item
                
                # Fondo del item
                pygame.draw.rect(pantalla, (60, 60, 60), (840, y, 320, 65))
                pygame.draw.rect(pantalla, BLANCO, (840, y, 320, 65), 1)
                
                # Nombre
                nombre = jugador.get('apodo', jugador.get('nombre', 'Jugador'))
                if len(nombre) > 20:
                    nombre = nombre[:18] + "..."
                texto_nombre = fuente_pequena.render(nombre, True, BLANCO)
                pantalla.blit(texto_nombre, (850, y + 5))
                
                # Posiciones
                posiciones_jugador = jugador.get('posicion', [])
                posiciones = ", ".join(posiciones_jugador[:2]) if posiciones_jugador else "Sin posición"
                if len(posiciones) > 35:
                    posiciones = posiciones[:33] + "..."
                texto_pos = fuente_mini.render(posiciones, True, GRIS)
                pantalla.blit(texto_pos, (850, y + 30))
                
                # Botón seleccionar
                boton_rect = pygame.Rect(840, y, 320, 65)
                if boton_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(pantalla, AMARILLO, (840, y, 320, 65), 2)
    else:
        # Juego completo
        texto = fuente_grande.render("🏆", True, AMARILLO)
        pantalla.blit(texto, (950, 300))
        
        texto2 = fuente_mediana.render("¡Equipo completo!", True, BLANCO)
        pantalla.blit(texto2, (870, 380))

def main():
    reloj = pygame.time.Clock()
    juego = Juego()
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                if not juego.juego_completo:
                    if evento.key == pygame.K_BACKSPACE:
                        juego.busqueda = juego.busqueda[:-1]
                        juego.scroll_y = 0
                    elif evento.key == pygame.K_ESCAPE:
                        juego.busqueda = ""
                        juego.scroll_y = 0
                    elif evento.unicode.isprintable():
                        juego.busqueda += evento.unicode
                        juego.scroll_y = 0
                
                if evento.key == pygame.K_F5:
                    juego.reiniciar()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Click en botón reiniciar
                if 1050 <= x <= 1170 and 30 <= y <= 70:
                    juego.reiniciar()
                
                # Click en lista de jugadores
                if 840 <= x <= 1160 and not juego.juego_completo:
                    disponibles = juego.obtener_jugadores_disponibles()
                    y_inicial = 210
                    altura_item = 70
                    
                    for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + 7]):
                        y_item = y_inicial + i * altura_item
                        if y_item <= y <= y_item + 65:
                            juego.colocar_jugador(jugador)
                            break
            
            elif evento.type == pygame.MOUSEWHEEL:
                # Scroll en lista de jugadores
                if not juego.juego_completo:
                    disponibles = juego.obtener_jugadores_disponibles()
                    juego.scroll_y = max(0, min(juego.scroll_y - evento.y, max(0, len(disponibles) - 7)))
        
        # Dibujar
        pantalla.fill((20, 20, 20))
        
        # Header
        titulo = fuente_grande.render("Fútbol 11 - Clubes", True, AMARILLO)
        pantalla.blit(titulo, (50, 20))
        
        # Contador
        contador = fuente_mediana.render(f"Jugadores: {len(juego.jugadores_colocados)}/11", True, BLANCO)
        pantalla.blit(contador, (450, 30))
        
        # Botón reiniciar
        pygame.draw.rect(pantalla, ROJO, (1050, 30, 120, 40))
        texto_reiniciar = fuente_pequena.render("Reiniciar", True, BLANCO)
        pantalla.blit(texto_reiniciar, (1065, 38))
        
        # Mensaje
        texto_mensaje = fuente_pequena.render(juego.mensaje, True, BLANCO)
        rect_mensaje = texto_mensaje.get_rect(center=(425, 80))
        pantalla.blit(texto_mensaje, rect_mensaje)
        
        # Campo
        dibujar_campo()
        
        # Posiciones
        for pos in FORMACION:
            jugador = juego.posiciones_ocupadas.get(pos['id'])
            dibujar_posicion(pos, jugador)
        
        # Panel de jugadores
        dibujar_panel_jugadores(juego)
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()