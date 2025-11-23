import pygame
import json
import sys
import random
from typing import List, Dict

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO = 1200
ALTO = 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Top 10 Fútbol")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (46, 204, 113)
ROJO = (231, 76, 60)
AZUL = (52, 152, 219)
GRIS = (189, 195, 199)
GRIS_OSCURO = (52, 73, 94)
VERDE_CLARO = (39, 174, 96)
AMARILLO = (241, 196, 15)
NARANJA = (230, 126, 34)

# Fuentes
fuente_titulo = pygame.font.Font(None, 52)
fuente_subtitulo = pygame.font.Font(None, 38)
fuente_texto = pygame.font.Font(None, 32)
fuente_pequeña = pygame.font.Font(None, 26)

# Cargar base de datos desde JSON
def cargar_jugadores():
    try:
        with open('basededatos.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['jugadores']
    except FileNotFoundError:
        print("Error: No se encontró el archivo basededatos.json")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo JSON está mal formateado")
        return []

# Cargar jugadores
jugadores_db = cargar_jugadores()
for jugador in jugadores_db:
    nacionalidad = jugador['nacionalidad']
    (nacionalidad, "nacionalidad.png")
    
banderas = {}

def cargar_banderas():
    """
    Carga las imágenes de banderas desde la carpeta 'image/'
    El nombre del archivo debe coincidir con la nacionalidad
    """
    nacionalidades_unicas = set()
    for jugador in jugadores_db:
        nacionalidad = jugador['nacionalidad']
        # Si la nacionalidad es una lista, tomar el primer elemento
        if isinstance(nacionalidad, list):
            if len(nacionalidad) > 0:
                nacionalidades_unicas.add(nacionalidad[0])
        else:
            nacionalidades_unicas.add(nacionalidad)
    
    for nacionalidad in nacionalidades_unicas:
        try:
            # Intenta cargar la imagen de la bandera
            ruta = f"image/image_fut/{nacionalidad}.png"
            imagen = pygame.image.load(ruta)
            # Redimensionar a 50x30 píxeles
            imagen = pygame.transform.scale(imagen, (50, 30))
            banderas[nacionalidad] = imagen
        except (pygame.error, FileNotFoundError):
            # Si no encuentra la imagen, crea un rectángulo de color como placeholder
            superficie = pygame.Surface((50, 30))
            superficie.fill(AZUL)
            banderas[nacionalidad] = superficie
            print(f"Advertencia: No se encontró la bandera para {nacionalidad}")

# Cargar banderas al inicio
cargar_banderas()

# Definición de diferentes tops
TOPS_DISPONIBLES = [
    {
        "titulo": "Jugadores con más Balones de Oro",
        "descripcion": "Los jugadores con más Balones de Oro en la historia",
        "jugadores_ids": [1, 2, 51, 74, 204, 75, 915, 914, 46, 27]
    },
    {
        "titulo": "Máximos Goleadores en Champions League",
        "descripcion": "Los máximos anotadores de la UEFA Champions League",
        "jugadores_ids": [2, 1, 20, 5, 153, 14, 201, 110, 19, 22]
    },
    {
        "titulo": "Goleadores en Mundiales (2002 - ...)",
        "descripcion": "Los máximos goleadores en Copas del Mundo desde 2002",
        "jugadores_ids": [62, 1, 14, 27, 201, 225, 3, 67, 2, 4]
    },
    {
        "titulo": "Goleadores de la Premier League (2000 - ...)",
        "descripcion": "Los máximos goleadores en la Premier League desde el año 2000",
        "jugadores_ids": [67, 37, 26, 18, 22, 141, 190, 94, 330, 95]
    },
    {
        "titulo": "Goleadores en LaLiga (2000 - ...)",
        "descripcion": "Los máximos goleadores en LaLiga desde el año 2000",
        "jugadores_ids": [1, 2, 5, 135, 225, 4, 916, 188, 917, 153]
    },
    {
        "titulo": "Jugadores con más partidos en AC Milan (Champions)",
        "descripcion": "Los jugadores con más apariciones en AC Milan en la Champions League",
        "jugadores_ids": [47, 100, 925, 913, 924, 25, 923, 926, 72, 927]
    },
    {
        "titulo": "Ranking Balón de Oro 2006",
        "descripcion": "Los 10 mejores jugadores según el Balón de Oro 2006",
        "jugadores_ids": [270, 35, 22, 21, 46, 188, 62, 911, 25, 165]
    },
    {
        "titulo": "Ranking Balón de Oro 2015",
        "descripcion": "Los 10 mejores jugadores según el Balón de Oro 2015",
        "jugadores_ids": [1, 2, 3, 20, 4, 201, 15, 928, 10, 305]
    },
    {
        "titulo": "Jugadores con más partidos en Barcelona (Champions)",
        "descripcion": "Los jugadores con más apariciones en Barcelona en la Champions League",
        "jugadores_ids": [11, 1, 10, 12, 16, 44, 176, 175, 365, 343]
    },
    {
        "titulo": "Jugadores con más partidos en Man Utd (Champions)",
        "descripcion": "Los jugadores con más apariciones en Manchester United en la Champions League",
        "jugadores_ids": [929, 39, 930, 226, 37, 143, 931, 932, 933, 171]
    },
    {
        "titulo": "Jugadores con más partidos en Real Madrid (Champions)",
        "descripcion": "Los jugadores con más apariciones en Real Madrid en la Champions League",
        "jugadores_ids": [76, 8, 5, 153, 265, 9, 78, 50, 2, 935]
    },
    {
        "titulo": "Jugadores con más partidos en Liverpool (Champions)",
        "descripcion": "Los jugadores con más apariciones en Liverpool en la Champions League",
        "jugadores_ids": [182, 26, 36, 117, 115, 185, 66, 360, 65, 192]
    },
    {
        "titulo": "Jugadores con más goles en Bayern (Champions)",
        "descripcion": "Los jugadores con más goles en Bayern de Múnich en la Champions League",
        "jugadores_ids": [20, 201, 24, 67, 936, 937, 938, 23, 939, 114]
    },
    {
        "titulo": "Ranking Balón de Oro 2017",
        "descripcion": "Los 10 mejores jugadores según el Balón de Oro 2017",
        "jugadores_ids": [2, 1, 3, 35, 8, 265, 14, 93, 20, 67]
    },
    {
        "titulo": "Transferencias más caras de la historia",
        "descripcion": "Los 10 fichajes más caros en la historia del fútbol",
        "jugadores_ids": [3, 14, 81, 376, 103, 765, 122, 371, 70, 928]
    },
    {
        "titulo": "Jugadores con más goles en Arsenal (Champions)",
        "descripcion": "Los jugadores con más goles en Arsenal en la Champions League",
        "jugadores_ids": [22, 330, 940, 45, 941, 259, 96, 111, 305, 942]
    },
    {
        "titulo": "Jugadores con más partidos en Chelsea (Champions)",
        "descripcion": "Los jugadores con más apariciones en Chelsea en la Champions League",
        "jugadores_ids": [142, 141, 56, 911, 263, 40, 943, 228, 944, 213]
    },
    {
        "titulo": "Jugadores con más goles en Juventus (Champions)",
        "descripcion": "Los jugadores con más goles en Juventus en la Champions League",
        "jugadores_ids": [79, 134, 130, 210, 91, 2, 71, 52, 267, 544]
    }
]

class JuegoTop10:
    def __init__(self):
        self.elegir_top_aleatorio()
        self.respuestas_correctas = set()
        self.input_texto = ""
        self.mensaje = ""
        self.mensaje_timer = 0
        self.mensaje_tipo = "info"
        self.puntos = 0
        self.juego_terminado = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.juego_rendirse = False
        
    def elegir_top_aleatorio(self):
        """Elige un top aleatorio de los disponibles"""
        self.top_actual = random.choice(TOPS_DISPONIBLES)
        self.jugadores_top = self.cargar_jugadores_top()
    
    def cargar_jugadores_top(self):
        """Carga los jugadores del top actual desde la base de datos"""
        jugadores = []
        for player_id in self.top_actual["jugadores_ids"]:
            jugador = next((j for j in jugadores_db if j["id"] == player_id), None)
            if jugador:
                jugadores.append(jugador)
        return jugadores
    
    def reiniciar_con_nuevo_top(self):
        """Reinicia el juego con un nuevo top aleatorio"""
        self.elegir_top_aleatorio()
        self.respuestas_correctas = set()
        self.input_texto = ""
        self.mensaje = ""
        self.mensaje_timer = 0
        self.puntos = 0
        self.juego_terminado = False
        self.juego_rendirse = False  
    
    def normalizar_texto(self, texto):
        """Normaliza texto para comparación (sin acentos, minúsculas)"""
        texto = texto.lower().strip()
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ü': 'u', 'à': 'a', 'è': 'e', 'ì': 'i', "ć": 'c',
            'ò': 'o', 'ù': 'u', 'ã': 'a', 'õ': 'o', 'â': 'a',
            'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u', 'ç': 'c',
            'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'č': 'c',
            "ž": 'z', "ě": 'e'
        }
        for acento, sin_acento in reemplazos.items():
            texto = texto.replace(acento, sin_acento)
        return texto
    
    def verificar_respuesta(self, input_jugador):
        """Verifica si el input coincide con algún jugador no adivinado"""
        if not input_jugador.strip():
            return None
        
        # Requerir mínimo 3 letras
        if len(input_jugador.strip()) < 3:
            return None
            
        input_normalizado = self.normalizar_texto(input_jugador)
        
        for i, jugador in enumerate(self.jugadores_top):
            if i in self.respuestas_correctas:
                continue
            
            nombre_normalizado = self.normalizar_texto(jugador["nombre"])
            if input_normalizado in nombre_normalizado or nombre_normalizado.startswith(input_normalizado):
                return i
            
            apellido = nombre_normalizado.split()[-1]
            if input_normalizado == apellido or apellido.startswith(input_normalizado):
                return i
            
            if "apodo" in jugador:
                apodo_normalizado = self.normalizar_texto(jugador["apodo"])
                if input_normalizado in apodo_normalizado or apodo_normalizado.startswith(input_normalizado):
                    return i
        
        return None
    
    def rendirse(self):
        """El jugador se rinde y se revelan todas las respuestas"""
        # Marcar todas las respuestas como correctas para que se muestren
        for i in range(len(self.jugadores_top)):
            self.respuestas_correctas.add(i)
        self.juego_rendirse = True
        self.mensaje = f"Te rendiste. Puntos finales: {self.puntos}/{len(self.jugadores_top) * 10}"
        self.mensaje_tipo = "info"
    
    def procesar_input(self):
        """Procesa el texto ingresado por el usuario"""
        if not self.input_texto.strip():
            return
        
        # Verificar si tiene al menos 3 letras
        if len(self.input_texto.strip()) < 3:
            self.mensaje = "Debes escribir al menos 3 letras"
            self.mensaje_tipo = "incorrecto"
            self.mensaje_timer = 60
            self.input_texto = ""
            return
        
        resultado = self.verificar_respuesta(self.input_texto)
        
        if resultado is not None:
            self.respuestas_correctas.add(resultado)
            self.puntos += 10
            jugador = self.jugadores_top[resultado]
            nombre_mostrar = jugador.get("apodo", jugador["nombre"])
            self.mensaje = f"¡Correcto! {nombre_mostrar}"
            self.mensaje_tipo = "correcto"
            self.mensaje_timer = 120
            
            if len(self.respuestas_correctas) == len(self.jugadores_top):
                self.juego_terminado = True
                self.mensaje = f"¡Felicitaciones! Completaste el Top 10 con {self.puntos} puntos"
                self.mensaje_tipo = "correcto"
        else:
            self.mensaje = f"'{self.input_texto}' no está en este Top 10"
            self.mensaje_tipo = "incorrecto"
            self.mensaje_timer = 90
        
        self.input_texto = ""
    
    def actualizar(self):
        """Actualiza el estado del juego"""
        if self.mensaje_timer > 0:
            self.mensaje_timer -= 1
            if self.mensaje_timer == 0:
                self.mensaje = ""
        
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        pantalla.fill(BLANCO)
        
        # Título del Top
        titulo_surf = fuente_titulo.render(self.top_actual["titulo"], True, NEGRO)
        titulo_rect = titulo_surf.get_rect(center=(ANCHO // 2.3, 40))
        pantalla.blit(titulo_surf, titulo_rect)
        
        # Descripción
        desc_surf = fuente_pequeña.render(self.top_actual["descripcion"], True, GRIS_OSCURO)
        desc_rect = desc_surf.get_rect(center=(ANCHO // 2.3, 80))
        pantalla.blit(desc_surf, desc_rect)
        
        # Botón de reiniciar (esquina superior derecha)
        boton_reiniciar_rect = pygame.Rect(ANCHO - 180, 20, 160, 50)
        pygame.draw.rect(pantalla, NARANJA, boton_reiniciar_rect, border_radius=8)
        pygame.draw.rect(pantalla, GRIS_OSCURO, boton_reiniciar_rect, 3, border_radius=8)
        
        texto_reiniciar = fuente_texto.render("🔄 Nuevo Top", True, BLANCO)
        texto_rect = texto_reiniciar.get_rect(center=boton_reiniciar_rect.center)
        pantalla.blit(texto_reiniciar, texto_rect)
        
        # Botón de rendirse (debajo del botón de reiniciar)
        if not self.juego_terminado:
            boton_rendirse_rect = pygame.Rect(ANCHO - 180, 80, 160, 50)
            pygame.draw.rect(pantalla, ROJO, boton_rendirse_rect, border_radius=8)
            pygame.draw.rect(pantalla, GRIS_OSCURO, boton_rendirse_rect, 3, border_radius=8)
            
            texto_rendirse = fuente_texto.render("🏳️ Rendirse", True, BLANCO)
            texto_rendirse_rect = texto_rendirse.get_rect(center=boton_rendirse_rect.center)
            pantalla.blit(texto_rendirse, texto_rendirse_rect)
        
        # Puntos
        puntos_surf = fuente_texto.render(f"Puntos: {self.puntos}/{len(self.jugadores_top) * 10}", True, VERDE)
        pantalla.blit(puntos_surf, (20, 100))
        
        # Progreso
        progreso_surf = fuente_texto.render(f"Adivinados: {len(self.respuestas_correctas)}/{len(self.jugadores_top)}", True, AZUL)
        pantalla.blit(progreso_surf, (ANCHO - 360, 100))
        
        # Lista de jugadores
        y_offset = 150
        for i, jugador in enumerate(self.jugadores_top):
            color_fondo = GRIS if i % 2 == 0 else (220, 220, 220)
            pygame.draw.rect(pantalla, color_fondo, (50, y_offset, ANCHO - 100, 55))
            
            pos_surf = fuente_texto.render(f"#{i+1}", True, NEGRO)
            pantalla.blit(pos_surf, (70, y_offset + 15))
            
            # Bandera
            nacionalidad_jugador = jugador['nacionalidad']
            if isinstance(nacionalidad_jugador, list):
                nacionalidad_jugador = nacionalidad_jugador[0] if len(nacionalidad_jugador) > 0 else ""

            if nacionalidad_jugador in banderas:
                pantalla.blit(banderas[nacionalidad_jugador], (140, y_offset + 12))
            
            if i in self.respuestas_correctas:
                nombre_mostrar = jugador.get("apodo", jugador["nombre"])
                nombre_surf = fuente_texto.render(nombre_mostrar, True, VERDE_CLARO)
                pantalla.blit(nombre_surf, (210, y_offset + 15))
            else:
                interrogacion = fuente_texto.render("???", True, GRIS_OSCURO)
                pantalla.blit(interrogacion, (210, y_offset + 15))
            
            y_offset += 60
        
        # Campo de entrada
        input_y = ALTO - 60
        pygame.draw.rect(pantalla, GRIS_OSCURO, (50, input_y, ANCHO - 100, 50), border_radius=10)
        pygame.draw.rect(pantalla, BLANCO, (55, input_y + 5, ANCHO - 110, 40), border_radius=8)
        
        input_surf = fuente_texto.render(self.input_texto, True, NEGRO)
        pantalla.blit(input_surf, (65, input_y + 13))
        
        if self.cursor_visible and not self.juego_terminado:
            cursor_x = 65 + input_surf.get_width() + 2
            pygame.draw.line(pantalla, NEGRO, (cursor_x, input_y + 10), (cursor_x, input_y + 40), 2)
        
        if not self.input_texto:
            placeholder = fuente_pequeña.render("Escribe el nombre del jugador y presiona ENTER...", True, GRIS)
            pantalla.blit(placeholder, (65, input_y + 15))
        
        # Mensaje de feedback
        if self.mensaje:
            if self.mensaje_tipo == "correcto":
                color_mensaje = VERDE
            elif self.mensaje_tipo == "incorrecto":
                color_mensaje = ROJO
            else:
                color_mensaje = AZUL
            
            mensaje_surf = fuente_texto.render(self.mensaje, True, color_mensaje)
            mensaje_rect = mensaje_surf.get_rect(center=(ANCHO // 2, ALTO - 60))
            pantalla.blit(mensaje_surf, mensaje_rect)
        
        # Mensaje de juego completado
        if self.juego_terminado:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(BLANCO)
            pantalla.blit(overlay, (0, 0))
            
            victoria_surf = fuente_titulo.render("¡COMPLETADO!", True, VERDE)
            victoria_rect = victoria_surf.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(victoria_surf, victoria_rect)
            
            puntos_final = fuente_subtitulo.render(f"Puntos totales: {self.puntos}", True, NEGRO)
            puntos_rect = puntos_final.get_rect(center=(ANCHO // 2, ALTO // 2 + 10))
            pantalla.blit(puntos_final, puntos_rect)
            
            reinicio = fuente_texto.render("Presiona ESPACIO o click en 'Nuevo Top' para continuar", True, GRIS_OSCURO)
            reinicio_rect = reinicio.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            pantalla.blit(reinicio, reinicio_rect)

        if self.juego_rendirse:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(BLANCO)
            pantalla.blit(overlay, (0, 0))
            
            victoria_surf = fuente_titulo.render("¡RENDIDO!", True, ROJO)
            victoria_rect = victoria_surf.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(victoria_surf, victoria_rect)
            
            puntos_final = fuente_subtitulo.render(f"Puntos totales: {self.puntos}", True, NEGRO)
            puntos_rect = puntos_final.get_rect(center=(ANCHO // 2, ALTO // 2 + 10))
            pantalla.blit(puntos_final, puntos_rect)
            
            reinicio = fuente_texto.render("Presiona ESPACIO o click en 'Nuevo Top' para continuar", True, GRIS_OSCURO)
            reinicio_rect = reinicio.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            pantalla.blit(reinicio, reinicio_rect)
        
        pygame.display.flip()

def main():
    if not jugadores_db:
        print("No se pudieron cargar los jugadores. Verifica que basededatos.json existe.")
        return
    
    reloj = pygame.time.Clock()
    juego = JuegoTop10()
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                if juego.juego_terminado or juego.juego_rendirse:
                    if evento.key == pygame.K_SPACE:
                        juego.reiniciar_con_nuevo_top()
                else:
                    if evento.key == pygame.K_RETURN:
                        juego.procesar_input()
                    elif evento.key == pygame.K_BACKSPACE:
                        juego.input_texto = juego.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    elif evento.unicode.isprintable():
                        if len(juego.input_texto) < 30:
                            juego.input_texto += evento.unicode
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Botón de reiniciar
                if ANCHO - 180 <= x <= ANCHO - 20 and 20 <= y <= 70:
                    juego.reiniciar_con_nuevo_top()
                # Botón de rendirse
                elif ANCHO - 180 <= x <= ANCHO - 20 and 80 <= y <= 130:
                    if not juego.juego_terminado:
                        juego.rendirse()
        
        juego.actualizar()
        juego.dibujar()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()