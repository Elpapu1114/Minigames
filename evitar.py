import pygame
import sys
import random
import math

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
pygame.display.set_caption("Evita Obstáculos - Pygame")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 20, 60)
AZUL = (30, 144, 255)
VERDE = (34, 139, 34)
AMARILLO = (255, 215, 0)
NARANJA = (255, 140, 0)
VIOLETA = (138, 43, 226)
GRIS = (128, 128, 128)
CELESTE = (135, 206, 235)

FPS = 60

def menu_resolucion(pantalla):
    fuente = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 32)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 800, 600
                elif evento.key == pygame.K_2:
                    return 1024, 768
                elif evento.key == pygame.K_3:
                    return 1280, 720
                elif evento.key == pygame.K_4:
                    return 1440, 900
        
        pantalla.fill(NEGRO)
        
        titulo = fuente.render("EVITA OBSTÁCULOS", True, AMARILLO)
        pantalla.blit(titulo, (400 - titulo.get_width()//2, 100))
        
        subtitulo = fuente_pequena.render("Selecciona la resolución:", True, BLANCO)
        pantalla.blit(subtitulo, (400 - subtitulo.get_width()//2, 200))
        
        opciones = [
            "1) 800 x 600",
            "2) 1024 x 768", 
            "3) 1280 x 720",
            "4) 1440 x 900"
        ]
        
        for i, opcion in enumerate(opciones):
            texto = fuente_pequena.render(opcion, True, BLANCO)
            pantalla.blit(texto, (400 - texto.get_width()//2, 260 + i * 40))
        
        pygame.display.flip()

def cuenta_regresiva(pantalla, ancho, alto):
    fuente = pygame.font.Font(None, 144)
    
    for i in range(3, 0, -1):
        pantalla.fill(NEGRO)
        
        texto = fuente.render(str(i), True, BLANCO)
        pantalla.blit(texto, (ancho//2 - texto.get_width()//2, alto//2 - texto.get_height()//2))
        
        pygame.display.flip()
        pygame.time.wait(800)
    
    pantalla.fill(NEGRO)
    go_texto = fuente.render("¡VAMOS!", True, VERDE)
    pantalla.blit(go_texto, (ancho//2 - go_texto.get_width()//2, alto//2 - go_texto.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(600)

def pantalla_fin_juego(pantalla, ancho, alto, puntuacion, record_actual, es_record=False):
    fuente_grande = pygame.font.Font(None, 72)
    fuente_mediana = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 32)
    
    overlay = pygame.Surface((ancho, alto))
    overlay.set_alpha(180)
    overlay.fill(NEGRO)
    pantalla.blit(overlay, (0, 0))
    
    if es_record:
        titulo = fuente_grande.render("¡NUEVO RÉCORD!", True, AMARILLO)
    else:
        titulo = fuente_grande.render("FIN DEL JUEGO", True, ROJO)
    
    pantalla.blit(titulo, (ancho//2 - titulo.get_width()//2, alto//2 - 120))
    
    puntos = fuente_mediana.render(f"Puntuación: {int(puntuacion)}", True, BLANCO)
    pantalla.blit(puntos, (ancho//2 - puntos.get_width()//2, alto//2 - 60))
    
    if record_actual > 0:
        record_texto = fuente_pequena.render(f"Récord anterior: {int(record_actual)}", True, GRIS)
        pantalla.blit(record_texto, (ancho//2 - record_texto.get_width()//2, alto//2 - 20))
    
    instrucciones = [
        "ENTER - Jugar de nuevo",
        "ESC - Salir"
    ]
    
    for i, instruccion in enumerate(instrucciones):
        texto = fuente_pequena.render(instruccion, True, BLANCO)
        pantalla.blit(texto, (ancho//2 - texto.get_width()//2, alto//2 + 40 + i * 30))
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

def crear_obstaculo(ancho, alto, tamaño):
    x = random.randint(0, ancho - tamaño)
    y = random.randint(-alto, -tamaño)
    tipo = random.choice(['cuadrado', 'triangulo', 'circulo'])
    color = random.choice([ROJO, NARANJA, VIOLETA])
    return {
        'rect': pygame.Rect(x, y, tamaño, tamaño),
        'tipo': tipo,
        'color': color,
        'rotacion': 0
    }

def dibujar_obstaculo(pantalla, obstaculo):
    rect = obstaculo['rect']
    color = obstaculo['color']
    centro_x = rect.centerx
    centro_y = rect.centery
    
    if obstaculo['tipo'] == 'cuadrado':
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, BLANCO, rect, 2)
    
    elif obstaculo['tipo'] == 'triangulo':
        puntos = [
            (centro_x, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom)
        ]
        pygame.draw.polygon(pantalla, color, puntos)
        pygame.draw.polygon(pantalla, BLANCO, puntos, 2)
    
    elif obstaculo['tipo'] == 'circulo':
        pygame.draw.circle(pantalla, color, (centro_x, centro_y), rect.width//2)
        pygame.draw.circle(pantalla, BLANCO, (centro_x, centro_y), rect.width//2, 2)

def dibujar_jugador(pantalla, x, y, ancho_jugador, alto_jugador, tiempo):
    brillo = int(20 * math.sin(tiempo * 5))
    color_jugador = (min(255, AZUL[0] + brillo), min(255, AZUL[1] + brillo), min(255, AZUL[2] + brillo))
    
    rect_jugador = pygame.Rect(int(x), int(y), ancho_jugador, alto_jugador)
    pygame.draw.rect(pantalla, color_jugador, rect_jugador)
    pygame.draw.rect(pantalla, BLANCO, rect_jugador, 3)
    
    centro_x = int(x + ancho_jugador//2)
    centro_y = int(y + alto_jugador//2)
    pygame.draw.circle(pantalla, BLANCO, (centro_x, centro_y), 3)

def dibujar_fondo(pantalla, ancho, alto, tiempo):
    pantalla.fill(NEGRO)
    
    for i in range(20):
        x = (i * 100 + int(tiempo * 50)) % (ancho + 100) - 50
        y = random.randint(0, alto)
        brillo = int(50 + 30 * math.sin(tiempo + i))
        color_estrella = (brillo, brillo, brillo)
        pygame.draw.circle(pantalla, color_estrella, (x, y % alto), 1)

def ejecutar_juego(pantalla, ancho, alto, record_actual):
    reloj = pygame.time.Clock()
    
    ancho_jugador = ancho // 15
    alto_jugador = alto // 20
    velocidad_jugador = ancho / 2.5
    tamaño_obstaculo = ancho // 20
    velocidad_obstaculo_inicial = alto / 2
    num_obstaculos = 4
    
    jugador_x = ancho//2 - ancho_jugador//2
    jugador_y = alto - alto_jugador - 10
    
    obstaculos = []
    for _ in range(num_obstaculos):
        obstaculos.append(crear_obstaculo(ancho, alto, tamaño_obstaculo))
    
    puntuacion = 0
    tiempo_transcurrido = 0.0
    
    cuenta_regresiva(pantalla, ancho, alto)
    
    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_transcurrido += dt
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return record_actual, False
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador_x -= velocidad_jugador * dt
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador_x += velocidad_jugador * dt
        
        if jugador_x < 0:
            jugador_x = 0
        if jugador_x + ancho_jugador > ancho:
            jugador_x = ancho - ancho_jugador
        
        factor_velocidad = 1.0 + tiempo_transcurrido / 20.0
        velocidad_actual = velocidad_obstaculo_inicial * factor_velocidad
        
        for obstaculo in obstaculos:
            obstaculo['rect'].y += velocidad_actual * dt
            obstaculo['rotacion'] += dt * 90
            
            if obstaculo['rect'].top > alto:
                nuevo_obstaculo = crear_obstaculo(ancho, alto, tamaño_obstaculo)
                obstaculo.update(nuevo_obstaculo)
        
        rect_jugador = pygame.Rect(int(jugador_x), int(jugador_y), ancho_jugador, alto_jugador)
        
        for obstaculo in obstaculos:
            if rect_jugador.colliderect(obstaculo['rect']):
                es_record = puntuacion > record_actual
                nuevo_record = max(puntuacion, record_actual)
                jugar_otra_vez = pantalla_fin_juego(pantalla, ancho, alto, puntuacion, record_actual, es_record)
                return nuevo_record, jugar_otra_vez
        
        puntuacion += dt * 15 * factor_velocidad
        
        dibujar_fondo(pantalla, ancho, alto, tiempo_transcurrido)
        
        for obstaculo in obstaculos:
            dibujar_obstaculo(pantalla, obstaculo)
        
        dibujar_jugador(pantalla, jugador_x, jugador_y, ancho_jugador, alto_jugador, tiempo_transcurrido)
        
        fuente_puntos = pygame.font.Font(None, 56)
        texto_puntos = fuente_puntos.render(f"Puntos: {int(puntuacion)}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
        
        if record_actual > 0:
            fuente_record = pygame.font.Font(None, 32)
            texto_record = fuente_record.render(f"Récord: {int(record_actual)}", True, AMARILLO)
            pantalla.blit(texto_record, (10, 70))
        
        nivel_texto = pygame.font.Font(None, 32).render(f"Velocidad: x{factor_velocidad:.1f}", True, VERDE)
        pantalla.blit(nivel_texto, (ancho - nivel_texto.get_width() - 10, 10))
        
        pygame.display.flip()

def main():
    pantalla_temporal = pygame.display.set_mode((800, 600))
    ancho, alto = menu_resolucion(pantalla_temporal)
    pantalla = pygame.display.set_mode((ancho, alto))
    
    record = 0
    
    while True:
        nuevo_record, continuar = ejecutar_juego(pantalla, ancho, alto, record)
        record = nuevo_record
        
        if not continuar:
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()