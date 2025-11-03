import pygame
import json
import random
import time

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
VERDE = (0, 200, 0)

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
    ]
}

# Mapeo de posiciones de jugador a posiciones en formación
MAPEO_POSICIONES = {
    'Delantero Centro': ['DC', 'DC1', 'DC2'],
    'Extremo Izquierdo': ['EI'],
    'Extremo Derecho': ['ED'],
    'Mediocampista Ofensivo': ['MCO', 'MC1', 'MC2', 'MC3'],
    'Mediocampista Central': ['MC', 'MC1', 'MC2', 'MC3', 'MCD', 'MCO'],
    'Mediocampista Defensivo': ['MCD', 'MC1', 'MC2', 'MC3'],
    'Mediocampista Izquierdo': ['MI'],
    'Mediocampista Derecho': ['MD'],
    'Defensa Central': ['DFC', 'DFC1', 'DFC2'],
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
            self.mensaje = "🎉 ¡Felicitaciones! Completaste el equipo"
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
            if not any(jc['jugador']['id'] == j['id'] for jc in self.jugadores_colocados):
                # Buscar por nombre completo (que puede incluir apellido)
                nombre_completo = j.get('nombre', '').lower()
                apodo = j.get('apodo', '').lower()
                
                # Dividir el nombre en palabras para buscar por cualquier parte
                palabras_nombre = nombre_completo.split()
                palabras_apodo = apodo.split()
                
                # Coincide si alguna palabra empieza con la búsqueda
                if any(palabra.startswith(busqueda_lower) for palabra in palabras_nombre):
                    disponibles.append(j)
                elif any(palabra.startswith(busqueda_lower) for palabra in palabras_apodo):
                    disponibles.append(j)
        
        # Ordenar alfabéticamente por nombre completo
        disponibles.sort(key=lambda x: x.get('nombre', '').lower())
        return disponibles
    
    def actualizar_mensaje(self):
        """Restaurar el mensaje original después de 3 segundos"""
        if self.tiempo_mensaje_error > 0 and time.time() - self.tiempo_mensaje_error > 3:
            self.mensaje = self.mensaje_original
            self.tiempo_mensaje_error = 0

def dibujar_campo():
    # Fondo del campo
    pygame.draw.rect(pantalla, VERDE_OSCURO, (50, 100, 700, 650))
    
    # Líneas del campo
    pygame.draw.rect(pantalla, BLANCO, (50, 100, 700, 650), 3)
    pygame.draw.line(pantalla, BLANCO, (50, 425), (750, 425), 2)
    pygame.draw.circle(pantalla, BLANCO, (400, 425), 60, 2)
    
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
        
        # Mostrar apodo si existe, sino nombre completo
        nombre_completo = jugador.get('nombre', 'Jugador')
        nombre = jugador.get('apodo', nombre_completo)
        
        # Limitar longitud del nombre
        if len(nombre) > 15:
            nombre = nombre[:13] + "..."
        
        texto = fuente_mini.render(nombre, True, BLANCO)
        rect = texto.get_rect(center=(x, y - 5))
        pantalla.blit(texto, rect)
        
        # Usar abreviatura de la posición
        abreviatura = ABREVIATURAS.get(pos['nombre'], pos['nombre'][:3])
        texto_pos = fuente_mini.render(abreviatura, True, BLANCO)
        rect_pos = texto_pos.get_rect(center=(x, y + 10))
        pantalla.blit(texto_pos, rect_pos)
    else:
        # Posición vacía
        pygame.draw.circle(pantalla, GRIS, (x, y), 30)
        pygame.draw.circle(pantalla, BLANCO, (x, y), 30, 2)
        
        # Usar abreviatura de la posición
        abreviatura = ABREVIATURAS.get(pos['nombre'], pos['nombre'][:3])
        texto = fuente_mini.render(abreviatura, True, BLANCO)
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
            altura_item = 50
            max_visible = 10
            
            for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + max_visible]):
                y = y_inicial + i * altura_item
                
                # Fondo uniforme para todos
                pygame.draw.rect(pantalla, (60, 60, 60), (840, y, 320, 45))
                pygame.draw.rect(pantalla, BLANCO, (840, y, 320, 45), 1)
                
                # Mostrar nombre completo
                nombre = jugador.get('nombre', 'Jugador')
                if len(nombre) > 30:
                    nombre = nombre[:28] + "..."
                texto_nombre = fuente_pequena.render(nombre, True, BLANCO)
                pantalla.blit(texto_nombre, (850, y + 12))
                
                # Botón seleccionar
                boton_rect = pygame.Rect(840, y, 320, 45)
                if boton_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(pantalla, AMARILLO, (840, y, 320, 45), 2)
    else:
        # Juego completo
        texto = fuente_grande.render("", True, AMARILLO)
        pantalla.blit(texto, (950, 300))
        
        texto2 = fuente_mediana.render("¡Equipo completo!", True, BLANCO)
        pantalla.blit(texto2, (870, 380))

def dibujar_selector_posicion(juego):
    """Dibujar el selector de posiciones cuando hay múltiples opciones"""
    if not juego.mostrando_selector_posicion:
        return
    
    # Overlay oscuro
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(180)
    overlay.fill(NEGRO)
    pantalla.blit(overlay, (0, 0))
    
    # Calcular tamaño del panel
    num_posiciones = len(juego.posiciones_disponibles_jugador)
    panel_h = 200 + num_posiciones * 60
    panel_w = 500
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
    
    # Botones de posiciones
    y_start = panel_y + 100
    for i, pos_id in enumerate(juego.posiciones_disponibles_jugador):
        y = y_start + i * 60
        boton_rect = pygame.Rect(panel_x + 50, y, panel_w - 100, 50)
        
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
    
    # Botón cancelar
    y_cancelar = y_start + num_posiciones * 60 + 20
    boton_cancelar = pygame.Rect(panel_x + 150, y_cancelar, 200, 50)
    pygame.draw.rect(pantalla, ROJO, boton_cancelar)
    pygame.draw.rect(pantalla, BLANCO, boton_cancelar, 2)
    
    if boton_cancelar.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, AMARILLO, boton_cancelar, 3)
    
    texto_cancelar = fuente_mediana.render("Cancelar", True, BLANCO)
    texto_rect = texto_cancelar.get_rect(center=boton_cancelar.center)
    pantalla.blit(texto_cancelar, texto_rect)

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
                elif not juego.juego_completo:
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
                
                # Click en selector de posición
                if juego.mostrando_selector_posicion:
                    panel_w = 500
                    panel_x = (ANCHO - panel_w) // 2
                    num_posiciones = len(juego.posiciones_disponibles_jugador)
                    panel_h = 200 + num_posiciones * 60
                    panel_y = (ALTO - panel_h) // 2
                    y_start = panel_y + 100
                    
                    # Verificar clicks en botones de posición
                    for i, pos_id in enumerate(juego.posiciones_disponibles_jugador):
                        y_boton = y_start + i * 60
                        boton_rect = pygame.Rect(panel_x + 50, y_boton, panel_w - 100, 50)
                        if boton_rect.collidepoint(x, y):
                            juego.colocar_jugador(juego.jugador_pendiente, pos_id)
                            break
                    
                    # Verificar click en botón cancelar
                    y_cancelar = y_start + num_posiciones * 60 + 20
                    boton_cancelar = pygame.Rect(panel_x + 150, y_cancelar, 200, 50)
                    if boton_cancelar.collidepoint(x, y):
                        juego.mostrando_selector_posicion = False
                        juego.jugador_pendiente = None
                        juego.posiciones_disponibles_jugador = []
                else:
                    # Click en botón reiniciar
                    if 1050 <= x <= 1170 and 30 <= y <= 70:
                        juego.reiniciar()
                    
                    # Click en lista de jugadores
                    if 840 <= x <= 1160 and not juego.juego_completo:
                        disponibles = juego.obtener_jugadores_disponibles()
                        y_inicial = 210
                        altura_item = 50
                        
                        for i, jugador in enumerate(disponibles[juego.scroll_y:juego.scroll_y + 10]):
                            y_item = y_inicial + i * altura_item
                            if y_item <= y <= y_item + 45:
                                juego.seleccionar_jugador(jugador)
                                break
            
            elif evento.type == pygame.MOUSEWHEEL:
                # Scroll en lista de jugadores
                if not juego.juego_completo and not juego.mostrando_selector_posicion:
                    disponibles = juego.obtener_jugadores_disponibles()
                    juego.scroll_y = max(0, min(juego.scroll_y - evento.y, max(0, len(disponibles) - 10)))
        
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
        
        # Mostrar formación actual
        texto_form_actual = fuente_pequena.render(f"Formación: {juego.formacion_actual}", True, GRIS)
        pantalla.blit(texto_form_actual, (50, 760))
        
        # Mensaje
        texto_mensaje = fuente_pequena.render(juego.mensaje, True, BLANCO)
        rect_mensaje = texto_mensaje.get_rect(center=(425, 80))
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
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()