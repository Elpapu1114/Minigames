import pygame
import random
import time

# Inicializar pygame
pygame.init()


# Constantes
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROJO_OSCURO = (150, 0, 0)
VERDE_OSCURO = (0, 150, 0)
AZUL_OSCURO = (0, 0, 150)
AMARILLO_OSCURO = (150, 150, 0)
GRIS = (128, 128, 128)

# Estados del juego
MENU = 0
JUGANDO = 1
MOSTRANDO_SECUENCIA = 2
ESPERANDO_JUGADOR = 3
GAME_OVER = 4

def crear_sonidos():
    """Crear sonidos sintéticos para cada botón"""
    sonidos = {}
    try:
        # Crear tonos simples para cada color
        duracion = 0.3
        sample_rate = 22050
        
        # Generar tonos
        for i, nota in enumerate([440, 523, 659, 784]):  # Do, Mi, Sol, Si
            frames = int(duracion * sample_rate)
            arr = []
            for x in range(frames):
                wave = 4096 * (x / sample_rate * nota * 2 * 3.14159) % (2 * 3.14159)
                arr.append([int(2000 * (wave - 3.14159)), int(2000 * (wave - 3.14159))])
            
            sound = pygame.sndarray.make_sound(arr)
            sonidos[i] = sound
    except:
        # Si hay error con los sonidos, crear diccionario vacío
        sonidos = {0: None, 1: None, 2: None, 3: None}
    
    return sonidos

def inicializar_juego():
    """Inicializar variables del juego"""
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simón Dice")
    reloj = pygame.time.Clock()
    
    # Variables del juego
    estado = MENU
    secuencia = []
    secuencia_jugador = []
    indice_secuencia = 0
    indice_jugador = 0
    nivel = 1
    puntuacion = 0
    tiempo_ultimo_boton = 0
    boton_presionado = -1
    
    # Sonidos
    sonidos = crear_sonidos()
    
    # Definir botones (x, y, ancho, alto, color_normal, color_presionado, sonido_index)
    botones = [
        (150, 150, 200, 200, ROJO, ROJO_OSCURO, 0),      # Rojo
        (450, 150, 200, 200, VERDE, VERDE_OSCURO, 1),    # Verde
        (150, 350, 200, 200, AZUL, AZUL_OSCURO, 2),      # Azul
        (450, 350, 200, 200, AMARILLO, AMARILLO_OSCURO, 3) # Amarillo
    ]
    
    return (pantalla, reloj, estado, secuencia, secuencia_jugador, indice_secuencia, 
            indice_jugador, nivel, puntuacion, tiempo_ultimo_boton, boton_presionado, 
            sonidos, botones)

def dibujar_boton(pantalla, boton, presionado=False, fuente=None):
    """Dibujar un botón en la pantalla"""
    x, y, ancho, alto, color_normal, color_presionado, _ = boton
    color = color_presionado if presionado else color_normal
    
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto), 3)
    
    # Agregar número al botón
    if fuente:
        numero = str(boton[6] + 1)
        texto = fuente.render(numero, True, NEGRO)
        texto_rect = texto.get_rect(center=(x + ancho//2, y + alto//2))
        pantalla.blit(texto, texto_rect)

def dibujar_pantalla(pantalla, estado, botones, nivel, puntuacion, boton_presionado):
    """Dibujar toda la pantalla según el estado actual"""
    pantalla.fill(BLANCO)
    fuente_grande = pygame.font.Font(None, 48)
    fuente_mediana = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    if estado == MENU:
        titulo = fuente_grande.render("SIMÓN DICE", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(ANCHO//2, 150))
        pantalla.blit(titulo, titulo_rect)
        
        instruccion = fuente_mediana.render("Presiona ESPACIO para comenzar", True, NEGRO)
        instruccion_rect = instruccion.get_rect(center=(ANCHO//2, 300))
        pantalla.blit(instruccion, instruccion_rect)
        
        reglas = [
            "Memoriza la secuencia de colores",
            "Repite la secuencia haciendo clic en los botones",
            "La secuencia se hace más larga cada nivel",
            "¡Intenta llegar lo más lejos posible!"
        ]
        
        for i, regla in enumerate(reglas):
            texto = fuente_pequena.render(regla, True, GRIS)
            texto_rect = texto.get_rect(center=(ANCHO//2, 380 + i*30))
            pantalla.blit(texto, texto_rect)
    
    elif estado == GAME_OVER:
        game_over = fuente_grande.render("GAME OVER", True, NEGRO)
        game_over_rect = game_over.get_rect(center=(ANCHO//2, 200))
        pantalla.blit(game_over, game_over_rect)
        
        puntuacion_final = fuente_mediana.render(f"Puntuación: {puntuacion}", True, NEGRO)
        puntuacion_rect = puntuacion_final.get_rect(center=(ANCHO//2, 280))
        pantalla.blit(puntuacion_final, puntuacion_rect)
        
        reiniciar = fuente_mediana.render("Presiona ESPACIO para jugar de nuevo", True, NEGRO)
        reiniciar_rect = reiniciar.get_rect(center=(ANCHO//2, 350))
        pantalla.blit(reiniciar, reiniciar_rect)
        
        salir = fuente_pequena.render("Presiona ESC para salir", True, GRIS)
        salir_rect = salir.get_rect(center=(ANCHO//2, 400))
        pantalla.blit(salir, salir_rect)
    
    else:  # Estados de juego
        # Dibujar información del juego
        nivel_texto = fuente_mediana.render(f"Nivel: {nivel}", True, NEGRO)
        pantalla.blit(nivel_texto, (50, 50))
        
        puntuacion_texto = fuente_mediana.render(f"Puntuación: {puntuacion}", True, NEGRO)
        pantalla.blit(puntuacion_texto, (50, 80))
        
        # Dibujar botones
        for i, boton in enumerate(botones):
            presionado = (i == boton_presionado)
            dibujar_boton(pantalla, boton, presionado, fuente_mediana)
        
        # Mensajes de estado
        if estado == MOSTRANDO_SECUENCIA:
            mensaje = fuente_mediana.render("Memoriza la secuencia...", True, NEGRO)
            mensaje_rect = mensaje.get_rect(center=(ANCHO//2, 120))
            pantalla.blit(mensaje, mensaje_rect)
        elif estado == ESPERANDO_JUGADOR:
            mensaje = fuente_mediana.render("Tu turno - Repite la secuencia", True, NEGRO)
            mensaje_rect = mensaje.get_rect(center=(ANCHO//2, 120))
            pantalla.blit(mensaje, mensaje_rect)

def punto_en_boton(pos, boton):
    """Verificar si un punto está dentro de un botón"""
    x, y, ancho, alto = boton[:4]
    px, py = pos
    return x <= px <= x + ancho and y <= py <= y + alto

def obtener_boton_clickeado(pos, botones):
    """Obtener el índice del botón clickeado"""
    for i, boton in enumerate(botones):
        if punto_en_boton(pos, boton):
            return i
    return -1

def reproducir_sonido(sonidos, indice):
    """Reproducir sonido del botón"""
    if indice in sonidos and sonidos[indice]:
        try:
            sonidos[indice].play()
        except:
            pass  # Ignorar errores de sonido

def agregar_color_secuencia(secuencia):
    """Agregar un nuevo color aleatorio a la secuencia"""
    secuencia.append(random.randint(0, 3))

def verificar_respuesta(secuencia, secuencia_jugador, indice_jugador):
    """Verificar si la respuesta del jugador es correcta"""
    if indice_jugador < len(secuencia):
        return secuencia[indice_jugador] == secuencia_jugador[indice_jugador]
    return False

def main():
    """Función principal del juego"""
    (pantalla, reloj, estado, secuencia, secuencia_jugador, indice_secuencia, 
     indice_jugador, nivel, puntuacion, tiempo_ultimo_boton, boton_presionado, 
     sonidos, botones) = inicializar_juego()
    
    corriendo = True
    
    while corriendo:
        tiempo_actual = pygame.time.get_ticks()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                elif evento.key == pygame.K_SPACE:
                    if estado == MENU or estado == GAME_OVER:
                        # Reiniciar juego
                        estado = JUGANDO
                        secuencia = []
                        secuencia_jugador = []
                        indice_secuencia = 0
                        indice_jugador = 0
                        nivel = 1
                        puntuacion = 0
                        agregar_color_secuencia(secuencia)
                        estado = MOSTRANDO_SECUENCIA
                        tiempo_ultimo_boton = tiempo_actual
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado == ESPERANDO_JUGADOR:
                    boton_clickeado = obtener_boton_clickeado(evento.pos, botones)
                    if boton_clickeado != -1:
                        boton_presionado = boton_clickeado
                        tiempo_ultimo_boton = tiempo_actual
                        secuencia_jugador.append(boton_clickeado)
                        reproducir_sonido(sonidos, boton_clickeado)
                        
                        # Verificar respuesta
                        if verificar_respuesta(secuencia, secuencia_jugador, indice_jugador):
                            indice_jugador += 1
                            
                            # Comprobar si completó la secuencia
                            if indice_jugador >= len(secuencia):
                                # Nivel completado
                                puntuacion += nivel * 10
                                nivel += 1
                                agregar_color_secuencia(secuencia)
                                secuencia_jugador = []
                                indice_jugador = 0
                                indice_secuencia = 0
                                estado = MOSTRANDO_SECUENCIA
                                tiempo_ultimo_boton = tiempo_actual + 1000  # Pausa antes de mostrar
                        else:
                            # Respuesta incorrecta
                            estado = GAME_OVER
        
        # Lógica del juego
        if estado == MOSTRANDO_SECUENCIA:
            if tiempo_actual - tiempo_ultimo_boton > 800:  # 800ms entre colores
                if indice_secuencia < len(secuencia):
                    # Mostrar siguiente color
                    boton_presionado = secuencia[indice_secuencia]
                    reproducir_sonido(sonidos, boton_presionado)
                    indice_secuencia += 1
                    tiempo_ultimo_boton = tiempo_actual
                else:
                    # Terminó de mostrar secuencia
                    boton_presionado = -1
                    estado = ESPERANDO_JUGADOR
                    secuencia_jugador = []
                    indice_jugador = 0
        
        # Quitar iluminación del botón después de un tiempo
        if boton_presionado != -1 and tiempo_actual - tiempo_ultimo_boton > 400:
            boton_presionado = -1
        
        # Dibujar todo
        dibujar_pantalla(pantalla, estado, botones, nivel, puntuacion, boton_presionado)
        
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()