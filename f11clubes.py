import pygame
import json
import random
import time

# Inicializar Pygame
pygame.init()

from display_config import init_display

# Configuración de pantalla (base + escala)
BASE_ANCHO = 1200
BASE_ALTO = 800
ANCHO = BASE_ANCHO
ALTO = BASE_ALTO
pantalla, ANCHO, ALTO = init_display(default_w=ANCHO, default_h=ALTO, title="Fútbol 11 - Clubes")

# Helpers de escala
SCALE_X = ANCHO / BASE_ANCHO
SCALE_Y = ALTO / BASE_ALTO
def sx(v):
    return int(v * SCALE_X)
def sy(v):
    return int(v * SCALE_Y)

# Colores
VERDE_OSCURO = (34, 139, 34)
VERDE_CLARO = (50, 205, 50)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (30, 144, 255)
ROJO = (220, 20, 60)
GRIS = (128, 128, 128)
AMARILLO = (255, 215, 0)
VERDE = (0, 200, 0)

# Fuentes escaladas
fuente_grande = pygame.font.Font(None, max(12, sx(48)))
fuente_mediana = pygame.font.Font(None, max(10, sx(32)))
fuente_pequena = pygame.font.Font(None, max(8, sx(24)))
fuente_mini = pygame.font.Font(None, max(8, sx(18)))

# Cargar datos
with open('basededatos.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    jugadores = datos['jugadores']

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    equipos = config['equipos']

# Abreviaturas de posiciones
ABREVIATURAS = {
    'Portero': 'PO',
    'Lateral Izquierdo': 'DFI',
    'Defensa Central': 'DFC',
    'Lateral Derecho': 'DFD',
    'Mediocampista Central': 'MC',
    'Mediocampista Defensivo': 'MCD',
    'Mediocampista Ofensivo': 'MCO',
    'Mediocampista Izquierdo': 'MI',
    'Mediocampista Derecho': 'MD',
    'Extremo Izquierdo': 'EI',
    'Delantero Centro': 'DC',
    'Extremo Derecho': 'ED'
}

# Formaciones disponibles
FORMACIONES = {
    '4-3-3 (1)': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFI', 'nombre': 'Lateral Izquierdo', 'x': 150, 'y': 490},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 275, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 425, 'y': 510},
        {'id': 'DFD', 'nombre': 'Lateral Derecho', 'x': 550, 'y': 490},
        {'id': 'MC1', 'nombre': 'Mediocampista Central', 'x': 250, 'y': 340},
        {'id': 'MC2', 'nombre': 'Mediocampista Central', 'x': 350, 'y': 320},
        {'id': 'MC3', 'nombre': 'Mediocampista Central', 'x': 450, 'y': 340},
        {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 200, 'y': 170},
        {'id': 'DC', 'nombre': 'Delantero Centro', 'x': 350, 'y': 140},
        {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 500, 'y': 170}
    ],
    '4-3-3 (2)': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFI', 'nombre': 'Lateral Izquierdo', 'x': 150, 'y': 490},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 275, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 425, 'y': 510},
        {'id': 'DFD', 'nombre': 'Lateral Derecho', 'x': 550, 'y': 490},
        {'id': 'MC1', 'nombre': 'Mediocampista Central', 'x': 250, 'y': 340},
        {'id': 'MCD', 'nombre': 'Mediocampista Defensivo', 'x': 350, 'y': 370},
        {'id': 'MC2', 'nombre': 'Mediocampista Central', 'x': 450, 'y': 340},
        {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 200, 'y': 170},
        {'id': 'DC', 'nombre': 'Delantero Centro', 'x': 350, 'y': 140},
        {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 500, 'y': 170}
    ],
    '4-3-3 (3)': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFI', 'nombre': 'Lateral Izquierdo', 'x': 150, 'y': 490},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 275, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 425, 'y': 510},
        {'id': 'DFD', 'nombre': 'Lateral Derecho', 'x': 550, 'y': 490},
        {'id': 'MC1', 'nombre': 'Mediocampista Central', 'x': 250, 'y': 340},
        {'id': 'MCO', 'nombre': 'Mediocampista Ofensivo', 'x': 350, 'y': 270},
        {'id': 'MC2', 'nombre': 'Mediocampista Central', 'x': 450, 'y': 340},
        {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 200, 'y': 170},
        {'id': 'DC', 'nombre': 'Delantero Centro', 'x': 350, 'y': 140},
        {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 500, 'y': 170}
    ],
    '4-4-2': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFI', 'nombre': 'Lateral Izquierdo', 'x': 150, 'y': 490},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 275, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 425, 'y': 510},
        {'id': 'DFD', 'nombre': 'Lateral Derecho', 'x': 550, 'y': 490},
        {'id': 'MI', 'nombre': 'Mediocampista Izquierdo', 'x': 150, 'y': 275},
        {'id': 'MC1', 'nombre': 'Mediocampista Central', 'x': 275, 'y': 330},
        {'id': 'MC2', 'nombre': 'Mediocampista Central', 'x': 425, 'y': 330},
        {'id': 'MD', 'nombre': 'Mediocampista Derecho', 'x': 550, 'y': 275},
        {'id': 'DC1', 'nombre': 'Delantero Centro', 'x': 275, 'y': 150},
        {'id': 'DC2', 'nombre': 'Delantero Centro', 'x': 425, 'y': 150}
    ],
    '3-4-3 (1)': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 230, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 350, 'y': 510},
        {'id': 'DFC3', 'nombre': 'Defensa Central', 'x': 470, 'y': 510},
        {'id': 'MI', 'nombre': 'Mediocampista Izquierdo', 'x': 150, 'y': 275},
        {'id': 'MCD1', 'nombre': 'Mediocampista Defensivo', 'x': 275, 'y': 370},
        {'id': 'MCD2', 'nombre': 'Mediocampista Defensivo', 'x': 425, 'y': 370},
        {'id': 'MD', 'nombre': 'Mediocampista Derecho', 'x': 550, 'y': 275},
        {'id': 'DC', 'nombre': 'Delantero Centro', 'x': 350, 'y': 140},
        {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 200, 'y': 170},
        {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 500, 'y': 170}
    ],
    '3-4-3 (2)': [
        {'id': 'PO', 'nombre': 'Portero', 'x': 350, 'y': 610},
        {'id': 'DFC1', 'nombre': 'Defensa Central', 'x': 230, 'y': 510},
        {'id': 'DFC2', 'nombre': 'Defensa Central', 'x': 350, 'y': 510},
        {'id': 'DFC3', 'nombre': 'Defensa Central', 'x': 470, 'y': 510},
        {'id': 'MI', 'nombre': 'Mediocampista Izquierdo', 'x': 150, 'y': 275},
        {'id': 'MCD1', 'nombre': 'Mediocampista Central', 'x': 275, 'y': 330},
        {'id': 'MCD2', 'nombre': 'Mediocampista Central', 'x': 425, 'y': 330},
        {'id': 'MD', 'nombre': 'Mediocampista Derecho', 'x': 550, 'y': 275},
        {'id': 'DC', 'nombre': 'Delantero Centro', 'x': 350, 'y': 140},
        {'id': 'EI', 'nombre': 'Extremo Izquierdo', 'x': 200, 'y': 170},
        {'id': 'ED', 'nombre': 'Extremo Derecho', 'x': 500, 'y': 170}
    ]
}

# Mapeo de posiciones de jugador a posiciones en formación
MAPEO_POSICIONES = {
    'Delantero Centro': ['DC', 'DC1', 'DC2'],
    'Extremo Izquierdo': ['EI'],
    'Extremo Derecho': ['ED'],
    'Mediocampista Ofensivo': ['MCO', 'MC1', 'MC2', 'MC3'],
    'Mediocampista Central': ['MC', 'MC1', 'MC2', 'MC3', 'MCD', 'MCO'],
    'Mediocampista Defensivo': ['MCD', 'MCD1', 'MCD2', 'MCD3'],
    'Mediocampista Izquierdo': ['MI'],
    'Mediocampista Derecho': ['MD'],
    'Defensa Central': ['DFC', 'DFC1', 'DFC2', 'DFC3'],
    'Lateral Izquierdo': ['DFI'],
    'Lateral Derecho': ['DFD'],
    'Portero': ['PO']
}

class Juego:
    def __init__(self):
        self.posiciones_ocupadas = {}
        self.jugadores_colocados = []
        self.equipos_usados = []
        self.equipo_actual = random.choice(equipos)
        self.equipos_usados.append(self.equipo_actual)
        self.busqueda = ""
        self.scroll_y = 0
        self.mensaje = f"Selecciona un jugador de: {self.equipo_actual}"
        self.mensaje_original = self.mensaje
        self.juego_completo = False
        self.formacion_actual = random.choice(list(FORMACIONES.keys()))
        self.tiempo_mensaje_error = 0
        self.jugador_pendiente = None
        self.posiciones_disponibles_jugador = []
        self.mostrando_selector_posicion = False
        self.mostrando_menu_pausa = False
    
    def obtener_posiciones_formacion(self):
        """Obtener todos los IDs de posiciones en la formación actual"""
        formacion = FORMACIONES[self.formacion_actual]
        return [pos['id'] for pos in formacion]
        
    def obtener_posiciones_validas(self, posiciones_jugador):
        """Obtener posiciones válidas que existan en la formación actual"""
        if not posiciones_jugador:
            return []
        
        posiciones_formacion = self.obtener_posiciones_formacion()
        posiciones_validas = []
        
        for pos in posiciones_jugador:
            if pos in MAPEO_POSICIONES:
                # Solo agregar posiciones que existan en la formación actual
                for pos_id in MAPEO_POSICIONES[pos]:
                    if pos_id in posiciones_formacion:
                        posiciones_validas.append(pos_id)
        
        return list(set(posiciones_validas))
    
    def seleccionar_jugador(self, jugador):
        """Primer paso: verificar si el jugador puede ser colocado"""
        nombre_completo = jugador.get('nombre', 'Jugador')
        if "apodo" in jugador:
            nombre_mostrar = jugador.get('apodo', nombre_completo)
        club_actual = jugador.get('club actual', '')
        
        # Verificar si el jugador es del equipo correcto
        if club_actual != self.equipo_actual:
            self.mensaje = f"❌ {nombre_completo} no juega en {self.equipo_actual}"
            self.tiempo_mensaje_error = time.time()
            return
        
        # Obtener posiciones válidas y disponibles
        posiciones_validas = self.obtener_posiciones_validas(jugador.get('posicion', []))
        posiciones_disponibles = [p for p in posiciones_validas if p not in self.posiciones_ocupadas]
        
        if not posiciones_disponibles:
            self.mensaje = f"❌ No hay lugar para {nombre_completo} en la formación"
            self.tiempo_mensaje_error = time.time()
            return
        
        # Si hay más de una posición disponible, mostrar selector
        if len(posiciones_disponibles) > 1:
            self.jugador_pendiente = jugador
            self.posiciones_disponibles_jugador = posiciones_disponibles
            self.mostrando_selector_posicion = True
            self.busqueda = ""
        else:
            # Si solo hay una posición, colocar directamente
            self.colocar_jugador(jugador, posiciones_disponibles[0])
    
    def colocar_jugador(self, jugador, posicion_elegida):
        """Segundo paso: colocar el jugador en la posición elegida"""
        self.posiciones_ocupadas[posicion_elegida] = jugador
        self.jugadores_colocados.append({'jugador': jugador, 'posicion': posicion_elegida})
        self.busqueda = ""
        self.scroll_y = 0
        self.mostrando_selector_posicion = False
        self.jugador_pendiente = None
        self.posiciones_disponibles_jugador = []
        
        if len(self.jugadores_colocados) == 11:
            self.mensaje = "¡Felicitaciones! Completaste el equipo"
            self.mensaje_original = self.mensaje
            self.juego_completo = True
        else:
            # Seleccionar un equipo que no haya sido usado
            equipos_disponibles = [e for e in equipos if e not in self.equipos_usados]
            
            # Si no quedan equipos sin usar, usar cualquiera
            if not equipos_disponibles:
                equipos_disponibles = equipos
            
            self.equipo_actual = random.choice(equipos_disponibles)
            self.equipos_usados.append(self.equipo_actual)
            self.mensaje = f"Selecciona un jugador de: {self.equipo_actual}"
            self.mensaje_original = self.mensaje
    
    def reiniciar(self):
        self.__init__()
    
    def obtener_jugadores_disponibles(self):
        # Mostrar todos los jugadores que coincidan con la búsqueda
        if not self.busqueda:
            return []
        
        disponibles = []
        busqueda_lower = self.busqueda.lower()

        for j in jugadores:
            nombre_completo = j['nombre'].lower()
            apodo = j.get('apodo', "").lower()

            # Aparece en sugerencias si coincide con nombre, apellido o apodo
            if busqueda_lower in nombre_completo or busqueda_lower in apodo:
                disponibles.append(j)

        # Opcional: ordenar por nombre
        disponibles.sort(key=lambda x: x['nombre'])
        
        # Ordenar alfabéticamente por nombre completo
        disponibles.sort(key=lambda x: x.get('nombre', '').lower())
        return disponibles
    
    def actualizar_mensaje(self):
        """Restaurar el mensaje original después de 3 segundos"""
        if self.tiempo_mensaje_error > 0 and time.time() - self.tiempo_mensaje_error > 3:
            self.mensaje = self.mensaje_original
            self.tiempo_mensaje_error = 0

def dibujar_campo():
    # Fondo del campo (escalado)
    campo_x = sx(50)
    campo_y = sy(100)
    campo_w = sx(700)
    campo_h = sy(650)
    pygame.draw.rect(pantalla, VERDE_OSCURO, (campo_x, campo_y, campo_w, campo_h))
    
    # Líneas del campo
    pygame.draw.rect(pantalla, BLANCO, (campo_x, campo_y, campo_w, campo_h), max(1, sx(3)))
    pygame.draw.line(pantalla, BLANCO, (campo_x, campo_y + campo_h // 2), (campo_x + campo_w, campo_y + campo_h // 2), max(1, sx(2)))
    pygame.draw.circle(pantalla, BLANCO, (campo_x + campo_w // 2, campo_y + campo_h // 2), max(6, sx(60)), max(1, sx(2)))
    
    # Área pequeña (arriba)
    pygame.draw.rect(pantalla, BLANCO, (sx(325), sy(100), sx(150), sy(60)), max(1, sx(2)))
    # Área grande (arriba)
    pygame.draw.rect(pantalla, BLANCO, (sx(250), sy(100), sx(300), sy(120)), max(1, sx(2)))
    
    # Área pequeña (abajo)
    pygame.draw.rect(pantalla, BLANCO, (sx(325), sy(690), sx(150), sy(60)), max(1, sx(2)))
    # Área grande (abajo)
    pygame.draw.rect(pantalla, BLANCO, (sx(250), sy(630), sx(300), sy(120)), max(1, sx(2)))

def dibujar_posicion(pos, jugador=None):
    x = sx(pos['x'] + 50)
    y = sy(pos['y'] + 100)
    
    if jugador:
        # Jugador colocado
        pygame.draw.circle(pantalla, AZUL, (x, y), max(6, sx(35)))
        pygame.draw.circle(pantalla, BLANCO, (x, y), max(6, sx(35)), max(1, sx(2)))
        
        # Mostrar apodo si existe, sino nombre completo
        nombre_completo = jugador.get('nombre', 'Jugador')
        nombre = jugador.get('apodo', nombre_completo)
        
        # Limitar longitud del nombre

        texto = fuente_mini.render(nombre, True, BLANCO)
        rect = texto.get_rect(center=(x, y - sy(5)))
        pantalla.blit(texto, rect)
        
        # Usar abreviatura de la posición
        abreviatura = ABREVIATURAS.get(pos['nombre'], pos['nombre'][:3])
        texto_pos = fuente_mini.render(abreviatura, True, BLANCO)
        rect_pos = texto_pos.get_rect(center=(x, y + sy(10)))
        pantalla.blit(texto_pos, rect_pos)
    else:
        # Posición vacía
        pygame.draw.circle(pantalla, GRIS, (x, y), max(6, sx(30)))
        pygame.draw.circle(pantalla, BLANCO, (x, y), max(6, sx(30)), max(1, sx(2)))
        
        # Usar abreviatura de la posición
        abreviatura = ABREVIATURAS.get(pos['nombre'], pos['nombre'][:3])
        texto = fuente_mini.render(abreviatura, True, BLANCO)
        rect = texto.get_rect(center=(x, y))
        pantalla.blit(texto, rect)

def dibujar_panel_jugadores(juego):
    # Panel de fondo (escalado)
    panel_x = sx(820)
    panel_y = sy(100)
    panel_w = sx(360)
    panel_h = sy(650)
    pygame.draw.rect(pantalla, (40, 40, 40), (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(pantalla, BLANCO, (panel_x, panel_y, panel_w, panel_h), max(1, sx(2)))
    
    # Título
    titulo = fuente_mediana.render("Jugadores", True, BLANCO)
    pantalla.blit(titulo, (panel_x + sx(80), panel_y + sy(10)))
    
    if not juego.juego_completo:
        # Cuadro de búsqueda
        pygame.draw.rect(pantalla, (60, 60, 60), (panel_x + sx(20), panel_y + sy(50), sx(320), sy(40)))
        pygame.draw.rect(pantalla, BLANCO, (panel_x + sx(20), panel_y + sy(50), sx(320), sy(40)), max(1, sx(2)))
        
        # Texto de placeholder si no hay búsqueda
        if juego.busqueda:
            texto_busqueda = fuente_pequena.render(juego.busqueda + "|", True, BLANCO)
        else:
            texto_busqueda = fuente_pequena.render("Escribe para buscar...", True, GRIS)
        pantalla.blit(texto_busqueda, (panel_x + sx(30), panel_y + sy(58)))
        
        # Lista de jugadores (solo si hay búsqueda)
        disponibles = juego.obtener_jugadores_disponibles()
        
        if juego.busqueda and len(disponibles) == 0:
            texto = fuente_pequena.render("No hay jugadores", True, GRIS)
            pantalla.blit(texto, (panel_x + sx(80), panel_y + sy(300)))
        elif len(disponibles) > 0:
            y_inicial = panel_y + sy(110)
            altura_item = sy(50)
            max_visible = 10
            
            for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + max_visible]):
                y = y_inicial + i * altura_item
                
                # Fondo uniforme para todos
                pygame.draw.rect(pantalla, (60, 60, 60), (panel_x + sx(20), y, sx(320), sy(45)))
                pygame.draw.rect(pantalla, BLANCO, (panel_x + sx(20), y, sx(320), sy(45)), max(1, sx(1)))
                
                # Mostrar nombre completo
                nombre_completo = jugador.get('nombre', 'Jugador')
                nombre = jugador.get('apodo', nombre_completo)
                if len(nombre) > 30:
                    nombre = nombre[:28] + "..."
                texto_nombre = fuente_pequena.render(nombre, True, BLANCO)
                pantalla.blit(texto_nombre, (panel_x + sx(30), y + sy(12)))
                
                # Botón seleccionar
                boton_rect = pygame.Rect(panel_x + sx(20), y, sx(320), sy(45))
                if boton_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(pantalla, AMARILLO, (panel_x + sx(20), y, sx(320), sy(45)), max(1, sx(2)))
        else:
            pass

    else:
        # Juego completo
        texto = fuente_grande.render("", True, AMARILLO)
        pantalla.blit(texto, (sx(950), sy(300)))
        
        texto2 = fuente_mediana.render("¡Equipo completo!", True, BLANCO)
        pantalla.blit(texto2, (sx(870), sy(380)))

def dibujar_selector_posicion(juego):
    """Dibujar el selector de posiciones cuando hay múltiples opciones"""
    if not juego.mostrando_selector_posicion:
        return
    
    # Overlay oscuro
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(180)
    overlay.fill(NEGRO)
    pantalla.blit(overlay, (0, 0))
    
    # Calcular tamaño del panel (escalado)
    num_posiciones = len(juego.posiciones_disponibles_jugador)
    panel_h = sy(200 + num_posiciones * 60)
    panel_w = sx(500)
    panel_x = (ANCHO - panel_w) // 2
    panel_y = (ALTO - panel_h) // 2
    
    # Panel
    pygame.draw.rect(pantalla, (40, 40, 40), (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(pantalla, AMARILLO, (panel_x, panel_y, panel_w, panel_h), 3)
    
    # Título
    nombre_completo = juego.jugador_pendiente.get('nombre', 'Jugador')
    nombre = juego.jugador_pendiente.get('apodo', nombre_completo)
    titulo = fuente_mediana.render(f"Selecciona posición para {nombre}", True, AMARILLO)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, panel_y + 40))
    
    # Ajustar si el título es muy largo
    if titulo.get_width() > panel_w - 40:
        if len(nombre) > 15:
            nombre = nombre[:13] + "..."
        titulo = fuente_mediana.render(f"Selecciona posición para {nombre}", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, panel_y + 40))
    
    pantalla.blit(titulo, titulo_rect)
    
    # Obtener formación actual para mostrar nombres completos
    formacion = FORMACIONES[juego.formacion_actual]
    
    # Botones de posiciones (escalados)
    y_start = panel_y + sy(100)
    for i, pos_id in enumerate(juego.posiciones_disponibles_jugador):
        y = y_start + i * sy(60)
        boton_rect = pygame.Rect(panel_x + sx(50), y, panel_w - sx(100), sy(50))
        
        # Encontrar el nombre completo de la posición
        nombre_posicion = pos_id
        for pos in formacion:
            if pos['id'] == pos_id:
                nombre_posicion = pos['nombre']
                break
        
        # Obtener abreviatura
        abreviatura = ABREVIATURAS.get(nombre_posicion, pos_id)
        
        pygame.draw.rect(pantalla, AZUL, boton_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_rect, 2)
        
        # Hover effect
        if boton_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, AMARILLO, boton_rect, 3)
        
        # Texto con nombre completo y abreviatura
        texto_posicion = fuente_mediana.render(f"{nombre_posicion} ({abreviatura})", True, BLANCO)
        texto_rect = texto_posicion.get_rect(center=boton_rect.center)
        pantalla.blit(texto_posicion, texto_rect)
    
    # Botón cancelar (escalado)
    y_cancelar = y_start + num_posiciones * sy(60) + sy(20)
    boton_cancelar = pygame.Rect(panel_x + sx(150), y_cancelar, sx(200), sy(50))
    pygame.draw.rect(pantalla, ROJO, boton_cancelar)
    pygame.draw.rect(pantalla, BLANCO, boton_cancelar, 2)
    
    if boton_cancelar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, AMARILLO, boton_cancelar, 3)
    
    texto_cancelar = fuente_mediana.render("Cancelar", True, BLANCO)
    texto_rect = texto_cancelar.get_rect(center=boton_cancelar.center)
    pantalla.blit(texto_cancelar, texto_rect)

def dibujar_menu_pausa():
    """Dibujar el menú de pausa"""
    # Overlay oscuro
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill(NEGRO)
    pantalla.blit(overlay, (0, 0))
    
    # Panel del menú
    panel_w = 400
    panel_h = 350
    panel_x = (ANCHO - panel_w) // 2
    panel_y = (ALTO - panel_h) // 2
    
    pygame.draw.rect(pantalla, (40, 40, 40), (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(pantalla, AMARILLO, (panel_x, panel_y, panel_w, panel_h), 3)
    
    # Título
    titulo = fuente_grande.render("MENÚ", True, AMARILLO)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, panel_y + 50))
    pantalla.blit(titulo, titulo_rect)
    
    # Botones
    botones = [
        {"texto": "Continuar", "y": panel_y + 120, "color": VERDE},
        {"texto": "Reiniciar", "y": panel_y + 190, "color": AZUL},
        {"texto": "Salir", "y": panel_y + 260, "color": ROJO}
    ]
    
    mouse_pos = pygame.mouse.get_pos()
    
    for boton in botones:
        boton_rect = pygame.Rect(panel_x + 50, boton["y"], panel_w - 100, 50)
        pygame.draw.rect(pantalla, boton["color"], boton_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_rect, 2)
        
        # Hover effect
        if boton_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, AMARILLO, boton_rect, 4)
        
        texto = fuente_mediana.render(boton["texto"], True, BLANCO)
        texto_rect = texto.get_rect(center=boton_rect.center)
        pantalla.blit(texto, texto_rect)
    
    return botones, panel_x, panel_w

def main():
    reloj = pygame.time.Clock()
    juego = Juego()
    ejecutando = True
    
    while ejecutando:
        # Actualizar mensaje si hay error temporal
        juego.actualizar_mensaje()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                if juego.mostrando_selector_posicion:
                    if evento.key == pygame.K_ESCAPE:
                        juego.mostrando_selector_posicion = False
                        juego.jugador_pendiente = None
                        juego.posiciones_disponibles_jugador = []
                elif juego.mostrando_menu_pausa:
                    if evento.key == pygame.K_ESCAPE:
                        juego.mostrando_menu_pausa = False
                elif not juego.juego_completo:
                    if evento.key == pygame.K_ESCAPE:
                        juego.mostrando_menu_pausa = True
                    elif evento.key == pygame.K_BACKSPACE:
                        juego.busqueda = juego.busqueda[:-1]
                        juego.scroll_y = 0
                    elif evento.unicode.isprintable():
                        juego.busqueda += evento.unicode
                        juego.scroll_y = 0
                else:
                    # En juego completo, ESC también abre el menú
                    if evento.key == pygame.K_ESCAPE:
                        juego.mostrando_menu_pausa = True
                
                if evento.key == pygame.K_F5:
                    juego.reiniciar()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Click en menú de pausa
                if juego.mostrando_menu_pausa:
                    panel_w = 400
                    panel_h = 350
                    panel_x = (ANCHO - panel_w) // 2
                    panel_y = (ALTO - panel_h) // 2
                    
                    # Botón Continuar
                    boton_continuar = pygame.Rect(panel_x + 50, panel_y + 120, panel_w - 100, 50)
                    if boton_continuar.collidepoint(x, y):
                        juego.mostrando_menu_pausa = False
                    
                    # Botón Reiniciar
                    boton_reiniciar = pygame.Rect(panel_x + 50, panel_y + 190, panel_w - 100, 50)
                    if boton_reiniciar.collidepoint(x, y):
                        juego.reiniciar()
                    
                    # Botón Salir
                    boton_salir = pygame.Rect(panel_x + 50, panel_y + 260, panel_w - 100, 50)
                    if boton_salir.collidepoint(x, y):
                        ejecutando = False
                
                # Click en selector de posición
                elif juego.mostrando_selector_posicion:
                    panel_w = sx(500)
                    num_posiciones = len(juego.posiciones_disponibles_jugador)
                    panel_h = sy(200 + num_posiciones * 60)
                    panel_x = (ANCHO - panel_w) // 2
                    panel_y = (ALTO - panel_h) // 2
                    y_start = panel_y + sy(100)
                    
                    # Verificar clicks en botones de posición
                    for i, pos_id in enumerate(juego.posiciones_disponibles_jugador):
                        y_boton = y_start + i * sy(60)
                        boton_rect = pygame.Rect(panel_x + sx(50), y_boton, panel_w - sx(100), sy(50))
                        if boton_rect.collidepoint(x, y):
                            juego.colocar_jugador(juego.jugador_pendiente, pos_id)
                            break
                    
                    # Verificar click en botón cancelar (escalado)
                    y_cancelar = y_start + num_posiciones * sy(60) + sy(20)
                    boton_cancelar = pygame.Rect(panel_x + sx(150), y_cancelar, sx(200), sy(50))
                    if boton_cancelar.collidepoint(x, y):
                        juego.mostrando_selector_posicion = False
                        juego.jugador_pendiente = None
                        juego.posiciones_disponibles_jugador = []
                else:
                        # Click en botón reiniciar (escalado)
                        rein_x = sx(1050)
                        rein_y = sy(30)
                        rein_w = sx(120)
                        rein_h = sy(40)
                        if rein_x <= x <= rein_x + rein_w and rein_y <= y <= rein_y + rein_h:
                            juego.reiniciar()

                        # Click en lista de jugadores (escalado)
                        panel_x = sx(820)
                        panel_y = sy(100)
                        panel_w = sx(360)
                        panel_h = sy(650)
                        if panel_x <= x <= panel_x + panel_w and not juego.juego_completo:
                            disponibles = juego.obtener_jugadores_disponibles()
                            y_inicial = panel_y + sy(110)
                            altura_item = sy(50)

                            for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + 10]):
                                y_item = y_inicial + i * altura_item
                                if y_item <= y <= y_item + sy(45):
                                    juego.seleccionar_jugador(jugador)
                                    break
            
            elif evento.type == pygame.MOUSEWHEEL:
                # Scroll en lista de jugadores
                if not juego.juego_completo and not juego.mostrando_selector_posicion:
                    disponibles = juego.obtener_jugadores_disponibles()
                    juego.scroll_y = max(0, min(juego.scroll_y - evento.y, max(0, len(disponibles) - 10)))
        
        # Dibujar
        pantalla.fill((20, 20, 20))
        
        # Header (escalado)
        titulo = fuente_grande.render("Fútbol 11 - Clubes", True, AMARILLO)
        pantalla.blit(titulo, (sx(50), sy(20)))

        # Contador
        contador = fuente_mediana.render(f"Jugadores: {len(juego.jugadores_colocados)}/11", True, BLANCO)
        pantalla.blit(contador, (sx(450), sy(30)))

        # Botón reiniciar (escalado)
        rein_x = sx(1050)
        rein_y = sy(30)
        rein_w = sx(120)
        rein_h = sy(40)
        pygame.draw.rect(pantalla, ROJO, (rein_x, rein_y, rein_w, rein_h))
        texto_reiniciar = fuente_pequena.render("Reiniciar", True, BLANCO)
        pantalla.blit(texto_reiniciar, (rein_x + sx(15), rein_y + sy(8)))

        # Mostrar formación actual
        texto_form_actual = fuente_pequena.render(f"Formación: {juego.formacion_actual}", True, GRIS)
        pantalla.blit(texto_form_actual, (sx(50), ALTO - sy(40)))

        # Mensaje
        texto_mensaje = fuente_pequena.render(juego.mensaje, True, BLANCO)
        rect_mensaje = texto_mensaje.get_rect(center=(sx(425), sy(80)))
        pantalla.blit(texto_mensaje, rect_mensaje)
        
        # Campo
        dibujar_campo()
        
        # Posiciones
        formacion_actual = FORMACIONES[juego.formacion_actual]
        for pos in formacion_actual:
            jugador = juego.posiciones_ocupadas.get(pos['id'])
            dibujar_posicion(pos, jugador)
        
        # Panel de jugadores
        dibujar_panel_jugadores(juego)
        
        # Selector de posición (se dibuja al final para estar encima)
        dibujar_selector_posicion(juego)
        
        # Menú de pausa (se dibuja al final de todo)
        if juego.mostrando_menu_pausa:
            dibujar_menu_pausa()
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()