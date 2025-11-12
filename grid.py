import os
import pygame
import json
import random
import sys

# Inicializar Pygame
pygame.init()

from display_config import init_display

# Constantes base (usadas para escalar)
BASE_ANCHO = 1000
BASE_ALTO = 800
ANCHO = BASE_ANCHO
ALTO = BASE_ALTO
TAMANO_CELDA_BASE = 100
MARGEN_BASE = 10
FPS = 60

# Inicializar pantalla con resolucion desde game_settings.json
pantalla, ANCHO, ALTO = init_display(default_w=ANCHO, default_h=ALTO, title="Grid Futbol")

# Factores de escala y helpers
SCALE_X = ANCHO / BASE_ANCHO
SCALE_Y = ALTO / BASE_ALTO
def sx(v):
    return int(v * SCALE_X)
def sy(v):
    return int(v * SCALE_Y)

# Tamaños escalados - calcular dinámicamente para centrar grid
# Espacio disponible para el grid (3 columnas + 2 márgenes)
# Calcular tamaño de celda en función de la resolución actual.
# Reservamos un margen lateral y vertical razonable y usamos tanto el ancho
# como la altura disponibles para decidir el mayor tamaño que encaje.
available_w = max(200, ANCHO - sx(200))  # dejar al menos 100px a cada lado
available_h = max(200, ALTO - sy(300))   # dejar espacio para encabezados y input

# Margen temporal basado en ancho (porcentaje pequeño)
tmp_margin = max(2, int(available_w * 0.03))

# Tamaño candidato por ancho: dividir el ancho disponible entre 3 celdas y restar márgenes
TAMANO_CELDA_w = max(16, int((available_w - 2 * tmp_margin) / 3))
# Tamaño candidato por alto: dividir el alto disponible entre 3 filas
TAMANO_CELDA_h = max(16, int(available_h / 3))

# Elegimos el tamaño que quepa tanto en ancho como en alto
TAMANO_CELDA = max(16, min(TAMANO_CELDA_w, TAMANO_CELDA_h))

# Margen proporcional al tamaño final de la celda
MARGEN = max(2, int(TAMANO_CELDA * 0.08))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
AZUL = (0, 100, 200)
AZUL_CLARO = (100, 150, 255)
AMARILLO = (255, 255, 200)
NARANJA = (255, 165, 0)

# Cargar base de datos
def cargar_datos():
    try:
        with open('basededatos.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if isinstance(datos, dict) and "jugadores" in datos:
            jugadores = datos["jugadores"]
        else:
            jugadores = datos
            
        print(f"Cargados {len(jugadores)} jugadores")
        if jugadores:
            print(f"Ejemplo de jugador: {jugadores[0]}")
        
        return jugadores, config
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error al leer JSON: {e}")
        sys.exit(1)

def cargar_imagenes():
    imagenes = {}
    try:
        img_w = max(16, sx(50))
        img_h = max(16, sy(50))

        mapping = [
            ("AC Milan", "AC Milan.png"),
            ("Inter de Milán", "Inter de Milán.png"),
            ("Juventus", "Juventus.png"),
            ("Real Madrid", "Real Madrid.png"),
            ("Barcelona", "Barcelona.png"),
            ("Atlético de Madrid", "Atlético de Madrid.png"),
            ("Manchester United", "Manchester United.png"),
            ("Liverpool", "Liverpool.png"),
            ("Chelsea", "Chelsea.png"),
            ("Manchester City", "Manchester City.png"),
            ("Arsenal", "Arsenal.png"),
            ("Tottenham Hotspur", "Tottenham Hotspur.png"),
            ("Bayern de Múnich", "Bayern de Múnich.png"),
            ("Borussia Dortmund", "Borussia Dortmund.png"),
            ("Paris Saint-Germain", "Paris Saint-Germain.png"),
            ("Argentina", "Argentina.png"),
            ("Brasil", "Brasil.png"),
            ("Alemania", "Alemania.png"),
            ("Francia", "Francia.png"),
            ("España", "España.png"),
            ("Italia", "Italia.png"),
            ("Inglaterra", "Inglaterra.png"),
            ("Países Bajos", "Países Bajos.png"),
        ]

        for key, filename in mapping:
            path = os.path.join("image", "image_fut", filename)
            imagen = pygame.image.load(path)
            imagen = pygame.transform.scale(imagen, (img_w, img_h))
            imagenes[key] = imagen

        print("Imágenes cargadas correctamente")
    except Exception as e:
        print(f"Error al cargar imágenes: {e}")
        imagenes = None

    return imagenes

def generar_grid(config):
    selecciones_en_filas = random.choice([True, False])
    
    categorias_filas = []
    categorias_cols = []
    
    equipos_disponibles = config["equipos"].copy()
    random.shuffle(equipos_disponibles)
    selecciones_disponibles = config["selecciones"].copy()
    random.shuffle(selecciones_disponibles)
    
    if selecciones_en_filas:
        num_selecciones = random.randint(1, 3)
        for i in range(3):
            if i < num_selecciones:
                categorias_filas.append(("seleccion", selecciones_disponibles[i]))
            else:
                categorias_filas.append(("equipo", equipos_disponibles[i]))
        
        for i in range(3):
            idx = num_selecciones + (3 - num_selecciones) + i
            categorias_cols.append(("equipo", equipos_disponibles[idx % len(equipos_disponibles)]))
    else:
        for i in range(3):
            categorias_filas.append(("equipo", equipos_disponibles[i]))
        
        num_selecciones = random.randint(1, 3)
        for i in range(3):
            if i < num_selecciones:
                categorias_cols.append(("seleccion", selecciones_disponibles[i]))
            else:
                categorias_cols.append(("equipo", equipos_disponibles[i + 3]))
    
    return categorias_filas, categorias_cols

def jugador_cumple(jugador, cat_fila, cat_col):
    cumple_fila = False
    cumple_col = False
    
    tipo_fila, valor_fila = cat_fila
    tipo_col, valor_col = cat_col
    
    if tipo_fila == "equipo":
        cumple_fila = valor_fila in jugador["clubes totales"]
    else:
        cumple_fila = valor_fila in jugador["nacionalidad"]
    
    if tipo_col == "equipo":
        cumple_col = valor_col in jugador["clubes totales"]
    else:
        cumple_col = valor_col in jugador["nacionalidad"]
    
    return cumple_fila and cumple_col

class MenuPrincipal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.Font(None, max(16, sx(80)))
        self.fuente_opcion = pygame.font.Font(None, max(12, sx(40)))
        self.fuente_pequena = pygame.font.Font(None, max(10, sx(30)))
        
        # Definir botones del menú
        self.botones = [
            {"texto": "SIN TIEMPO", "tiempo": None, "rect": pygame.Rect(sx(300), sy(250), sx(400), sy(70))},
            {"texto": "90 SEGUNDOS", "tiempo": 90, "rect": pygame.Rect(sx(300), sy(340), sx(400), sy(70))},
            {"texto": "60 SEGUNDOS", "tiempo": 60, "rect": pygame.Rect(sx(300), sy(430), sx(400), sy(70))},
            {"texto": "40 SEGUNDOS", "tiempo": 40, "rect": pygame.Rect(sx(300), sy(520), sx(400), sy(70))},
            {"texto": "SALIR", "tiempo": "salir", "rect": pygame.Rect(sx(300), sy(610), sx(400), sy(70))}
        ]
        
        self.boton_hover = None
    
    def dibujar(self):
        self.pantalla.fill(AZUL)
        
        # Título
        titulo = self.fuente_titulo.render("FÚTBOL GRID", True, AMARILLO)
        rect_titulo = titulo.get_rect(center=(ANCHO // 2, sy(120)))
        self.pantalla.blit(titulo, rect_titulo)
        
        # Subtítulo
        subtitulo = self.fuente_pequena.render("Selecciona el modo de juego:", True, BLANCO)
        rect_subtitulo = subtitulo.get_rect(center=(ANCHO // 2, sy(190)))
        self.pantalla.blit(subtitulo, rect_subtitulo)
        
        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        
        for i, boton in enumerate(self.botones):
            # Color según hover
            if boton["rect"].collidepoint(mouse_pos):
                color = AMARILLO
                color_texto = AZUL
                self.boton_hover = i
            else:
                if boton["tiempo"] == "salir":
                    color = ROJO
                else:
                    color = BLANCO
                color_texto = AZUL
            
            # Dibujar botón
            pygame.draw.rect(self.pantalla, color, boton["rect"])
            pygame.draw.rect(self.pantalla, NEGRO, boton["rect"], 3)
            
            # Texto del botón
            texto = self.fuente_opcion.render(boton["texto"], True, color_texto)
            rect_texto = texto.get_rect(center=boton["rect"].center)
            self.pantalla.blit(texto, rect_texto)
    
    def manejar_clic(self, pos):
        for boton in self.botones:
            if boton["rect"].collidepoint(pos):
                return boton["tiempo"]
        return False

class FutbolGrid:
    def __init__(self, tiempo_limite=None):
        # Usar la pantalla inicializada por display_config
        self.pantalla = pantalla
        pygame.display.set_caption("Fútbol Grid")
        self.reloj = pygame.time.Clock()
        # Fuentes escaladas
        self.fuente = pygame.font.Font(None, max(10, sx(28)))
        self.fuente_pequena = pygame.font.Font(None, max(8, sx(20)))
        self.fuente_grande = pygame.font.Font(None, max(12, sx(36)))
        self.fuente_titulo = pygame.font.Font(None, max(14, sx(64)))
        self.fuente_tiempo = pygame.font.Font(None, max(12, sx(48)))
        
        self.jugadores, self.config = cargar_datos()
        self.categorias_filas, self.categorias_cols = generar_grid(self.config)
        self.imagenes = cargar_imagenes()
        
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.input_texto = ""
        self.sugerencias = []
        self.jugador_seleccionado = None
        self.mostrando_menu_celdas = False
        self.celdas_validas = []
        self.input_activo = True
        self.juego_terminado = False
        
        # Sistema de tiempo
        self.tiempo_limite = tiempo_limite
        self.tiempo_restante = tiempo_limite if tiempo_limite else None
        self.tiempo_inicio = pygame.time.get_ticks() if tiempo_limite else None
        self.tiempo_perdido = False
        
        # Variables para el sistema de mensajes
        self.jugadores_usados = set()
        self.mensaje_error = ""
        self.tiempo_mensaje = 0
        
    def actualizar_tiempo(self):
        if self.tiempo_limite and not self.juego_terminado and not self.tiempo_perdido:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) / 1000
            self.tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
            
            if self.tiempo_restante <= 0:
                self.tiempo_perdido = True
                self.juego_terminado = True
    
    def verificar_juego_terminado(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] is None:
                    return False
        return True
    
    def buscar_jugador(self, nombre):
        nombre_lower = nombre.lower().strip()
        for jugador in self.jugadores:
            # Buscar por nombre si existe
            if "nombre" in jugador:
                nombre_jugador = jugador["nombre"].lower().strip()
                if nombre_jugador == nombre_lower:
                    return jugador
                if nombre_jugador.split()[-1] == nombre_lower:
                    return jugador
            # Buscar por apodo si existe
            if "apodo" in jugador:
                apodo_lower = jugador["apodo"].lower().strip()
                if apodo_lower == nombre_lower:
                    return jugador
        return None
    
    def obtener_sugerencias(self, texto):
        if len(texto) < 1:
            return []
        sugerencias = []
        texto_lower = texto.lower().strip()
        
        for jugador in self.jugadores:
            # Primero verificar si coincide con el apodo
            if "apodo" in jugador:
                apodo = jugador["apodo"]
                apodo_lower = apodo.lower()
                if texto_lower in apodo_lower:
                    sugerencias.append(apodo)
                    if len(sugerencias) >= 5:
                        break
                    continue  # Si encontramos por apodo, pasar al siguiente jugador
            
            # Si no tiene apodo o no coincidió con el apodo, buscar por nombre
            if "nombre" in jugador:
                nombre_completo = jugador["nombre"]
                nombre_lower = nombre_completo.lower()
                if texto_lower in nombre_lower:
                    sugerencias.append(nombre_completo)
                    if len(sugerencias) >= 5:
                        break
        
        return sugerencias
    
    def encontrar_celdas_validas(self, jugador):
        celdas = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] is None:
                    if jugador_cumple(jugador, self.categorias_filas[i], self.categorias_cols[j]):
                        celdas.append((i, j))
        return celdas
    
    def mostrar_mensaje(self, mensaje, duracion=3000):
        """Muestra un mensaje temporal en pantalla (duracion en milisegundos)"""
        self.mensaje_error = mensaje
        self.tiempo_mensaje = pygame.time.get_ticks() + duracion
    
    def dibujar_tiempo(self):
        """Dibuja el temporizador en la parte superior"""
        if self.tiempo_limite:
            if self.tiempo_restante <= 10:
                color = ROJO
            elif self.tiempo_restante <= 20:
                color = NARANJA
            else:
                color = VERDE
            
            minutos = int(self.tiempo_restante // 60)
            segundos = int(self.tiempo_restante % 60)
            texto_tiempo = f"{minutos:02d}:{segundos:02d}"
            
            texto = self.fuente_tiempo.render(texto_tiempo, True, color)
            rect_texto = texto.get_rect(center=(ANCHO // 2, sy(60)))
            
            # Fondo para el tiempo (ligeramente escalado)
            pygame.draw.rect(self.pantalla, BLANCO, (rect_texto.x - sx(10), rect_texto.y - sy(5), rect_texto.width + sx(20), rect_texto.height + sy(10)))
            pygame.draw.rect(self.pantalla, NEGRO, (rect_texto.x - sx(10), rect_texto.y - sy(5), rect_texto.width + sx(20), rect_texto.height + sy(10)), max(1, sx(3)))
            
            self.pantalla.blit(texto, rect_texto)
    
    def dibujar_mensaje_error(self):
        """Dibuja el mensaje de error si hay uno activo"""
        if self.mensaje_error and pygame.time.get_ticks() < self.tiempo_mensaje:
            # Fondo del mensaje (escalado)
            ancho_msg = sx(700)
            alto_msg = sy(60)
            x = (ANCHO - ancho_msg) // 2
            y = ALTO - sy(100)
            
            pygame.draw.rect(self.pantalla, ROJO, (x, y, ancho_msg, alto_msg))
            pygame.draw.rect(self.pantalla, NEGRO, (x, y, ancho_msg, alto_msg), max(1, sx(3)))
            
            # Texto del mensaje
            texto = self.fuente.render(self.mensaje_error, True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, y + alto_msg // 2))
            self.pantalla.blit(texto, rect_texto)
        elif pygame.time.get_ticks() >= self.tiempo_mensaje:
            # Limpiar el mensaje cuando expire
            self.mensaje_error = ""
    
    def dibujar_grid(self):
        # Calcular tamaño total de la grilla (3 celdas y 2 márgenes) y centrarla
        total_grid_width = 3 * TAMANO_CELDA + 2 * MARGEN
        total_grid_height = 3 * TAMANO_CELDA + 2 * MARGEN
        # Centrar horizontalmente, dejando un margen mínimo a los lados
        inicio_x = max(sx(50), (ANCHO - total_grid_width) // 2)
        # Intentar centrar verticalmente pero mantener un margen superior mínimo
        inicio_y = max(sy(100), (ALTO - total_grid_height) // 2 - sy(20))

        # Guardar posiciones de la grilla para que otras partes (input) sepan dónde colocar elementos
        self.grid_inicio_x = inicio_x
        self.grid_inicio_y = inicio_y
        self.grid_total_width = total_grid_width
        self.grid_total_height = total_grid_height

        # Encabezados de columnas
        for j in range(3):
            tipo, valor = self.categorias_cols[j]
            x = inicio_x + j * (TAMANO_CELDA + MARGEN)
            y = inicio_y - sy(50)
            if tipo == "equipo":
                color = AZUL
            if tipo == "seleccion":
                color = AZUL

            if tipo == "equipo" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + TAMANO_CELDA // 2, y - sy(25)))
                self.pantalla.blit(imagen, rect_img)

            if tipo == "seleccion" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + TAMANO_CELDA // 2, y - sy(25)))
                self.pantalla.blit(imagen, rect_img)

            texto = self.fuente_pequena.render(valor, True, color)
            rect_texto = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + sy(10)))
            self.pantalla.blit(texto, rect_texto)

        # Encabezados de filas
        for i in range(3):
            tipo, valor = self.categorias_filas[i]
            x = inicio_x - sx(150)
            y = inicio_y + i * (TAMANO_CELDA + MARGEN)
            if tipo == "equipo":
                color = AZUL
            if tipo == "seleccion":
                color = AZUL

            if tipo == "equipo" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + sx(75), y + sy(30)))
                self.pantalla.blit(imagen, rect_img)
            
            if tipo == "seleccion" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + sx(75), y + sy(30)))
                self.pantalla.blit(imagen, rect_img)

            texto = self.fuente_pequena.render(valor, True, color)
            rect_texto = texto.get_rect(center=(x + sx(75), y + TAMANO_CELDA // 2))
            self.pantalla.blit(texto, rect_texto)

        # Dibujar celdas
        for i in range(3):
            for j in range(3):
                x = inicio_x + j * (TAMANO_CELDA + MARGEN)
                y = inicio_y + i * (TAMANO_CELDA + MARGEN)
                
                color = GRIS
                if self.mostrando_menu_celdas and (i, j) in self.celdas_validas:
                    color = VERDE
                
                pygame.draw.rect(self.pantalla, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(self.pantalla, NEGRO, (x, y, TAMANO_CELDA, TAMANO_CELDA), max(1, sx(2)))
                
                if self.grid[i][j]:
                    jugador = self.grid[i][j]
                    # Mostrar el nombre o apodo del jugador
                    if "apodo" in jugador:
                        nombre = jugador["apodo"]
                    elif "nombre" in jugador:
                        nombre = jugador["nombre"].split()[-1]
                    else:
                        nombre = "?"
                    
                    texto = self.fuente_pequena.render(nombre, True, NEGRO)
                    rect_texto = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                    self.pantalla.blit(texto, rect_texto)

    def calcular_posiciones_input(self):
        """Calcula y guarda las coordenadas del área de input"""
        ancho_input = min(sx(900), ANCHO - sx(100))
        x_input = (ANCHO - ancho_input) // 2
        base_y = getattr(self, 'grid_inicio_y', sy(150))
        total_h = getattr(self, 'grid_total_height', 3 * TAMANO_CELDA + 2 * MARGEN)
        y = base_y + total_h + sy(20)
        
        self.input_x = x_input
        self.input_y = y
        self.input_ancho = ancho_input
        self.input_alto = sy(40)

    def dibujar_input(self):
        # Calcular posiciones primero
        self.calcular_posiciones_input()
        
        x_input = self.input_x
        y = self.input_y
        ancho_input = self.input_ancho

        color_fondo = AMARILLO if self.input_activo else BLANCO
        pygame.draw.rect(self.pantalla, color_fondo, (x_input, y, ancho_input, sy(40)))
        pygame.draw.rect(self.pantalla, NEGRO, (x_input, y, ancho_input, sy(40)), max(1, sx(3)))
        
        texto = self.fuente.render(self.input_texto, True, NEGRO)
        self.pantalla.blit(texto, (x_input + sx(10), y + sy(8)))
        
        if self.input_activo and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = x_input + sx(10) + texto.get_width() + 2
            pygame.draw.line(self.pantalla, NEGRO, (cursor_x, y + sy(8)), (cursor_x, y + sy(32)), max(1, sx(2)))
        
        if self.sugerencias:
            y_sug = y + sy(45)
            for i, sugerencia in enumerate(self.sugerencias):
                rect_sug = pygame.Rect(x_input, y_sug + i * sy(35), ancho_input, sy(33))
                pygame.draw.rect(self.pantalla, GRIS, rect_sug)
                pygame.draw.rect(self.pantalla, NEGRO, rect_sug, max(1, sx(1)))
                texto = self.fuente_pequena.render(sugerencia, True, NEGRO)
                self.pantalla.blit(texto, (x_input + sx(10), y_sug + i * sy(35) + sy(8)))
    
    def dibujar_menu_celdas(self):
        ancho_menu = sx(400)
        alto_menu = min(sy(300), sy(70 + len(self.celdas_validas) * 50))
        x = (ANCHO - ancho_menu) // 2
        y = (ALTO - alto_menu) // 2

        pygame.draw.rect(self.pantalla, BLANCO, (x, y, ancho_menu, alto_menu))
        pygame.draw.rect(self.pantalla, NEGRO, (x, y, ancho_menu, alto_menu), max(1, sx(3)))

        texto = self.fuente_grande.render("Elige una celda:", True, NEGRO)
        self.pantalla.blit(texto, (x + sx(20), y + sy(20)))

        y_celda = y + sy(70)
        for idx, (i, j) in enumerate(self.celdas_validas):
            tipo_fila, valor_fila = self.categorias_filas[i]
            tipo_col, valor_col = self.categorias_cols[j]
            
            pygame.draw.rect(self.pantalla, AZUL_CLARO, (x + sx(20), y_celda + idx * sy(50), sx(360), sy(45)))
            pygame.draw.rect(self.pantalla, NEGRO, (x + sx(20), y_celda + idx * sy(50), sx(360), sy(45)), max(1, sx(2)))
            
            texto_celda = f"{valor_fila} x {valor_col}"
            texto = self.fuente.render(texto_celda, True, NEGRO)
            self.pantalla.blit(texto, (x + sx(30), y_celda + idx * sy(50) + sy(10)))
    
    def manejar_clic_menu(self, pos):
        ancho_menu = sx(400)
        alto_menu = min(sy(300), sy(70 + len(self.celdas_validas) * 50))
        x = (ANCHO - ancho_menu) // 2
        y = (ALTO - alto_menu) // 2
        y_celda = y + sy(70)

        for idx, (i, j) in enumerate(self.celdas_validas):
            rect = pygame.Rect(x + sx(20), y_celda + idx * sy(50), sx(360), sy(45))
            if rect.collidepoint(pos):
                self.grid[i][j] = self.jugador_seleccionado
                # Obtener identificador único del jugador
                identificador = self.jugador_seleccionado.get("nombre") or self.jugador_seleccionado.get("apodo", "desconocido")
                self.jugadores_usados.add(identificador)
                if "Juanjo Shlamovitz" in identificador:
                    self.mostrar_mensaje("Bro realmente tuvo que poner a Juanjo porque no sabe de futbol")

                self.mostrando_menu_celdas = False
                self.jugador_seleccionado = None
                self.celdas_validas = []
                self.input_texto = ""
                self.sugerencias = []
                
                if self.verificar_juego_terminado():
                    self.juego_terminado = True
                return
    
    def procesar_jugador(self, nombre_jugador):
        jugador = self.buscar_jugador(nombre_jugador)
        if jugador:
            # Obtener identificador único del jugador
            identificador = jugador.get("nombre") or jugador.get("apodo", "desconocido")
            
            # Verificar si el jugador ya fue usado
            if identificador in self.jugadores_usados:
                self.mostrar_mensaje(f"¡{identificador} ya fue seleccionado!")
                self.input_texto = ""
                self.sugerencias = []
                return
            
            
            celdas = self.encontrar_celdas_validas(jugador)
            if celdas:
                if len(celdas) == 1:
                    i, j = celdas[0]
                    self.grid[i][j] = jugador
                    self.jugadores_usados.add(identificador)
                    self.input_texto = ""
                    self.sugerencias = []
                    
                    if self.verificar_juego_terminado():
                        self.juego_terminado = True
                else:
                    self.jugador_seleccionado = jugador
                    self.celdas_validas = celdas
                    self.mostrando_menu_celdas = True

            else:
                if "apodo" in jugador:
                    self.mostrar_mensaje(f"{jugador['apodo']} no encaja en ninguna celda disponible")
                    self.input_texto = ""
                    self.sugerencias = []
                else:
                    self.mostrar_mensaje(f"{jugador['nombre']} no encaja en ninguna celda disponible")
                    self.input_texto = ""
                    self.sugerencias = []
        else:
            self.mostrar_mensaje(f"No se encontró el jugador: {nombre_jugador}")
            self.input_texto = ""
            self.sugerencias = []
        
    def ejecutar(self):
        ejecutando = True
        
        while ejecutando:
            self.reloj.tick(FPS)
            
            # Actualizar tiempo si hay límite
            self.actualizar_tiempo()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"
                    
                    if not self.juego_terminado and not self.mostrando_menu_celdas:
                        if evento.key == pygame.K_BACKSPACE:
                            self.input_texto = self.input_texto[:-1]
                            self.sugerencias = self.obtener_sugerencias(self.input_texto)
                        elif evento.key == pygame.K_RETURN:
                            if self.input_texto:
                                self.procesar_jugador(self.input_texto)
                        else:
                            if len(evento.unicode) > 0 and evento.unicode.isprintable():
                                self.input_texto += evento.unicode
                                self.sugerencias = self.obtener_sugerencias(self.input_texto)
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.mostrando_menu_celdas:
                        self.manejar_clic_menu(evento.pos)
                    elif not self.juego_terminado:
                        # Asegurarse de que las posiciones estén calculadas
                        self.calcular_posiciones_input()
                        
                        rect_input = pygame.Rect(self.input_x, self.input_y, self.input_ancho, self.input_alto)
                        if rect_input.collidepoint(evento.pos):
                            self.input_activo = True
                        if self.sugerencias:
                            y_sug = self.input_y + sy(45)  # Usar la misma fórmula que en dibujar_input()
                            for i, sugerencia in enumerate(self.sugerencias):
                                rect = pygame.Rect(self.input_x, y_sug + i * sy(35), self.input_ancho, sy(33))
                                if rect.collidepoint(evento.pos):
                                    self.input_texto = sugerencia
                                    self.sugerencias = []
                                    self.procesar_jugador(sugerencia)
                                    break
            
            # Determinar color de fondo según el estado
            if self.juego_terminado:
                if self.tiempo_perdido:
                    self.pantalla.fill(ROJO)
                else:
                    self.pantalla.fill(VERDE)
            else:
                self.pantalla.fill(BLANCO)
            
            # Título y tiempo
            if not self.juego_terminado:
                titulo = self.fuente_grande.render("FÚTBOL GRID", True, NEGRO)
                rect_titulo = titulo.get_rect(center=(ANCHO // 2, sy(30)))
                self.pantalla.blit(titulo, rect_titulo)
                self.dibujar_tiempo()
            
            self.dibujar_grid()
            
            if self.juego_terminado:
                if self.tiempo_perdido:
                    # Perdiste por tiempo
                    texto_terminado = self.fuente_titulo.render("TIEMPO AGOTADO", True, BLANCO)
                    rect_terminado = texto_terminado.get_rect(center=(ANCHO // 2, sy(650)))
                    self.pantalla.blit(texto_terminado, rect_terminado)
                else:
                    # Ganaste completando el grid
                    texto_terminado = self.fuente_titulo.render("¡COMPLETADO!", True, BLANCO)
                    rect_terminado = texto_terminado.get_rect(center=(ANCHO // 2, sy(650)))
                    self.pantalla.blit(texto_terminado, rect_terminado)
                
                # Texto "Presiona ESC para volver al menú" debajo
                texto_esc = self.fuente_grande.render("Presiona ESC para volver al menú", True, BLANCO)
                rect_esc = texto_esc.get_rect(center=(ANCHO // 2, sy(720)))
                self.pantalla.blit(texto_esc, rect_esc)
            elif not self.mostrando_menu_celdas:
                self.dibujar_input()
                inst = self.fuente_pequena.render("Escribe el nombre de un jugador (presiona ESC para volver al menú)", True, GRIS_OSCURO)
                self.pantalla.blit(inst, (sx(50), sy(600)))
            else:
                self.dibujar_menu_celdas()
            
            # Mostrar mensajes de error si los hay
            self.dibujar_mensaje_error()
            
            pygame.display.flip()
        
        return "salir"

def main():
    # Usar la pantalla inicializada por display_config (variable `pantalla` ya definida)
    pygame.display.set_caption("Fútbol Grid")
    reloj = pygame.time.Clock()
    
    estado = "menu"
    
    while True:
        if estado == "menu":
            menu = MenuPrincipal(pantalla)
            
            while estado == "menu":
                reloj.tick(FPS)
                
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        opcion = menu.manejar_clic(evento.pos)
                        if opcion == "salir":
                            pygame.quit()
                            sys.exit()
                        elif opcion is not False:
                            estado = "juego"
                            tiempo_seleccionado = opcion
                            break
                
                menu.dibujar()
                pygame.display.flip()
        
        elif estado == "juego":
            juego = FutbolGrid(tiempo_limite=tiempo_seleccionado)
            resultado = juego.ejecutar()
            
            if resultado == "menu":
                estado = "menu"
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()