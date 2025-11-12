import os
import pygame
import json
import random
import sys

# Inicializar Pygame
pygame.init()

from display_config import init_display

# Constantes
ANCHO = 1000
ALTO = 800
TAMANO_CELDA = 150
MARGEN = 10
FPS = 60

# Inicializar pantalla con resolucion desde game_settings.json
pantalla, ANCHO, ALTO = init_display(default_w=ANCHO, default_h=ALTO, title="Grid Futbol")

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
        imagenes['AC Milan'] = pygame.image.load(os.path.join("image", "image_fut", "AC Milan.png"))
        imagenes['AC Milan'] = pygame.transform.scale(imagenes['AC Milan'], (50,50))

        imagenes['Inter de Milán'] = pygame.image.load(os.path.join("image", "image_fut", "Inter de Milán.png"))
        imagenes['Inter de Milán'] = pygame.transform.scale(imagenes['Inter de Milán'], (50,50))

        imagenes['Juventus'] = pygame.image.load(os.path.join("image", "image_fut", "Juventus.png"))
        imagenes['Juventus'] = pygame.transform.scale(imagenes['Juventus'], (50,50))

        imagenes['Real Madrid'] = pygame.image.load(os.path.join("image", "image_fut", "Real Madrid.png"))
        imagenes['Real Madrid'] = pygame.transform.scale(imagenes['Real Madrid'], (50,50))

        imagenes['Barcelona'] = pygame.image.load(os.path.join("image", "image_fut", "Barcelona.png"))
        imagenes['Barcelona'] = pygame.transform.scale(imagenes['Barcelona'], (50,50))

        imagenes['Atlético de Madrid'] = pygame.image.load(os.path.join("image", "image_fut", "Atlético de Madrid.png"))
        imagenes['Atlético de Madrid'] = pygame.transform.scale(imagenes['Atlético de Madrid'], (50,50))

        imagenes['Manchester United'] = pygame.image.load(os.path.join("image", "image_fut", "Manchester United.png"))
        imagenes['Manchester United'] = pygame.transform.scale(imagenes['Manchester United'], (50,50))

        imagenes['Liverpool'] = pygame.image.load(os.path.join("image", "image_fut", "Liverpool.png"))
        imagenes['Liverpool'] = pygame.transform.scale(imagenes['Liverpool'], (50,50))

        imagenes['Chelsea'] = pygame.image.load(os.path.join("image", "image_fut", "Chelsea.png"))
        imagenes['Chelsea'] = pygame.transform.scale(imagenes['Chelsea'], (50,50))

        imagenes['Manchester City'] = pygame.image.load(os.path.join("image", "image_fut", "Manchester City.png"))
        imagenes['Manchester City'] = pygame.transform.scale(imagenes['Manchester City'], (50,50))

        imagenes['Arsenal'] = pygame.image.load(os.path.join("image", "image_fut", "Arsenal.png"))
        imagenes['Arsenal'] = pygame.transform.scale(imagenes['Arsenal'], (50,50))

        imagenes['Tottenham Hotspur'] = pygame.image.load(os.path.join("image", "image_fut", "Tottenham Hotspur.png"))
        imagenes['Tottenham Hotspur'] = pygame.transform.scale(imagenes['Tottenham Hotspur'], (50,50))

        imagenes['Bayern de Múnich'] = pygame.image.load(os.path.join("image", "image_fut", "Bayern de Múnich.png"))
        imagenes['Bayern de Múnich'] = pygame.transform.scale(imagenes["Bayern de Múnich"], (50,50))

        imagenes['Borussia Dortmund'] = pygame.image.load(os.path.join("image", "image_fut", "Borussia Dortmund.png"))
        imagenes['Borussia Dortmund'] = pygame.transform.scale(imagenes['Borussia Dortmund'], (50,50))

        imagenes['Paris Saint-Germain'] = pygame.image.load(os.path.join("image", "image_fut", "Paris Saint-Germain.png"))
        imagenes['Paris Saint-Germain'] = pygame.transform.scale(imagenes['Paris Saint-Germain'], (50,50))

        imagenes["Argentina"] = pygame.image.load(os.path.join("image", "image_fut", "Argentina.png"))
        imagenes["Argentina"] = pygame.transform.scale(imagenes["Argentina"], (50,50))

        imagenes["Brasil"] = pygame.image.load(os.path.join("image", "image_fut", "Brasil.png"))
        imagenes["Brasil"] = pygame.transform.scale(imagenes["Brasil"], (50,50))

        imagenes["Alemania"] = pygame.image.load(os.path.join("image", "image_fut", "Alemania.png"))
        imagenes["Alemania"] = pygame.transform.scale(imagenes["Alemania"], (50,50))

        imagenes["Francia"] = pygame.image.load(os.path.join("image", "image_fut", "Francia.png"))
        imagenes["Francia"] = pygame.transform.scale(imagenes["Francia"], (50,50))

        imagenes["España"] = pygame.image.load(os.path.join("image", "image_fut", "España.png"))
        imagenes["España"] = pygame.transform.scale(imagenes["España"], (50,50))

        imagenes["Italia"] = pygame.image.load(os.path.join("image", "image_fut", "Italia.png"))
        imagenes["Italia"] = pygame.transform.scale(imagenes["Italia"], (50,50))

        imagenes["Inglaterra"] = pygame.image.load(os.path.join("image", "image_fut", "Inglaterra.png"))
        imagenes["Inglaterra"] = pygame.transform.scale(imagenes["Inglaterra"], (50,50))

        imagenes["Países Bajos"] = pygame.image.load(os.path.join("image", "image_fut", "Países Bajos.png"))
        imagenes["Países Bajos"] = pygame.transform.scale(imagenes["Países Bajos"], (50,50))

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
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_opcion = pygame.font.Font(None, 40)
        self.fuente_pequena = pygame.font.Font(None, 30)
        
        # Definir botones del menú
        self.botones = [
            {"texto": "SIN TIEMPO", "tiempo": None, "rect": pygame.Rect(300, 250, 400, 70)},
            {"texto": "90 SEGUNDOS", "tiempo": 90, "rect": pygame.Rect(300, 340, 400, 70)},
            {"texto": "60 SEGUNDOS", "tiempo": 60, "rect": pygame.Rect(300, 430, 400, 70)},
            {"texto": "40 SEGUNDOS", "tiempo": 40, "rect": pygame.Rect(300, 520, 400, 70)},
            {"texto": "SALIR", "tiempo": "salir", "rect": pygame.Rect(300, 610, 400, 70)}
        ]
        
        self.boton_hover = None
    
    def dibujar(self):
        self.pantalla.fill(AZUL)
        
        # Título
        titulo = self.fuente_titulo.render("FÚTBOL GRID", True, AMARILLO)
        rect_titulo = titulo.get_rect(center=(ANCHO // 2, 120))
        self.pantalla.blit(titulo, rect_titulo)
        
        # Subtítulo
        subtitulo = self.fuente_pequena.render("Selecciona el modo de juego:", True, BLANCO)
        rect_subtitulo = subtitulo.get_rect(center=(ANCHO // 2, 190))
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
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Fútbol Grid")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 28)
        self.fuente_pequena = pygame.font.Font(None, 20)
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_tiempo = pygame.font.Font(None, 48)
        
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
            nombre_jugador = jugador["nombre"].lower().strip()
            if nombre_jugador == nombre_lower:
                return jugador
            if nombre_jugador.split()[-1] == nombre_lower:
                return jugador
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
            nombre_completo = jugador["nombre"]
            nombre_lower = nombre_completo.lower()
            if texto_lower in nombre_lower:
                sugerencias.append(nombre_completo)
            elif "apodo" in jugador and texto_lower in jugador["apodo"].lower():
                apodo = jugador["apodo"]
                sugerencias.append(apodo)
            
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
            rect_texto = texto.get_rect(center=(ANCHO // 2, 60))
            
            # Fondo para el tiempo
            pygame.draw.rect(self.pantalla, BLANCO, (rect_texto.x - 10, rect_texto.y - 5, rect_texto.width + 20, rect_texto.height + 10))
            pygame.draw.rect(self.pantalla, NEGRO, (rect_texto.x - 10, rect_texto.y - 5, rect_texto.width + 20, rect_texto.height + 10), 3)
            
            self.pantalla.blit(texto, rect_texto)
    
    def dibujar_mensaje_error(self):
        """Dibuja el mensaje de error si hay uno activo"""
        if self.mensaje_error and pygame.time.get_ticks() < self.tiempo_mensaje:
            # Fondo del mensaje
            ancho_msg = 700
            alto_msg = 60
            x = (ANCHO - ancho_msg) // 2
            y = 700
            
            pygame.draw.rect(self.pantalla, ROJO, (x, y, ancho_msg, alto_msg))
            pygame.draw.rect(self.pantalla, NEGRO, (x, y, ancho_msg, alto_msg), 3)
            
            # Texto del mensaje
            texto = self.fuente.render(self.mensaje_error, True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, y + 30))
            self.pantalla.blit(texto, rect_texto)
        elif pygame.time.get_ticks() >= self.tiempo_mensaje:
            # Limpiar el mensaje cuando expire
            self.mensaje_error = ""
    
    def dibujar_grid(self):
        inicio_x = 200
        inicio_y = 150

        # Encabezados de columnas
        for j in range(3):
            tipo, valor = self.categorias_cols[j]
            x = inicio_x + j * (TAMANO_CELDA + MARGEN)
            y = inicio_y - 50
            if tipo == "equipo":
                color = AZUL
            if tipo == "seleccion":
                color = AZUL

            if tipo == "equipo" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + TAMANO_CELDA // 2, y - 25))
                self.pantalla.blit(imagen, rect_img)

            if tipo == "seleccion" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + TAMANO_CELDA // 2, y - 25))
                self.pantalla.blit(imagen, rect_img)

            texto = self.fuente_pequena.render(valor, True, color)
            rect_texto = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + 10))
            self.pantalla.blit(texto, rect_texto)

        # Encabezados de filas
        for i in range(3):
            tipo, valor = self.categorias_filas[i]
            x = inicio_x - 150
            y = inicio_y + i * (TAMANO_CELDA + MARGEN)
            if tipo == "equipo":
                color = AZUL
            if tipo == "seleccion":
                color = AZUL

            if tipo == "equipo" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + 75, y + 30))
                self.pantalla.blit(imagen, rect_img)
            
            if tipo == "seleccion" and valor in self.imagenes:
                imagen = self.imagenes[valor]
                rect_img = imagen.get_rect(center=(x + 75, y + 30))
                self.pantalla.blit(imagen, rect_img)

            texto = self.fuente_pequena.render(valor, True, color)
            rect_texto = texto.get_rect(center=(x + 75, y + TAMANO_CELDA // 2))
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
                pygame.draw.rect(self.pantalla, NEGRO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)
                
                if self.grid[i][j]:
                    jugador = self.grid[i][j]
                    # Mostrar el nombre o apodo del jugador
                    if "apodo" in jugador:
                        nombre = jugador["apodo"]
                    else:
                        nombre = jugador["nombre"].split()[-1]
                    
                    texto = self.fuente_pequena.render(nombre, True, NEGRO)
                    rect_texto = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                    self.pantalla.blit(texto, rect_texto)

    def dibujar_input(self):
        y = 625
        color_fondo = AMARILLO if self.input_activo else BLANCO
        pygame.draw.rect(self.pantalla, color_fondo, (50, 625, 900, 40))
        pygame.draw.rect(self.pantalla, NEGRO, (50, 625, 900, 40), 3)
        
        texto = self.fuente.render(self.input_texto, True, NEGRO)
        self.pantalla.blit(texto, (60, y + 8))
        
        if self.input_activo and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 60 + texto.get_width() + 2
            pygame.draw.line(self.pantalla, NEGRO, (cursor_x, y + 8), (cursor_x, y + 32), 2)
        
        if self.sugerencias:
            y_sug = y + 45
            for i, sugerencia in enumerate(self.sugerencias):
                rect_sug = pygame.Rect(50, y_sug + i * 35, 900, 33)
                pygame.draw.rect(self.pantalla, GRIS, rect_sug)
                pygame.draw.rect(self.pantalla, NEGRO, rect_sug, 1)
                texto = self.fuente_pequena.render(sugerencia, True, NEGRO)
                self.pantalla.blit(texto, (60, y_sug + i * 35 + 8))
    
    def dibujar_menu_celdas(self):
        ancho_menu = 400
        alto_menu = min(300, 70 + len(self.celdas_validas) * 50)
        x = (ANCHO - ancho_menu) // 2
        y = (ALTO - alto_menu) // 2
        
        pygame.draw.rect(self.pantalla, BLANCO, (x, y, ancho_menu, alto_menu))
        pygame.draw.rect(self.pantalla, NEGRO, (x, y, ancho_menu, alto_menu), 3)
        
        texto = self.fuente_grande.render("Elige una celda:", True, NEGRO)
        self.pantalla.blit(texto, (x + 20, y + 20))
        
        y_celda = y + 70
        for idx, (i, j) in enumerate(self.celdas_validas):
            tipo_fila, valor_fila = self.categorias_filas[i]
            tipo_col, valor_col = self.categorias_cols[j]
            
            pygame.draw.rect(self.pantalla, AZUL_CLARO, (x + 20, y_celda + idx * 50, 360, 45))
            pygame.draw.rect(self.pantalla, NEGRO, (x + 20, y_celda + idx * 50, 360, 45), 2)
            
            texto_celda = f"{valor_fila} x {valor_col}"
            texto = self.fuente.render(texto_celda, True, NEGRO)
            self.pantalla.blit(texto, (x + 30, y_celda + idx * 50 + 10))
    
    def manejar_clic_menu(self, pos):
        ancho_menu = 400
        alto_menu = min(300, 70 + len(self.celdas_validas) * 50)
        x = (ANCHO - ancho_menu) // 2
        y = (ALTO - alto_menu) // 2
        y_celda = y + 70
        
        for idx, (i, j) in enumerate(self.celdas_validas):
            rect = pygame.Rect(x + 20, y_celda + idx * 50, 360, 45)
            if rect.collidepoint(pos):
                self.grid[i][j] = self.jugador_seleccionado
                self.jugadores_usados.add(self.jugador_seleccionado["nombre"])
                if "Juanjo Shlamovitz" in self.jugador_seleccionado["nombre"]:
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
            # Verificar si el jugador ya fue usado
            if jugador["nombre"] in self.jugadores_usados:
                self.mostrar_mensaje(f"¡{jugador['nombre']} ya fue seleccionado!")
                self.input_texto = ""
                self.sugerencias = []
                return
            
            
            celdas = self.encontrar_celdas_validas(jugador)
            if celdas:
                if len(celdas) == 1:
                    i, j = celdas[0]
                    self.grid[i][j] = jugador
                    self.jugadores_usados.add(jugador["nombre"])
                    self.input_texto = ""
                    self.sugerencias = []
                    
                    if self.verificar_juego_terminado():
                        self.juego_terminado = True
                else:
                    self.jugador_seleccionado = jugador
                    self.celdas_validas = celdas
                    self.mostrando_menu_celdas = True

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
                        rect_input = pygame.Rect(50, 625, 900, 40)
                        if rect_input.collidepoint(evento.pos):
                            self.input_activo = True
                        if self.sugerencias:
                            y_sug = 670
                            for i, sugerencia in enumerate(self.sugerencias):
                                rect = pygame.Rect(50, y_sug + i * 35, 900, 33)
                                if rect.collidepoint(evento.pos):
                                    self.input_texto = sugerencia
                                    self.sugerencias = []
                                    self.procesar_jugador(sugerencia)
                                    break
                        
                        rect_input = pygame.Rect(50, 625, 900, 40)
                        if rect_input.collidepoint(evento.pos):
                            self.input_activo = True
            
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
                self.pantalla.blit(titulo, (ANCHO // 2 - 100, 10))
                self.dibujar_tiempo()
            
            self.dibujar_grid()
            
            if self.juego_terminado:
                if self.tiempo_perdido:
                    # Perdiste por tiempo
                    texto_terminado = self.fuente_titulo.render("TIEMPO AGOTADO", True, BLANCO)
                    rect_terminado = texto_terminado.get_rect(center=(ANCHO // 2, 650))
                    self.pantalla.blit(texto_terminado, rect_terminado)
                else:
                    # Ganaste completando el grid
                    texto_terminado = self.fuente_titulo.render("¡COMPLETADO!", True, BLANCO)
                    rect_terminado = texto_terminado.get_rect(center=(ANCHO // 2, 650))
                    self.pantalla.blit(texto_terminado, rect_terminado)
                
                # Texto "Presiona ESC para volver al menú" debajo
                texto_esc = self.fuente_grande.render("Presiona ESC para volver al menú", True, BLANCO)
                rect_esc = texto_esc.get_rect(center=(ANCHO // 2, 720))
                self.pantalla.blit(texto_esc, rect_esc)
            elif not self.mostrando_menu_celdas:
                self.dibujar_input()
                inst = self.fuente_pequena.render("Escribe el nombre de un jugador (presiona ESC para volver al menú)", True, GRIS_OSCURO)
                self.pantalla.blit(inst, (50, 600))
            else:
                self.dibujar_menu_celdas()
            
            # Mostrar mensajes de error si los hay
            self.dibujar_mensaje_error()
            
            pygame.display.flip()
        
        return "salir"

def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
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
