import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Constantes del juego
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
NARANJA = (255, 165, 0)

# Variables globales del juego
puntuacion = 0
velocidad_base = 5
nivel = 1
vidas = 3

def crear_pantalla():
    """Crea la ventana del juego"""
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego de Carreras")
    return pantalla

def crear_coche():
    """Crea el coche del jugador"""
    return {
        'x': ANCHO_PANTALLA // 2,
        'y': ALTO_PANTALLA - 100,
        'ancho': 40,
        'alto': 60,
        'velocidad': 7,
        'color': AZUL
    }

def crear_obstaculo():
    """Crea un obstáculo aleatorio"""
    return {
        'x': random.randint(50, ANCHO_PANTALLA - 100),
        'y': -50,
        'ancho': random.randint(40, 80),
        'alto': random.randint(40, 80),
        'velocidad': random.randint(3, 6) + velocidad_base,
        'color': ROJO
    }

def crear_potenciador():
    """Crea un potenciador"""
    tipo = random.choice(['velocidad', 'puntos', 'vida'])
    colores = {'velocidad': AMARILLO, 'puntos': VERDE, 'vida': NARANJA}
    return {
        'x': random.randint(50, ANCHO_PANTALLA - 50),
        'y': -30,
        'ancho': 30,
        'alto': 30,
        'velocidad': velocidad_base + 2,
        'tipo': tipo,
        'color': colores[tipo]
    }

def mover_coche(coche, teclas):
    """Mueve el coche según las teclas presionadas"""
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        coche['x'] -= coche['velocidad']
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        coche['x'] += coche['velocidad']
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        coche['y'] -= coche['velocidad']
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        coche['y'] += coche['velocidad']
    
    # Mantener el coche dentro de la pantalla
    coche['x'] = max(0, min(coche['x'], ANCHO_PANTALLA - coche['ancho']))
    coche['y'] = max(0, min(coche['y'], ALTO_PANTALLA - coche['alto']))

def mover_obstaculos(obstaculos):
    """Mueve todos los obstáculos hacia abajo"""
    for obstaculo in obstaculos[:]:
        obstaculo['y'] += obstaculo['velocidad']
        if obstaculo['y'] > ALTO_PANTALLA:
            obstaculos.remove(obstaculo)

def mover_potenciadores(potenciadores):
    """Mueve todos los potenciadores hacia abajo"""
    for potenciador in potenciadores[:]:
        potenciador['y'] += potenciador['velocidad']
        if potenciador['y'] > ALTO_PANTALLA:
            potenciadores.remove(potenciador)

def detectar_colision(obj1, obj2):
    """Detecta colisión entre dos objetos rectangulares"""
    return (obj1['x'] < obj2['x'] + obj2['ancho'] and
            obj1['x'] + obj1['ancho'] > obj2['x'] and
            obj1['y'] < obj2['y'] + obj2['alto'] and
            obj1['y'] + obj1['alto'] > obj2['y'])

def aplicar_potenciador(potenciador, coche):
    """Aplica el efecto de un potenciador"""
    global puntuacion, vidas
    
    if potenciador['tipo'] == 'velocidad':
        coche['velocidad'] = min(coche['velocidad'] + 1, 12)
        return "¡Velocidad aumentada!"
    elif potenciador['tipo'] == 'puntos':
        puntuacion += 50
        return "¡+50 puntos!"
    elif potenciador['tipo'] == 'vida':
        vidas = min(vidas + 1, 5)
        return "¡Vida extra!"

def dibujar_carretera(pantalla, offset):
    """Dibuja la carretera con líneas centrales y carriles más realistas"""
    pantalla.fill((60, 60, 60))  # Asfalto gris oscuro
    
    # Líneas laterales (bordes de la carretera)
    pygame.draw.rect(pantalla, BLANCO, (30, 0, 8, ALTO_PANTALLA))
    pygame.draw.rect(pantalla, BLANCO, (ANCHO_PANTALLA - 38, 0, 8, ALTO_PANTALLA))
    
    # Líneas de carriles (divisiones)
    carril_1 = ANCHO_PANTALLA // 3
    carril_2 = 2 * ANCHO_PANTALLA // 3
    
    # Líneas discontinuas de carriles
    for y in range(-50 + offset % 80, ALTO_PANTALLA, 80):
        pygame.draw.rect(pantalla, BLANCO, (carril_1 - 2, y, 4, 40))
        pygame.draw.rect(pantalla, BLANCO, (carril_2 - 2, y, 4, 40))

def dibujar_objeto(pantalla, objeto):
    """Dibuja un objeto rectangular"""
    pygame.draw.rect(pantalla, objeto['color'], 
                    (objeto['x'], objeto['y'], objeto['ancho'], objeto['alto']))

def dibujar_coche_detallado(pantalla, coche):
    """Dibuja el coche con más detalles"""
    # Cuerpo principal
    pygame.draw.rect(pantalla, coche['color'], 
                    (coche['x'], coche['y'], coche['ancho'], coche['alto']))
    
    # Ventanas
    pygame.draw.rect(pantalla, BLANCO, 
                    (coche['x'] + 5, coche['y'] + 5, coche['ancho'] - 10, 15))
    pygame.draw.rect(pantalla, BLANCO, 
                    (coche['x'] + 5, coche['y'] + 25, coche['ancho'] - 10, 15))
    
    # Ruedas
    pygame.draw.circle(pantalla, NEGRO, (coche['x'] + 8, coche['y'] + 10), 5)
    pygame.draw.circle(pantalla, NEGRO, (coche['x'] + coche['ancho'] - 8, coche['y'] + 10), 5)
    pygame.draw.circle(pantalla, NEGRO, (coche['x'] + 8, coche['y'] + coche['alto'] - 10), 5)
    pygame.draw.circle(pantalla, NEGRO, (coche['x'] + coche['ancho'] - 8, coche['y'] + coche['alto'] - 10), 5)

def dibujar_potenciador_detallado(pantalla, potenciador):
    """Dibuja potenciadores con símbolos"""
    pygame.draw.circle(pantalla, potenciador['color'],
                      (potenciador['x'] + potenciador['ancho'] // 2,
                       potenciador['y'] + potenciador['alto'] // 2),
                      potenciador['ancho'] // 2)
    
    # Símbolo según el tipo
    centro_x = potenciador['x'] + potenciador['ancho'] // 2
    centro_y = potenciador['y'] + potenciador['alto'] // 2
    
    if potenciador['tipo'] == 'velocidad':
        # Flecha hacia arriba
        puntos = [(centro_x, centro_y - 8), (centro_x - 5, centro_y + 2), (centro_x + 5, centro_y + 2)]
        pygame.draw.polygon(pantalla, NEGRO, puntos)
    elif potenciador['tipo'] == 'puntos':
        # Signo +
        pygame.draw.line(pantalla, NEGRO, (centro_x - 5, centro_y), (centro_x + 5, centro_y), 3)
        pygame.draw.line(pantalla, NEGRO, (centro_x, centro_y - 5), (centro_x, centro_y + 5), 3)
    elif potenciador['tipo'] == 'vida':
        # Corazón simplificado
        pygame.draw.circle(pantalla, NEGRO, (centro_x - 3, centro_y - 2), 3)
        pygame.draw.circle(pantalla, NEGRO, (centro_x + 3, centro_y - 2), 3)

def dibujar_interfaz(pantalla, fuente):
    """Dibuja la interfaz del usuario"""
    # Puntuación
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntos, (10, 10))
    
    # Nivel
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto_nivel, (10, 40))
    
    # Vidas
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 70))
    
    # Velocidad
    texto_velocidad = fuente.render(f"Velocidad: {velocidad_base}", True, BLANCO)
    pantalla.blit(texto_velocidad, (ANCHO_PANTALLA - 150, 10))

def mostrar_mensaje(pantalla, fuente, mensaje, color=BLANCO):
    """Muestra un mensaje en el centro de la pantalla"""
    texto = fuente.render(mensaje, True, color)
    rect_texto = texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
    pantalla.blit(texto, rect_texto)

def actualizar_nivel():
    """Actualiza el nivel basado en la puntuación"""
    global nivel, velocidad_base
    nuevo_nivel = (puntuacion // 200) + 1
    if nuevo_nivel > nivel:
        nivel = nuevo_nivel
        velocidad_base = min(velocidad_base + 1, 15)
        return True
    return False

def pantalla_game_over(pantalla, fuente):
    """Muestra la pantalla de game over"""
    pantalla.fill(NEGRO)
    
    # Título
    titulo = pygame.font.Font(None, 72).render("GAME OVER", True, ROJO)
    rect_titulo = titulo.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 100))
    pantalla.blit(titulo, rect_titulo)
    
    # Puntuación final
    texto_puntos = fuente.render(f"Puntuación Final: {puntuacion}", True, BLANCO)
    rect_puntos = texto_puntos.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 20))
    pantalla.blit(texto_puntos, rect_puntos)
    
    # Nivel alcanzado
    texto_nivel = fuente.render(f"Nivel Alcanzado: {nivel}", True, BLANCO)
    rect_nivel = texto_nivel.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20))
    pantalla.blit(texto_nivel, rect_nivel)
    
    # Instrucciones
    texto_reiniciar = fuente.render("Presiona ESPACIO para jugar de nuevo o ESC para salir", True, AMARILLO)
    rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80))
    pantalla.blit(texto_reiniciar, rect_reiniciar)

def reiniciar_juego():
    """Reinicia todas las variables del juego"""
    global puntuacion, velocidad_base, nivel, vidas
    puntuacion = 0
    velocidad_base = 5
    nivel = 1
    vidas = 3

def juego_principal():
    """Función principal del juego"""
    global puntuacion, vidas
    
    pantalla = crear_pantalla()
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    
    # Crear el coche del jugador
    coche = crear_coche()
    
    # Listas para obstáculos y potenciadores
    obstaculos = []
    potenciadores = []
    
    # Variables de tiempo y efectos
    tiempo_obstaculo = 0
    tiempo_potenciador = 0
    offset_carretera = 0
    mensaje_potenciador = ""
    tiempo_mensaje = 0
    
    ejecutando = True
    juego_activo = True
    
    while ejecutando:
        dt = reloj.tick(FPS)
        offset_carretera += velocidad_base
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if not juego_activo:
                    if evento.key == pygame.K_SPACE:
                        # Reiniciar juego
                        reiniciar_juego()
                        coche = crear_coche()
                        obstaculos.clear()
                        potenciadores.clear()
                        juego_activo = True
                        tiempo_obstaculo = 0
                        tiempo_potenciador = 0
                        mensaje_potenciador = ""
                        tiempo_mensaje = 0
                    elif evento.key == pygame.K_ESCAPE:
                        ejecutando = False
        
        if juego_activo:
            # Obtener teclas presionadas
            teclas = pygame.key.get_pressed()
            
            # Mover el coche
            mover_coche(coche, teclas)
            
            # Crear obstáculos
            tiempo_obstaculo += dt
            if tiempo_obstaculo > max(800 - nivel * 50, 200):
                obstaculos.append(crear_obstaculo())
                tiempo_obstaculo = 0
            
            # Crear potenciadores
            tiempo_potenciador += dt
            if tiempo_potenciador > random.randint(3000, 5000):
                potenciadores.append(crear_potenciador())
                tiempo_potenciador = 0
            
            # Mover obstáculos y potenciadores
            mover_obstaculos(obstaculos)
            mover_potenciadores(potenciadores)
            
            # Detectar colisiones con obstáculos
            for obstaculo in obstaculos[:]:
                if detectar_colision(coche, obstaculo):
                    obstaculos.remove(obstaculo)
                    vidas -= 1
                    if vidas <= 0:
                        juego_activo = False
            
            # Detectar colisiones con potenciadores
            for potenciador in potenciadores[:]:
                if detectar_colision(coche, potenciador):
                    potenciadores.remove(potenciador)
                    mensaje_potenciador = aplicar_potenciador(potenciador, coche)
                    tiempo_mensaje = pygame.time.get_ticks()
            
            # Aumentar puntuación por tiempo
            puntuacion += 1
            
            # Actualizar nivel
            if actualizar_nivel():
                mensaje_potenciador = f"¡Nivel {nivel}!"
                tiempo_mensaje = pygame.time.get_ticks()
            
            # Dibujar todo
            dibujar_carretera(pantalla, offset_carretera)
            
            # Dibujar obstáculos
            for obstaculo in obstaculos:
                dibujar_objeto(pantalla, obstaculo)
            
            # Dibujar potenciadores
            for potenciador in potenciadores:
                dibujar_potenciador_detallado(pantalla, potenciador)
            
            # Dibujar el coche
            dibujar_coche_detallado(pantalla, coche)
            
            # Dibujar interfaz
            dibujar_interfaz(pantalla, fuente)
            
            # Mostrar mensaje de potenciador
            if mensaje_potenciador and pygame.time.get_ticks() - tiempo_mensaje < 2000:
                texto_mensaje = fuente.render(mensaje_potenciador, True, AMARILLO)
                rect_mensaje = texto_mensaje.get_rect(center=(ANCHO_PANTALLA // 2, 150))
                pantalla.blit(texto_mensaje, rect_mensaje)
            elif pygame.time.get_ticks() - tiempo_mensaje >= 2000:
                mensaje_potenciador = ""
        
        else:
            # Pantalla de game over
            pantalla_game_over(pantalla, fuente)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    juego_principal()