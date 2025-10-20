import os
import pygame
import json
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 1000
ALTO = 800
TAMANO_CELDA = 150
MARGEN = 10
FPS = 60

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
        cumple_fila = jugador["nacionalidad"] == valor_fila
    
    if tipo_col == "equipo":
        cumple_col = valor_col in jugador["clubes totales"]
    else:
        cumple_col = jugador["nacionalidad"] == valor_col
    
    return cumple_fila and cumple_col

class FutbolGrid:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Fútbol Grid")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 28)
        self.fuente_pequena = pygame.font.Font(None, 20)
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_titulo = pygame.font.Font(None, 64)
        
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
                rect_img = imagen.get_rect(center=(x + TAMANO_CELDA // 2, y - 20))
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
                rect_img = imagen.get_rect(center=(x + 75, y - 20))
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
        y = 600
        color_fondo = AMARILLO if self.input_activo else BLANCO
        pygame.draw.rect(self.pantalla, color_fondo, (50, y, 900, 40))
        pygame.draw.rect(self.pantalla, NEGRO, (50, y, 900, 40), 3)
        
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
            celdas = self.encontrar_celdas_validas(jugador)
            if celdas:
                if len(celdas) == 1:
                    i, j = celdas[0]
                    self.grid[i][j] = jugador
                    self.input_texto = ""
                    self.sugerencias = []
                    
                    if self.verificar_juego_terminado():
                        self.juego_terminado = True
                else:
                    self.jugador_seleccionado = jugador
                    self.celdas_validas = celdas
                    self.mostrando_menu_celdas = True
            else:
                print(f"El jugador {jugador['nombre']} no encaja en ninguna celda disponible")
                self.input_texto = ""
                self.sugerencias = []
        else:
            print(f"No se encontró el jugador: {nombre_jugador}")
            self.input_texto = ""
            self.sugerencias = []
    
    def ejecutar(self):
        ejecutando = True
        
        while ejecutando:
            self.reloj.tick(FPS)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    
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
                        if self.sugerencias:
                            y_sug = 645
                            for i, sugerencia in enumerate(self.sugerencias):
                                rect = pygame.Rect(50, y_sug + i * 35, 900, 33)
                                if rect.collidepoint(evento.pos):
                                    self.input_texto = sugerencia
                                    self.sugerencias = []
                                    self.procesar_jugador(sugerencia)
                                    break
                        
                        rect_input = pygame.Rect(50, 600, 900, 40)
                        if rect_input.collidepoint(evento.pos):
                            self.input_activo = True
            
            # Fondo verde cuando el juego termina, blanco cuando está jugando
            if self.juego_terminado:
                self.pantalla.fill(VERDE)
            else:
                self.pantalla.fill(BLANCO)
            
            # Título solo cuando NO ha terminado
            titulo = self.fuente_grande.render("FÚTBOL GRID", True, NEGRO)
            self.pantalla.blit(titulo, (ANCHO // 2 - 100, 30))
            
            self.dibujar_grid()
            
            if self.juego_terminado:
                # Texto "JUEGO TERMINADO" grande en el centro superior
                texto_terminado = self.fuente_titulo.render("JUEGO TERMINADO", True, BLANCO)
                rect_terminado = texto_terminado.get_rect(center=(ANCHO // 2, 650))
                self.pantalla.blit(texto_terminado, rect_terminado)
                
                # Texto "Presiona ESC para salir" debajo
                texto_esc = self.fuente_grande.render("Presiona ESC para salir", True, BLANCO)
                rect_esc = texto_esc.get_rect(center=(ANCHO // 2, 720))
                self.pantalla.blit(texto_esc, rect_esc)
            elif not self.mostrando_menu_celdas:
                self.dibujar_input()
                inst = self.fuente_pequena.render("Escribe el nombre de un jugador (presiona ESC para salir)", True, GRIS_OSCURO)
                self.pantalla.blit(inst, (50, 570))
            else:
                self.dibujar_menu_celdas()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = FutbolGrid()
    juego.ejecutar()