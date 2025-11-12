import pygame
import sys
import time
import os

pygame.init()

from display_config import init_display
ANCHO = 800
ALTO = 600
FPS = 60
META = 650
# Inicializar pantalla según game_settings.json
pantalla, ANCHO, ALTO = init_display(default_w=ANCHO, default_h=ALTO, title="Carrera de Teclas")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 100, 100)
AZUL = (100, 150, 255)
VERDE = (100, 255, 100)
AMARILLO = (255, 255, 100)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Carrera de Teclas")
reloj = pygame.time.Clock()
fuente_grande = pygame.font.Font(None, 48)
fuente_mediana = pygame.font.Font(None, 32)
fuente_pequeña = pygame.font.Font(None, 24)

try:
    auto_rojo = pygame.image.load(os.path.join("image", "carreraautorojo.png"))
    auto_azul = pygame.image.load(os.path.join("image", "carreraautoazul.png"))
    auto_rojo = pygame.transform.scale(auto_rojo, (50, 50))
    auto_azul = pygame.transform.scale(auto_azul, (50, 50))
except:
    auto_rojo = None
    auto_azul = None
    print("Advertencia: No se pudieron cargar las imágenes de los autos")

try:
    menu_image = pygame.image.load(os.path.join("image", "menu_fast_fingers.png"))
    victoria_j1_image = pygame.image.load(os.path.join("image", "jugador_1_victoria_fast_fingers.png"))
    victoria_j2_image = pygame.image.load(os.path.join("image", "jugador_2_victoria_fast_fingers.png"))
    usar_imagenes = True
except:
    menu_image = None
    victoria_j1_image = None
    victoria_j2_image = None
    usar_imagenes = False
    print("Advertencia: No se pudieron cargar las imágenes del menú/victoria")

estado_juego = "menu" 
posicion_j1 = 50
posicion_j2 = 50
ganador = None
tiempo_inicio_cuenta = 0

def dibujar_menu():
    """Dibuja el menú principal"""
    if usar_imagenes and menu_image:
        scaled_image = pygame.transform.scale(menu_image, (ANCHO, ALTO))
        pantalla.blit(scaled_image, (0, 0))
    else:
        pantalla.fill(AZUL)

        titulo = fuente_grande.render("CARRERA DE TECLAS", True, BLANCO)
        rect_titulo = titulo.get_rect(center=(ANCHO//2, 150))
        pantalla.blit(titulo, rect_titulo)

        subtitulo = fuente_mediana.render("¡Presiona las teclas más rápido para ganar!", True, BLANCO)
        rect_subtitulo = subtitulo.get_rect(center=(ANCHO//2, 200))
        pantalla.blit(subtitulo, rect_subtitulo)

        instrucciones = [
            "Jugador 1: Tecla 'A'",
            "Jugador 2: Tecla 'L'",
            "",
            "Presiona ESPACIO para comenzar"
        ]
        
        y_inicio = 280
        for i, linea in enumerate(instrucciones):
            if linea:
                if "Jugador 1" in linea:
                    color = ROJO
                elif "Jugador 2" in linea:
                    color = AZUL
                else:
                    color = BLANCO
                
                texto = fuente_pequeña.render(linea, True, color)
                rect_texto = texto.get_rect(center=(ANCHO//2, y_inicio + i*30))
                pantalla.blit(texto, rect_texto)

        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 450, 200, 50))
        texto_boton = fuente_mediana.render("INICIAR", True, NEGRO)
        rect_boton = texto_boton.get_rect(center=(ANCHO//2, 475))
        pantalla.blit(texto_boton, rect_boton)

def dibujar_pista():
    """Dibuja la pista de carrera"""
    pantalla.fill(VERDE)
    
    pygame.draw.rect(pantalla, GRIS_CLARO, (50, 150, META, 80))
    pygame.draw.rect(pantalla, NEGRO, (50, 150, META, 80), 3)

    pygame.draw.rect(pantalla, GRIS_CLARO, (50, 350, META, 80))
    pygame.draw.rect(pantalla, NEGRO, (50, 350, META, 80), 3)

    pygame.draw.line(pantalla, AMARILLO, (META, 100), (META, 500), 5)

    texto_j1 = fuente_mediana.render("Jugador 1 - Tecla 'A'", True, ROJO)
    pantalla.blit(texto_j1, (50, 120))
    
    texto_j2 = fuente_mediana.render("Jugador 2 - Tecla 'L'", True, AZUL)
    pantalla.blit(texto_j2, (50, 320))

    texto_meta = fuente_pequeña.render("META", True, NEGRO)
    pantalla.blit(texto_meta, (META + 10, 300))

def dibujar_corredores():
    """Dibuja los corredores en sus posiciones actuales"""
    if auto_rojo:
        pantalla.blit(auto_rojo, (int(posicion_j1) - 25, 165))
    else:
        pygame.draw.circle(pantalla, ROJO, (int(posicion_j1), 190), 25)
        pygame.draw.circle(pantalla, NEGRO, (int(posicion_j1), 190), 25, 3)

    if auto_azul:
        pantalla.blit(auto_azul, (int(posicion_j2) - 25, 365))
    else:
        pygame.draw.circle(pantalla, AZUL, (int(posicion_j2), 390), 25)
        pygame.draw.circle(pantalla, NEGRO, (int(posicion_j2), 390), 25, 3)

def dibujar_progreso():
    """Dibuja las barras de progreso"""
    progreso_j1 = (posicion_j1 - 50) / (META - 50)
    ancho_barra_j1 = int(200 * progreso_j1)
    pygame.draw.rect(pantalla, GRIS, (50, 50, 200, 20))
    pygame.draw.rect(pantalla, ROJO, (50, 50, ancho_barra_j1, 20))
    pygame.draw.rect(pantalla, NEGRO, (50, 50, 200, 20), 2)
    
    progreso_j2 = (posicion_j2 - 50) / (META - 50)
    ancho_barra_j2 = int(200 * progreso_j2)
    pygame.draw.rect(pantalla, GRIS, (500, 50, 200, 20))
    pygame.draw.rect(pantalla, AZUL, (500, 50, ancho_barra_j2, 20))
    pygame.draw.rect(pantalla, NEGRO, (500, 50, 200, 20), 2)

    texto_prog1 = fuente_pequeña.render(f"J1: {int(progreso_j1*100)}%", True, NEGRO)
    pantalla.blit(texto_prog1, (50, 25))
    
    texto_prog2 = fuente_pequeña.render(f"J2: {int(progreso_j2*100)}%", True, NEGRO)
    pantalla.blit(texto_prog2, (500, 25))

def dibujar_juego():
    """Dibuja toda la pantalla del juego"""
    dibujar_pista()
    dibujar_corredores()
    dibujar_progreso()
    
    texto_inst = fuente_pequeña.render("¡Presiona tu tecla repetidamente! ESC para volver al menú", True, NEGRO)
    rect_inst = texto_inst.get_rect(center=(ANCHO//2, ALTO - 30))
    pantalla.blit(texto_inst, rect_inst)

def dibujar_cuenta_regresiva():
    """Dibuja la pantalla de cuenta regresiva"""
    dibujar_pista()
    dibujar_corredores()
    dibujar_progreso()

    tiempo_transcurrido = time.time() - tiempo_inicio_cuenta
    tiempo_restante = 3 - int(tiempo_transcurrido)
    
    if tiempo_restante > 0:
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        texto_cuenta = pygame.font.Font(None, 150).render(str(tiempo_restante), True, AMARILLO)
        rect_cuenta = texto_cuenta.get_rect(center=(ANCHO//2, ALTO//2))
        pantalla.blit(texto_cuenta, rect_cuenta)
        
        texto_preparate = fuente_mediana.render("¡PREPÁRATE!", True, BLANCO)
        rect_preparate = texto_preparate.get_rect(center=(ANCHO//2, ALTO//2 + 80))
        pantalla.blit(texto_preparate, rect_preparate)

def dibujar_pantalla_ganador():
    """Dibuja la pantalla del ganador"""
    if usar_imagenes:
        if ganador == 1 and victoria_j1_image:
            scaled_image = pygame.transform.scale(victoria_j1_image, (ANCHO, ALTO))
            pantalla.blit(scaled_image, (0, 0))
            return
        elif ganador == 2 and victoria_j2_image:
            scaled_image = pygame.transform.scale(victoria_j2_image, (ANCHO, ALTO))
            pantalla.blit(scaled_image, (0, 0))
            return
    
    pantalla.fill(VERDE)

    color_ganador = ROJO if ganador == 1 else AZUL
    
    texto_ganador = fuente_grande.render(f"¡JUGADOR {ganador} GANA!", True, color_ganador)
    rect_ganador = texto_ganador.get_rect(center=(ANCHO//2, 200))
    pantalla.blit(texto_ganador, rect_ganador)

    felicitacion = fuente_mediana.render("¡Felicitaciones por tu victoria!", True, BLANCO)
    rect_felicitacion = felicitacion.get_rect(center=(ANCHO//2, 280))
    pantalla.blit(felicitacion, rect_felicitacion)

    opciones = [
        "Presiona ESPACIO para jugar de nuevo",
        "Presiona ESC para volver al menú"
    ]
    
    for i, opcion in enumerate(opciones):
        texto_opcion = fuente_pequeña.render(opcion, True, BLANCO)
        rect_opcion = texto_opcion.get_rect(center=(ANCHO//2, 350 + i*30))
        pantalla.blit(texto_opcion, rect_opcion)

    pygame.draw.ellipse(pantalla, AMARILLO, (ANCHO//2 - 30, 100, 60, 40))
    pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 10, 140, 20, 30))
    pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 20, 170, 40, 10))

def manejar_eventos():
    """Maneja todos los eventos del juego"""
    global estado_juego, posicion_j1, posicion_j2, ganador
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if estado_juego == "menu":
                if evento.key == pygame.K_SPACE:
                    iniciar_cuenta_regresiva()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif estado_juego == "ganador":
                if evento.key == pygame.K_SPACE:
                    iniciar_cuenta_regresiva()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif estado_juego == "juego":
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"

                elif evento.key == pygame.K_a:
                    mover_jugador(1)
                elif evento.key == pygame.K_l:
                    mover_jugador(2)

def iniciar_cuenta_regresiva():
    """Inicia la cuenta regresiva antes del juego"""
    global estado_juego, posicion_j1, posicion_j2, ganador, tiempo_inicio_cuenta
    estado_juego = "cuenta_regresiva"
    posicion_j1 = 75
    posicion_j2 = 75
    ganador = None
    tiempo_inicio_cuenta = time.time()

def iniciar_juego():
    """Inicia una nueva partida"""
    global estado_juego
    estado_juego = "juego"

def mover_jugador(jugador):
    """Mueve el jugador especificado hacia adelante"""
    global posicion_j1, posicion_j2, estado_juego, ganador
    
    velocidad = 8
    
    if jugador == 1:
        posicion_j1 += velocidad
        if posicion_j1 >= META:
            ganador = 1
            estado_juego = "ganador"
    
    elif jugador == 2:
        posicion_j2 += velocidad
        if posicion_j2 >= META:
            ganador = 2
            estado_juego = "ganador"

def actualizar_juego():
    """Actualiza la lógica del juego"""
    global estado_juego

    if estado_juego == "cuenta_regresiva":
        tiempo_transcurrido = time.time() - tiempo_inicio_cuenta
        if tiempo_transcurrido >= 3:
            iniciar_juego()

def ejecutar_juego():
    """Bucle principal del juego"""
    ejecutando = True
    
    while ejecutando:
        manejar_eventos()

        actualizar_juego()

        if estado_juego == "menu":
            dibujar_menu()
        elif estado_juego == "cuenta_regresiva":
            dibujar_cuenta_regresiva()
        elif estado_juego == "juego":
            dibujar_juego()
        elif estado_juego == "ganador":
            dibujar_pantalla_ganador()

        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    ejecutar_juego()