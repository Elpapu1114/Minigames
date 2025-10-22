import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuraciones de la ventana
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (100, 150, 255)
VERDE = (50, 200, 50)
ROJO = (255, 100, 100)
AMARILLO = (255, 255, 100)
GRIS = (128, 128, 128)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
CYAN = (0, 255, 255)

# Configuraciones de dificultad
DIFICULTADES = {
    'FACIL': {
        'nombre': 'FÁCIL',
        'color': VERDE,
        'distancia_min': 50,
        'distancia_max': 90,
        'altura_min': 60,
        'altura_max': 100,
        'velocidad_inicial': 4,
        'prob_impulsor': 0.3
    },
    'MEDIO': {
        'nombre': 'MEDIO',
        'color': NARANJA,
        'distancia_min': 70,
        'distancia_max': 120,
        'altura_min': 80,
        'altura_max': 130,
        'velocidad_inicial': 5,
        'prob_impulsor': 0.2
    },
    'DIFICIL': {
        'nombre': 'DIFÍCIL',
        'color': ROJO,
        'distancia_min': 100,
        'distancia_max': 160,
        'altura_min': 100,
        'altura_max': 150,
        'velocidad_inicial': 6,
        'prob_impulsor': 0.15
    }
}

# Variables globales del juego
jugador = None
plataformas = []
impulsores = []
camara_y = 0
altura_maxima = 0
puntuacion = 0
game_over = False
pantalla = None
reloj = None
fuente = None
dificultad_actual = 'FACIL'
en_menu = True
en_menu_eleccion = False
velocidad_acumulada = 0
tiempo_impulso = 0
img_menu = None
img_menu_eleccion = None
img_game_over = None

def inicializar_pygame():
    """Inicializa pygame y crea la ventana"""
    global pantalla, reloj, fuente, img_menu, img_menu_eleccion, img_game_over
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Sky Hopper - Estilo Pou")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    
    # Cargar imágenes
    try:
        img_menu = pygame.image.load('image/menu_sky_hopper.png')
        img_menu = pygame.transform.scale(img_menu, (ANCHO, ALTO))
    except:
        img_menu = None
        print("No se pudo cargar menu_sky_hopper.png")
        
    try:
        img_menu_eleccion = pygame.image.load('image/menu_eleccion_sky_hopper.png')
        img_menu_eleccion = pygame.transform.scale(img_menu_eleccion, (ANCHO, ALTO))
    except:
        img_menu_eleccion = None
        print("No se pudo cargar menu_eleccion_sky_hopper.png")
        
    try:
        img_game_over = pygame.image.load('image/game_over_sky_hopper.png')
        img_game_over = pygame.transform.scale(img_game_over, (ANCHO, ALTO))
    except:
        img_game_over = None
        print("No se pudo cargar game_over_sky_hopper.png")

def crear_jugador(x, y):
    """Crea y retorna un diccionario con los datos del jugador"""
    config = DIFICULTADES[dificultad_actual]
    return {
        'x': x,
        'y': y,
        'ancho': 30,
        'alto': 40,
        'vel_x': 0,
        'vel_y': 0,
        'en_suelo': False,
        'velocidad_base': config['velocidad_inicial'],
        'velocidad_actual': config['velocidad_inicial'],
        'fuerza_salto_base': -15,
        'fuerza_salto_actual': -15,
        'gravedad': 0.8,
        'con_impulso': False
    }

def crear_plataforma(x, y, ancho, tiene_impulsor=False):
    """Crea y retorna un diccionario con los datos de una plataforma"""
    return {
        'x': x,
        'y': y,
        'ancho': ancho,
        'alto': 20,
        'tiene_impulsor': tiene_impulsor
    }

def crear_impulsor(x, y):
    """Crea un impulsor (power-up)"""
    return {
        'x': x,
        'y': y,
        'ancho': 15,
        'alto': 15,
        'activo': True,
        'tiempo_animacion': 0
    }

def actualizar_velocidad_progresiva():
    """Aumenta la velocidad y salto del jugador con el tiempo"""
    global velocidad_acumulada, jugador
    
    # Aumentar velocidad cada 10 puntos de altura
    incremento = puntuacion // 50
    velocidad_acumulada = incremento * 0.5
    
    # Aplicar incrementos al jugador
    config = DIFICULTADES[dificultad_actual]
    jugador['velocidad_actual'] = min(config['velocidad_inicial'] + velocidad_acumulada, 12)
    jugador['fuerza_salto_actual'] = max(jugador['fuerza_salto_base'] - incremento * 0.5, -25)

def actualizar_impulso():
    """Maneja el efecto del impulso temporal"""
    global tiempo_impulso, jugador
    
    if tiempo_impulso > 0:
        tiempo_impulso -= 1
        jugador['con_impulso'] = True
        # Durante el impulso: mayor velocidad y salto
        jugador['velocidad_actual'] *= 1.5
        jugador['fuerza_salto_actual'] *= 1.3
    else:
        jugador['con_impulso'] = False

def actualizar_jugador(jugador, teclas):
    """Actualiza la posición y velocidad del jugador"""
    # Actualizar velocidad progresiva
    actualizar_velocidad_progresiva()
    actualizar_impulso()
    
    # Movimiento horizontal
    jugador['vel_x'] = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jugador['vel_x'] = -jugador['velocidad_actual']
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jugador['vel_x'] = jugador['velocidad_actual']
        
    # Salto
    if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and jugador['en_suelo']:
        jugador['vel_y'] = jugador['fuerza_salto_actual']
        jugador['en_suelo'] = False
        
    # Aplicar gravedad
    jugador['vel_y'] += jugador['gravedad']
    
    # Actualizar posición
    jugador['x'] += jugador['vel_x']
    jugador['y'] += jugador['vel_y']
    
    # Limitar movimiento horizontal a la pantalla
    if jugador['x'] < 0:
        jugador['x'] = 0
    elif jugador['x'] > ANCHO - jugador['ancho']:
        jugador['x'] = ANCHO - jugador['ancho']

def dibujar_jugador(jugador, camara_y):
    """Dibuja el jugador en pantalla"""
    color_jugador = ROJO
    if jugador['con_impulso']:
        # Efecto parpadeante durante el impulso
        color_jugador = CYAN if (tiempo_impulso // 5) % 2 == 0 else AMARILLO
    
    pygame.draw.rect(pantalla, color_jugador, 
                    (jugador['x'], jugador['y'] - camara_y, jugador['ancho'], jugador['alto']))
    
    # Ojos del jugador
    pygame.draw.circle(pantalla, BLANCO, 
                      (int(jugador['x'] + 8), int(jugador['y'] - camara_y + 10)), 4)
    pygame.draw.circle(pantalla, BLANCO, 
                      (int(jugador['x'] + 22), int(jugador['y'] - camara_y + 10)), 4)
    pygame.draw.circle(pantalla, NEGRO, 
                      (int(jugador['x'] + 8), int(jugador['y'] - camara_y + 10)), 2)
    pygame.draw.circle(pantalla, NEGRO, 
                      (int(jugador['x'] + 22), int(jugador['y'] - camara_y + 10)), 2)
    
    # Indicador de impulso
    if jugador['con_impulso']:
        pygame.draw.circle(pantalla, AMARILLO, 
                          (int(jugador['x'] + 15), int(jugador['y'] - camara_y - 10)), 8, 3)

def dibujar_plataforma(plataforma, camara_y):
    """Dibuja una plataforma en pantalla si está visible"""
    if -50 < plataforma['y'] - camara_y < ALTO + 50:
        # Color según dificultad
        color = DIFICULTADES[dificultad_actual]['color']
        
        pygame.draw.rect(pantalla, color, 
                       (plataforma['x'], plataforma['y'] - camara_y, plataforma['ancho'], plataforma['alto']))
        # Borde de la plataforma
        pygame.draw.rect(pantalla, NEGRO, 
                       (plataforma['x'], plataforma['y'] - camara_y, plataforma['ancho'], plataforma['alto']), 2)

def dibujar_impulsor(impulsor, camara_y):
    """Dibuja un impulsor animado"""
    if impulsor['activo'] and -50 < impulsor['y'] - camara_y < ALTO + 50:
        # Animación de rotación
        impulsor['tiempo_animacion'] += 1
        offset_y = math.sin(impulsor['tiempo_animacion'] * 0.2) * 3
        
        # Dibujar estrella (impulsor)
        centro_x = impulsor['x'] + impulsor['ancho'] // 2
        centro_y = impulsor['y'] + impulsor['alto'] // 2 - camara_y + offset_y
        
        # Estrella de 5 puntas
        puntos = []
        for i in range(10):
            angulo = i * math.pi / 5
            radio = 12 if i % 2 == 0 else 6
            px = centro_x + radio * math.cos(angulo - math.pi/2)
            py = centro_y + radio * math.sin(angulo - math.pi/2)
            puntos.append((px, py))
        
        pygame.draw.polygon(pantalla, AMARILLO, puntos)
        pygame.draw.polygon(pantalla, NARANJA, puntos, 2)

def calcular_distancia_salto(altura_diferencia):
    """Calcula la distancia máxima horizontal que puede alcanzar el jugador"""
    config = DIFICULTADES[dificultad_actual]
    fuerza_salto = 15 + velocidad_acumulada * 0.5
    gravedad = 0.8
    velocidad_horizontal = config['velocidad_inicial'] + velocidad_acumulada
    
    tiempo_aire = math.sqrt(2 * (fuerza_salto + altura_diferencia) / gravedad)
    distancia_maxima = velocidad_horizontal * tiempo_aire
    
    # Margen de seguridad según dificultad
    margen = 0.9 if dificultad_actual == 'FACIL' else 0.8 if dificultad_actual == 'MEDIO' else 0.7
    return distancia_maxima * margen

def generar_plataforma_alcanzable(ultima_plataforma):
    """Genera una nueva plataforma según la dificultad"""
    config = DIFICULTADES[dificultad_actual]
    
    # Altura de la nueva plataforma según dificultad
    nueva_altura = random.randint(config['altura_min'], config['altura_max'])
    nueva_y = ultima_plataforma['y'] - nueva_altura
    
    # Distancia horizontal según dificultad
    distancia_horizontal = random.randint(config['distancia_min'], config['distancia_max'])
    
    # Ancho de la plataforma
    nuevo_ancho = random.randint(80, 160)
    
    # Posición X
    centro_anterior = ultima_plataforma['x'] + ultima_plataforma['ancho'] // 2
    direccion = random.choice([-1, 1])  # Izquierda o derecha
    
    centro_nuevo = centro_anterior + (direccion * distancia_horizontal)
    nueva_x = centro_nuevo - nuevo_ancho // 2
    
    # Asegurar que esté en pantalla
    nueva_x = max(0, min(ANCHO - nuevo_ancho, nueva_x))
    
    # Decidir si tiene impulsor
    tiene_impulsor = random.random() < config['prob_impulsor']
    
    return crear_plataforma(nueva_x, nueva_y, nuevo_ancho, tiene_impulsor)

def generar_plataformas_iniciales():
    """Genera las plataformas iniciales del juego"""
    global plataformas, impulsores
    plataformas = []
    impulsores = []
    
    # Plataforma inicial
    plataforma_inicial = crear_plataforma(300, 450, 200, False)
    plataformas.append(plataforma_inicial)
    
    # Generar plataformas hacia arriba
    for i in range(25):
        nueva_plataforma = generar_plataforma_alcanzable(plataformas[-1])
        plataformas.append(nueva_plataforma)
        
        # Agregar impulsor si la plataforma lo tiene
        if nueva_plataforma['tiene_impulsor']:
            impulsor_x = nueva_plataforma['x'] + nueva_plataforma['ancho'] // 2 - 7
            impulsor_y = nueva_plataforma['y'] - 25
            impulsores.append(crear_impulsor(impulsor_x, impulsor_y))

def generar_mas_plataformas():
    """Genera más plataformas cuando sea necesario"""
    global plataformas, impulsores, camara_y
    
    if len(plataformas) > 0:
        plataforma_mas_alta = min(p['y'] for p in plataformas)
        if plataforma_mas_alta > camara_y - 500:
            for _ in range(8):
                nueva_plataforma = generar_plataforma_alcanzable(plataformas[-1])
                plataformas.append(nueva_plataforma)
                
                # Agregar impulsor si corresponde
                if nueva_plataforma['tiene_impulsor']:
                    impulsor_x = nueva_plataforma['x'] + nueva_plataforma['ancho'] // 2 - 7
                    impulsor_y = nueva_plataforma['y'] - 25
                    impulsores.append(crear_impulsor(impulsor_x, impulsor_y))

def limpiar_plataformas():
    """Elimina plataformas e impulsores que están muy abajo"""
    global plataformas, impulsores, camara_y
    plataformas = [p for p in plataformas if p['y'] < camara_y + ALTO + 200]
    impulsores = [i for i in impulsores if i['y'] < camara_y + ALTO + 200]

def comprobar_colisiones():
    """Comprueba colisiones entre el jugador y las plataformas"""
    global jugador, plataformas, impulsores, tiempo_impulso
    
    jugador_rect = pygame.Rect(jugador['x'], jugador['y'], 
                             jugador['ancho'], jugador['alto'])
    
    jugador['en_suelo'] = False
    
    # Colisiones con plataformas
    for plataforma in plataformas:
        plat_rect = pygame.Rect(plataforma['x'], plataforma['y'], 
                              plataforma['ancho'], plataforma['alto'])
        
        if jugador_rect.colliderect(plat_rect):
            if jugador['vel_y'] > 0 and jugador['y'] < plataforma['y']:
                jugador['y'] = plataforma['y'] - jugador['alto']
                jugador['vel_y'] = 0
                jugador['en_suelo'] = True
    
    # Colisiones con impulsores
    for impulsor in impulsores:
        if impulsor['activo']:
            imp_rect = pygame.Rect(impulsor['x'], impulsor['y'], 
                                 impulsor['ancho'], impulsor['alto'])
            
            if jugador_rect.colliderect(imp_rect):
                impulsor['activo'] = False
                tiempo_impulso = 180  # 3 segundos a 60 FPS

def actualizar_camara():
    """Actualiza la posición de la cámara para seguir al jugador"""
    global camara_y, jugador, altura_maxima, puntuacion
    
    objetivo_camara = jugador['y'] - ALTO // 2
    if objetivo_camara < camara_y:
        camara_y = objetivo_camara
        
    if jugador['y'] < altura_maxima:
        altura_maxima = jugador['y']
        puntuacion = max(0, int((450 - altura_maxima) / 10))

def comprobar_game_over():
    """Comprueba si el juego ha terminado"""
    global game_over, jugador, camara_y
    
    if jugador['y'] > camara_y + ALTO + 100:
        game_over = True

def dibujar_fondo():
    """Dibuja el fondo con gradiente según dificultad"""
    color_base = DIFICULTADES[dificultad_actual]['color']
    
    for y in range(ALTO):
        intensidad = y / ALTO
        r = int(color_base[0] * 0.3 + intensidad * 50)
        g = int(color_base[1] * 0.3 + intensidad * 50)
        b = int(color_base[2] * 0.3 + intensidad * 100)
        color = (min(255, r), min(255, g), min(255, b))
        pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))

def dibujar_menu():
    """Dibuja el menú principal con imagen de fondo"""
    if img_menu:
        pantalla.blit(img_menu, (0, 0))
    else:
        # Fallback si no se carga la imagen
        pantalla.fill((50, 50, 100))
        
        fuente_titulo = pygame.font.Font(None, 72)
        titulo = fuente_titulo.render("SKY HOPPER", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        
        fuente_inst = pygame.font.Font(None, 48)
        texto_space = fuente_inst.render("PRESS SPACE TO CONTINUE", True, BLANCO)
        pantalla.blit(texto_space, (ANCHO//2 - texto_space.get_width()//2, 400))
        
        texto_esc = fuente_inst.render("ESC TO EXIT", True, BLANCO)
        pantalla.blit(texto_esc, (ANCHO//2 - texto_esc.get_width()//2, 500))

def dibujar_menu_eleccion():
    """Dibuja el menú de selección de dificultad con imagen de fondo"""
    if img_menu_eleccion:
        pantalla.blit(img_menu_eleccion, (0, 0))
    else:
        # Fallback si no se carga la imagen
        pantalla.fill((50, 50, 100))
        
        fuente_titulo = pygame.font.Font(None, 72)
        titulo = fuente_titulo.render("CHOOSE DIFFICULTY", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        # Opciones de dificultad
        y_inicio = 300
        opciones = ["1. EASY", "2. MEDIUM", "3. HARD"]
        
        fuente_opcion = pygame.font.Font(None, 64)
        for i, texto in enumerate(opciones):
            texto_render = fuente_opcion.render(texto, True, BLANCO)
            pantalla.blit(texto_render, (ANCHO//2 - texto_render.get_width()//2, y_inicio + i*100))

def dibujar_ui():
    """Dibuja la interfaz de usuario"""
    global puntuacion, fuente, game_over, velocidad_acumulada, tiempo_impulso
    
    # Puntuación
    texto_puntuacion = fuente.render(f"Altura: {puntuacion}m", True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))
    
    # Dificultad
    config = DIFICULTADES[dificultad_actual]
    texto_dif = fuente.render(f"Dificultad: {config['nombre']}", True, config['color'])
    pantalla.blit(texto_dif, (10, 50))
    
    # Velocidad actual
    vel_text = f"Velocidad: {jugador['velocidad_actual']:.1f}"
    texto_vel = fuente.render(vel_text, True, BLANCO)
    pantalla.blit(texto_vel, (10, 90))
    
    # Indicador de impulso
    if tiempo_impulso > 0:
        tiempo_restante = tiempo_impulso / 60
        texto_impulso = fuente.render(f"¡IMPULSO! {tiempo_restante:.1f}s", True, AMARILLO)
        pantalla.blit(texto_impulso, (ANCHO - texto_impulso.get_width() - 10, 10))

def dibujar_game_over():
    """Dibuja la pantalla de game over con imagen de fondo"""
    if img_game_over:
        pantalla.blit(img_game_over, (0, 0))
    else:
        # Fallback si no se carga la imagen
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(128)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))
        
        fuente_grande = pygame.font.Font(None, 72)
        fuente_mediana = pygame.font.Font(None, 36)
        
        texto_go = fuente_grande.render("GAME OVER", True, BLANCO)
        texto_reinicio = fuente_mediana.render("PRESS SPACE TO PLAY AGAIN", True, AMARILLO)
        texto_menu = fuente_mediana.render("ESC TO QUIT", True, CYAN)
        
        pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, ALTO//2 - 100))
        pantalla.blit(texto_reinicio, (ANCHO//2 - texto_reinicio.get_width()//2, ALTO//2 + 50))
        pantalla.blit(texto_menu, (ANCHO//2 - texto_menu.get_width()//2, ALTO//2 + 100))

def reiniciar_juego():
    """Reinicia el juego al estado inicial"""
    global jugador, plataformas, impulsores, camara_y, altura_maxima, puntuacion, game_over, velocidad_acumulada, tiempo_impulso
    
    jugador = crear_jugador(ANCHO // 2, 400)
    generar_plataformas_iniciales()
    camara_y = 0
    altura_maxima = 0
    puntuacion = 0
    velocidad_acumulada = 0
    tiempo_impulso = 0
    game_over = False

def actualizar_juego(teclas):
    """Actualiza toda la lógica del juego"""
    if not game_over:
        actualizar_jugador(jugador, teclas)
        comprobar_colisiones()
        actualizar_camara()
        comprobar_game_over()
        limpiar_plataformas()
        generar_mas_plataformas()

def dibujar_juego():
    """Dibuja todos los elementos del juego"""
    dibujar_fondo()
    
    for plataforma in plataformas:
        dibujar_plataforma(plataforma, camara_y)
        
    for impulsor in impulsores:
        dibujar_impulsor(impulsor, camara_y)
        
    dibujar_jugador(jugador, camara_y)
    dibujar_ui()
    
    if game_over:
        dibujar_game_over()

def manejar_eventos():
    """Maneja todos los eventos de pygame"""
    global game_over, en_menu, en_menu_eleccion, dificultad_actual
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        elif evento.type == pygame.KEYDOWN:
            if en_menu and not en_menu_eleccion:
                # Menú principal
                if evento.key == pygame.K_SPACE:
                    en_menu_eleccion = True
                elif evento.key == pygame.K_ESCAPE:
                    return False
                    
            elif en_menu_eleccion:
                # Menú de selección de dificultad
                if evento.key == pygame.K_1:
                    dificultad_actual = 'FACIL'
                    en_menu = False
                    en_menu_eleccion = False
                    reiniciar_juego()
                elif evento.key == pygame.K_2:
                    dificultad_actual = 'MEDIO'
                    en_menu = False
                    en_menu_eleccion = False
                    reiniciar_juego()
                elif evento.key == pygame.K_3:
                    dificultad_actual = 'DIFICIL'
                    en_menu = False
                    en_menu_eleccion = False
                    reiniciar_juego()
                elif evento.key == pygame.K_ESCAPE:
                    en_menu_eleccion = False
                    
            elif game_over:
                # Pantalla de game over
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                elif evento.key == pygame.K_ESCAPE:
                    en_menu = True
                    en_menu_eleccion = False
                    game_over = False
    return True

def ejecutar_juego():
    """Función principal que ejecuta el bucle del juego"""
    global jugador
    
    inicializar_pygame()
    
    corriendo = True
    
    while corriendo:
        corriendo = manejar_eventos()
        
        if en_menu and not en_menu_eleccion:
            dibujar_menu()
        elif en_menu_eleccion:
            dibujar_menu_eleccion()
        else:
            teclas = pygame.key.get_pressed()
            actualizar_juego(teclas)
            dibujar_juego()
        
        pygame.display.flip()
        reloj.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    ejecutar_juego()