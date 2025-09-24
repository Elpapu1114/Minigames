import pygame
import sys
import time

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60
META = 650

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 100, 100)
AZUL = (100, 150, 255)
VERDE = (100, 255, 100)
AMARILLO = (255, 255, 100)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)

# Variables globales
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Carrera de Teclas")
reloj = pygame.time.Clock()
fuente_grande = pygame.font.Font(None, 48)
fuente_mediana = pygame.font.Font(None, 32)
fuente_pequeña = pygame.font.Font(None, 24)

# Estado del juego
estado_juego = "menu"  # "menu", "juego", "ganador"
posicion_j1 = 50
posicion_j2 = 50
ganador = None

def dibujar_menu():
    """Dibuja el menú principal"""
    pantalla.fill(AZUL)
    
    # Título
    titulo = fuente_grande.render("CARRERA DE TECLAS", True, BLANCO)
    rect_titulo = titulo.get_rect(center=(ANCHO//2, 150))
    pantalla.blit(titulo, rect_titulo)
    
    # Subtítulo
    subtitulo = fuente_mediana.render("¡Presiona las teclas más rápido para ganar!", True, BLANCO)
    rect_subtitulo = subtitulo.get_rect(center=(ANCHO//2, 200))
    pantalla.blit(subtitulo, rect_subtitulo)
    
    # Instrucciones
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
    
    # Botón de inicio (visual)
    pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 450, 200, 50))
    texto_boton = fuente_mediana.render("INICIAR", True, NEGRO)
    rect_boton = texto_boton.get_rect(center=(ANCHO//2, 475))
    pantalla.blit(texto_boton, rect_boton)

def dibujar_pista():
    """Dibuja la pista de carrera"""
    # Fondo
    pantalla.fill(VERDE)
    
    # Pista Jugador 1 (arriba)
    pygame.draw.rect(pantalla, GRIS_CLARO, (50, 150, META, 80))
    pygame.draw.rect(pantalla, NEGRO, (50, 150, META, 80), 3)
    
    # Pista Jugador 2 (abajo)
    pygame.draw.rect(pantalla, GRIS_CLARO, (50, 350, META, 80))
    pygame.draw.rect(pantalla, NEGRO, (50, 350, META, 80), 3)
    
    # Línea de meta
    pygame.draw.line(pantalla, AMARILLO, (META, 100), (META, 500), 5)
    
    # Etiquetas de jugadores
    texto_j1 = fuente_mediana.render("Jugador 1 - Tecla 'A'", True, ROJO)
    pantalla.blit(texto_j1, (50, 120))
    
    texto_j2 = fuente_mediana.render("Jugador 2 - Tecla 'L'", True, AZUL)
    pantalla.blit(texto_j2, (50, 320))
    
    # META
    texto_meta = fuente_pequeña.render("META", True, NEGRO)
    pantalla.blit(texto_meta, (META + 10, 300))

def dibujar_corredores():
    """Dibuja los corredores en sus posiciones actuales"""
    # Corredor 1 (círculo rojo)
    pygame.draw.circle(pantalla, ROJO, (int(posicion_j1), 190), 25)
    pygame.draw.circle(pantalla, NEGRO, (int(posicion_j1), 190), 25, 3)
    
    # Corredor 2 (círculo azul)
    pygame.draw.circle(pantalla, AZUL, (int(posicion_j2), 390), 25)
    pygame.draw.circle(pantalla, NEGRO, (int(posicion_j2), 390), 25, 3)

def dibujar_progreso():
    """Dibuja las barras de progreso"""
    # Barra de progreso Jugador 1
    progreso_j1 = (posicion_j1 - 50) / (META - 50)
    ancho_barra_j1 = int(200 * progreso_j1)
    pygame.draw.rect(pantalla, GRIS, (50, 50, 200, 20))
    pygame.draw.rect(pantalla, ROJO, (50, 50, ancho_barra_j1, 20))
    pygame.draw.rect(pantalla, NEGRO, (50, 50, 200, 20), 2)
    
    # Barra de progreso Jugador 2
    progreso_j2 = (posicion_j2 - 50) / (META - 50)
    ancho_barra_j2 = int(200 * progreso_j2)
    pygame.draw.rect(pantalla, GRIS, (500, 50, 200, 20))
    pygame.draw.rect(pantalla, AZUL, (500, 50, ancho_barra_j2, 20))
    pygame.draw.rect(pantalla, NEGRO, (500, 50, 200, 20), 2)
    
    # Etiquetas de progreso
    texto_prog1 = fuente_pequeña.render(f"J1: {int(progreso_j1*100)}%", True, NEGRO)
    pantalla.blit(texto_prog1, (50, 25))
    
    texto_prog2 = fuente_pequeña.render(f"J2: {int(progreso_j2*100)}%", True, NEGRO)
    pantalla.blit(texto_prog2, (500, 25))

def dibujar_juego():
    """Dibuja toda la pantalla del juego"""
    dibujar_pista()
    dibujar_corredores()
    dibujar_progreso()
    
    # Instrucciones durante el juego
    texto_inst = fuente_pequeña.render("¡Presiona tu tecla repetidamente! ESC para volver al menú", True, NEGRO)
    rect_inst = texto_inst.get_rect(center=(ANCHO//2, ALTO - 30))
    pantalla.blit(texto_inst, rect_inst)

def dibujar_pantalla_ganador():
    """Dibuja la pantalla del ganador"""
    pantalla.fill(VERDE)
    
    # Determinar color del ganador
    color_ganador = ROJO if ganador == 1 else AZUL
    
    # Mensaje principal
    texto_ganador = fuente_grande.render(f"¡JUGADOR {ganador} GANA!", True, color_ganador)
    rect_ganador = texto_ganador.get_rect(center=(ANCHO//2, 200))
    pantalla.blit(texto_ganador, rect_ganador)
    
    # Felicitaciones
    felicitacion = fuente_mediana.render("¡Felicitaciones por tu victoria!", True, BLANCO)
    rect_felicitacion = felicitacion.get_rect(center=(ANCHO//2, 280))
    pantalla.blit(felicitacion, rect_felicitacion)
    
    # Opciones
    opciones = [
        "Presiona ESPACIO para jugar de nuevo",
        "Presiona ESC para volver al menú"
    ]
    
    for i, opcion in enumerate(opciones):
        texto_opcion = fuente_pequeña.render(opcion, True, BLANCO)
        rect_opcion = texto_opcion.get_rect(center=(ANCHO//2, 350 + i*30))
        pantalla.blit(texto_opcion, rect_opcion)
    
    # Dibujar trofeo simple
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
            # En el menú
            if estado_juego == "menu":
                if evento.key == pygame.K_SPACE:
                    iniciar_juego()
            
            # En la pantalla de ganador
            elif estado_juego == "ganador":
                if evento.key == pygame.K_SPACE:
                    iniciar_juego()
                elif evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
            
            # Durante el juego
            elif estado_juego == "juego":
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
                
                # Movimiento de jugadores
                elif evento.key == pygame.K_a:
                    mover_jugador(1)
                elif evento.key == pygame.K_l:
                    mover_jugador(2)

def iniciar_juego():
    """Inicia una nueva partida"""
    global estado_juego, posicion_j1, posicion_j2, ganador
    estado_juego = "juego"
    posicion_j1 = 75
    posicion_j2 = 75
    ganador = None

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
    pass

def ejecutar_juego():
    """Bucle principal del juego"""
    ejecutando = True
    
    while ejecutando:
        # Manejar eventos
        manejar_eventos()
        
        # Actualizar juego
        actualizar_juego()
        
        # Dibujar según el estado actual
        if estado_juego == "menu":
            dibujar_menu()
        elif estado_juego == "juego":
            dibujar_juego()
        elif estado_juego == "ganador":
            dibujar_pantalla_ganador()
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()

# Ejecutar el juego si se ejecuta directamente
if __name__ == "__main__":
    ejecutar_juego()