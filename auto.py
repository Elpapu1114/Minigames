import pygame
import random
import math
import os

pygame.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
NARANJA = (255, 165, 0)

puntuacion = 0
velocidad_base = 5
nivel = 1
vidas = 3
estado_juego = "menu" 
tiempo_inicio_cuenta = 0

def cargar_imagenes():
    """Carga todas las imágenes del juego"""
    imagenes = {}
    try:
        
        imagenes['jugador'] = pygame.image.load(os.path.join("image", "autoesquivaverde.png"))
        imagenes['jugador'] = pygame.transform.scale(imagenes['jugador'], (90, 120))
        
       
        imagenes['auto_naranja'] = pygame.image.load(os.path.join("image", "autoesquivanaranja.png"))
        imagenes['auto_naranja'] = pygame.transform.scale(imagenes['auto_naranja'], (90, 120))
        
        imagenes['auto_violeta'] = pygame.image.load(os.path.join("image", "autoesquivavioleta.png"))
        imagenes['auto_violeta'] = pygame.transform.scale(imagenes['auto_violeta'], (90, 120))
        
        imagenes['auto_azul'] = pygame.image.load(os.path.join("image", "autoesquivaazul.png"))
        imagenes['auto_azul'] = pygame.transform.scale(imagenes['auto_azul'], (90, 120))

       
        imagenes['camion'] = pygame.image.load(os.path.join("image", "camionesquiva.png"))
        imagenes['camion'] = pygame.transform.scale(imagenes['camion'], (100, 150))
        
        print("Imágenes cargadas correctamente")
    except Exception as e:
        print(f"Error al cargar imágenes: {e}")
        imagenes = None
    
    return imagenes

def crear_pantalla():
    """Crea la ventana del juego"""
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego de Carreras - Esquiva Autos")
    return pantalla

def crear_coche():
    """Crea el coche del jugador"""
    return {
        'x': ANCHO_PANTALLA // 2,
        'y': ALTO_PANTALLA - 120,
        'ancho': 60,
        'alto': 90,
        'velocidad': 7,
        'color': VERDE
    }

def crear_obstaculo():
    """Crea un obstáculo aleatorio (auto o camión)"""
    tipo = random.choice(['auto_naranja', 'auto_violeta', 'auto_azul', 'camion'])
    
    if tipo == 'camion':
        ancho, alto = 70, 120
    else:
        ancho, alto = 60, 90
    
    return {
        'x': random.randint(50, ANCHO_PANTALLA - ancho - 50),
        'y': -alto,
        'ancho': ancho,
        'alto': alto,
        'velocidad': random.randint(3, 6) + velocidad_base,
        'tipo': tipo
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
    pantalla.fill((60, 60, 60))  
    
    pygame.draw.rect(pantalla, BLANCO, (30, 0, 8, ALTO_PANTALLA))
    pygame.draw.rect(pantalla, BLANCO, (ANCHO_PANTALLA - 38, 0, 8, ALTO_PANTALLA))
    
    carril_1 = ANCHO_PANTALLA // 3
    carril_2 = 2 * ANCHO_PANTALLA // 3

    for y in range(-50 + offset % 80, ALTO_PANTALLA, 80):
        pygame.draw.rect(pantalla, BLANCO, (carril_1 - 2, y, 4, 40))
        pygame.draw.rect(pantalla, BLANCO, (carril_2 - 2, y, 4, 40))

def dibujar_coche_con_imagen(pantalla, coche, imagenes):
    """Dibuja el coche del jugador usando la imagen"""
    if imagenes and 'jugador' in imagenes:
        pantalla.blit(imagenes['jugador'], (coche['x'], coche['y']))
    else:
        pygame.draw.rect(pantalla, coche['color'], 
                        (coche['x'], coche['y'], coche['ancho'], coche['alto']))

def dibujar_obstaculo_con_imagen(pantalla, obstaculo, imagenes):
    """Dibuja un obstáculo usando su imagen correspondiente"""
    if imagenes and obstaculo['tipo'] in imagenes:
        pantalla.blit(imagenes[obstaculo['tipo']], (obstaculo['x'], obstaculo['y']))
    else:
        
        pygame.draw.rect(pantalla, ROJO, 
                        (obstaculo['x'], obstaculo['y'], obstaculo['ancho'], obstaculo['alto']))

def dibujar_potenciador_detallado(pantalla, potenciador):
    """Dibuja potenciadores con símbolos"""
    pygame.draw.circle(pantalla, potenciador['color'],
                      (potenciador['x'] + potenciador['ancho'] // 2,
                       potenciador['y'] + potenciador['alto'] // 2),
                      potenciador['ancho'] // 2)
    
    centro_x = potenciador['x'] + potenciador['ancho'] // 2
    centro_y = potenciador['y'] + potenciador['alto'] // 2
    
    if potenciador['tipo'] == 'velocidad':
        puntos = [(centro_x, centro_y - 8), (centro_x - 5, centro_y + 2), (centro_x + 5, centro_y + 2)]
        pygame.draw.polygon(pantalla, NEGRO, puntos)
        
    elif potenciador['tipo'] == 'puntos':
        pygame.draw.line(pantalla, NEGRO, (centro_x - 5, centro_y), (centro_x + 5, centro_y), 3)
        pygame.draw.line(pantalla, NEGRO, (centro_x, centro_y - 5), (centro_x, centro_y + 5), 3)
        
    elif potenciador['tipo'] == 'vida':
        pygame.draw.circle(pantalla, NEGRO, (centro_x - 3, centro_y - 2), 3)
        pygame.draw.circle(pantalla, NEGRO, (centro_x + 3, centro_y - 2), 3)

def dibujar_interfaz(pantalla, fuente):
    """Dibuja la interfaz del usuario"""
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntos, (10, 10))
    
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto_nivel, (10, 40))

    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 70))
    
    texto_velocidad = fuente.render(f"Velocidad: {velocidad_base}", True, BLANCO)
    pantalla.blit(texto_velocidad, (ANCHO_PANTALLA - 150, 10))

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
    
    titulo = pygame.font.Font(None, 72).render("GAME OVER", True, ROJO)
    rect_titulo = titulo.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 100))
    pantalla.blit(titulo, rect_titulo)
    
    texto_puntos = fuente.render(f"Puntuación Final: {puntuacion}", True, BLANCO)
    rect_puntos = texto_puntos.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 20))
    pantalla.blit(texto_puntos, rect_puntos)

    texto_nivel = fuente.render(f"Nivel Alcanzado: {nivel}", True, BLANCO)
    rect_nivel = texto_nivel.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20))
    pantalla.blit(texto_nivel, rect_nivel)

    texto_reiniciar = fuente.render("Presiona ESPACIO para jugar de nuevo o ESC para salir", True, AMARILLO)
    rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80))
    pantalla.blit(texto_reiniciar, rect_reiniciar)

def dibujar_cuenta_regresiva(pantalla, fuente):
    """Dibuja la pantalla de cuenta regresiva"""
    global tiempo_inicio_cuenta

    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_cuenta
    tiempo_restante = 3 - int(tiempo_transcurrido)
    
    if tiempo_restante > 0:
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        overlay.set_alpha(180)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        texto_cuenta = pygame.font.Font(None, 150).render(str(tiempo_restante), True, AMARILLO)
        rect_cuenta = texto_cuenta.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
        pantalla.blit(texto_cuenta, rect_cuenta)
        
        texto_preparate = fuente.render("¡PREPÁRATE!", True, BLANCO)
        rect_preparate = texto_preparate.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80))
        pantalla.blit(texto_preparate, rect_preparate)

def reiniciar_juego():
    """Reinicia todas las variables del juego"""
    global puntuacion, velocidad_base, nivel, vidas, estado_juego
    puntuacion = 0
    velocidad_base = 5
    nivel = 1
    vidas = 3
    estado_juego = "cuenta_regresiva"

def mostrar_menu(pantalla, fuente):
    """Muestra el menú de inicio"""
    pantalla.fill(NEGRO)
    
    titulo = pygame.font.Font(None, 72).render("Esquiva Autos", True, VERDE)
    rect_titulo = titulo.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 100))
    pantalla.blit(titulo, rect_titulo)
    
    opcion_jugar = fuente.render("Presiona ESPACIO para Jugar", True, AMARILLO)
    rect_jugar = opcion_jugar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
    pantalla.blit(opcion_jugar, rect_jugar)
    
    opcion_salir = fuente.render("Presiona ESC para Salir", True, AMARILLO)
    rect_salir = opcion_salir.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 50))
    pantalla.blit(opcion_salir, rect_salir)
    
    controles = fuente.render("Usa las flechas o WASD para moverte", True, BLANCO)
    rect_controles = controles.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 120))
    pantalla.blit(controles, rect_controles)
    
    pygame.display.flip()

def juego_principal():
    """Función principal del juego"""
    global puntuacion, vidas
    
    pantalla = crear_pantalla()
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)

    imagenes = cargar_imagenes()

    mostrar_menu(pantalla, fuente)

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Iniciar el juego
                    juego_activo(imagenes)
                    ejecutando = False
                elif evento.key == pygame.K_ESCAPE:
                    # Salir del juego
                    ejecutando = False

    pygame.quit()

def juego_activo(imagenes):
    """Juego en funcionamiento"""
    global puntuacion, vidas, estado_juego, tiempo_inicio_cuenta
    
    pantalla = crear_pantalla()
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)

    coche = crear_coche()

    obstaculos = []
    potenciadores = []

    tiempo_obstaculo = 0
    tiempo_potenciador = 0
    offset_carretera = 0
    mensaje_potenciador = ""
    tiempo_mensaje = 0

    estado_juego = "cuenta_regresiva"
    tiempo_inicio_cuenta = pygame.time.get_ticks()
    
    ejecutando = True
    
    while ejecutando:
        dt = reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if estado_juego == "game_over":
                    if evento.key == pygame.K_SPACE:
                        reiniciar_juego()
                        coche = crear_coche()
                        obstaculos.clear()
                        potenciadores.clear()
                        tiempo_obstaculo = 0
                        tiempo_potenciador = 0
                        mensaje_potenciador = ""
                        tiempo_mensaje = 0
                        tiempo_inicio_cuenta = pygame.time.get_ticks()
                    elif evento.key == pygame.K_ESCAPE:
                        ejecutando = False
        
        if estado_juego == "cuenta_regresiva":
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_cuenta
            if tiempo_transcurrido >= 3:
                estado_juego = "jugando"
            
            offset_carretera += velocidad_base
            dibujar_carretera(pantalla, offset_carretera)
            dibujar_coche_con_imagen(pantalla, coche, imagenes)
            dibujar_interfaz(pantalla, fuente)
            dibujar_cuenta_regresiva(pantalla, fuente)
            
        elif estado_juego == "jugando":
            offset_carretera += velocidad_base
            
            teclas = pygame.key.get_pressed()
            
            mover_coche(coche, teclas)
            
            tiempo_obstaculo += dt
            if tiempo_obstaculo > max(800 - nivel * 50, 200):
                obstaculos.append(crear_obstaculo())
                tiempo_obstaculo = 0

            tiempo_potenciador += dt
            if tiempo_potenciador > random.randint(3000, 5000):
                potenciadores.append(crear_potenciador())
                tiempo_potenciador = 0

            mover_obstaculos(obstaculos)
            mover_potenciadores(potenciadores)

            for obstaculo in obstaculos[:]:
                if detectar_colision(coche, obstaculo):
                    obstaculos.remove(obstaculo)
                    vidas -= 1
                    if vidas <= 0:
                        estado_juego = "game_over"

            for potenciador in potenciadores[:]:
                if detectar_colision(coche, potenciador):
                    potenciadores.remove(potenciador)
                    mensaje_potenciador = aplicar_potenciador(potenciador, coche)
                    tiempo_mensaje = pygame.time.get_ticks()

            puntuacion += 1

            if actualizar_nivel():
                mensaje_potenciador = f"¡Nivel {nivel}!"
                tiempo_mensaje = pygame.time.get_ticks()

            dibujar_carretera(pantalla, offset_carretera)

            for obstaculo in obstaculos:
                dibujar_obstaculo_con_imagen(pantalla, obstaculo, imagenes)

            for potenciador in potenciadores:
                dibujar_potenciador_detallado(pantalla, potenciador)

            dibujar_coche_con_imagen(pantalla, coche, imagenes)

            dibujar_interfaz(pantalla, fuente)

            if mensaje_potenciador and pygame.time.get_ticks() - tiempo_mensaje < 2000:
                texto_mensaje = fuente.render(mensaje_potenciador, True, AMARILLO)
                rect_mensaje = texto_mensaje.get_rect(center=(ANCHO_PANTALLA // 2, 150))
                pantalla.blit(texto_mensaje, rect_mensaje)
            elif pygame.time.get_ticks() - tiempo_mensaje >= 2000:
                mensaje_potenciador = ""
        
        elif estado_juego == "game_over":

            pantalla_game_over(pantalla, fuente)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    juego_principal()
