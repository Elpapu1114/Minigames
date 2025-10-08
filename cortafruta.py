import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 1000
ALTO = 700
FPS = 60
GRAVEDAD = 0.5

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 50)
AZUL = (50, 50, 255)
AMARILLO = (255, 255, 50)
NARANJA = (255, 165, 0)
ROSA = (255, 192, 203)
MARRON = (139, 69, 19)
GRIS = (128, 128, 128)
GRIS_OSCURO = (64, 64, 64)

# Colores de frutas
COLORES_FRUTAS = [ROJO, VERDE, AMARILLO, NARANJA, ROSA]

# Variables globales
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fruit ninja - Corta Frutas")
reloj = pygame.time.Clock()
fuente_grande = pygame.font.Font(None, 48)
fuente_mediana = pygame.font.Font(None, 32)
fuente_pequeña = pygame.font.Font(None, 24)

# Estado del juego
estado_juego = "menu"  # "menu", "juego", "game_over"
puntuacion = 0
vidas = 3
tiempo_spawn = 0
frutas = []
bombas = []
cortes = []
particulas = []
trail_mouse = []
tiempo_juego = 0  # Contador de tiempo para dificultad progresiva

class Fruta:
    def __init__(self, x, y, velocidad_x, velocidad_y, color, tamaño):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.color = color
        self.tamaño = tamaño
        self.cortada = False
        self.tiempo_corte = 0
        self.mitades = []
    
    def actualizar(self):
        if not self.cortada:
            self.x += self.velocidad_x
            self.y += self.velocidad_y
            self.velocidad_y += GRAVEDAD
        else:
            # Animar las mitades cortadas
            for mitad in self.mitades:
                mitad['x'] += mitad['vx']
                mitad['y'] += mitad['vy']
                mitad['vy'] += GRAVEDAD
            self.tiempo_corte += 1
    
    def dibujar(self, pantalla):
        if not self.cortada:
            # Dibujar fruta completa con efecto 3D
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.tamaño)
            # Brillo
            pygame.draw.circle(pantalla, tuple(min(255, c + 50) for c in self.color), 
                             (int(self.x - self.tamaño//3), int(self.y - self.tamaño//3)), self.tamaño//3)
        else:
            # Dibujar mitades cortadas
            for mitad in self.mitades:
                pygame.draw.circle(pantalla, self.color, (int(mitad['x']), int(mitad['y'])), self.tamaño//2)
    
    def cortar(self, pos_corte):
        if not self.cortada:
            self.cortada = True
            # Crear dos mitades que se separan
            self.mitades = [
                {'x': self.x - 5, 'y': self.y, 'vx': random.uniform(-5, -2), 'vy': random.uniform(-8, -5)},
                {'x': self.x + 5, 'y': self.y, 'vx': random.uniform(2, 5), 'vy': random.uniform(-8, -5)}
            ]
            crear_particulas(self.x, self.y, self.color)
            return True
        return False
    
    def en_pantalla(self):
        return -50 < self.x < ANCHO + 50 and self.y < ALTO + 100

class Bomba:
    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.explotada = False
        self.tiempo_explosion = 0
    
    def actualizar(self):
        if not self.explotada:
            self.x += self.velocidad_x
            self.y += self.velocidad_y
            self.velocidad_y += GRAVEDAD
        else:
            self.tiempo_explosion += 1
    
    def dibujar(self, pantalla):
        if not self.explotada:
            # Dibujar bomba
            pygame.draw.circle(pantalla, NEGRO, (int(self.x), int(self.y)), 25)
            pygame.draw.circle(pantalla, GRIS_OSCURO, (int(self.x), int(self.y)), 20)
            # Mecha
            pygame.draw.line(pantalla, MARRON, (int(self.x), int(self.y - 25)), 
                           (int(self.x - 10), int(self.y - 35)), 3)
            # Chispa en la mecha
            if random.randint(0, 10) > 7:
                pygame.draw.circle(pantalla, AMARILLO, (int(self.x - 10), int(self.y - 35)), 3)
        else:
            # Dibujar explosión
            if self.tiempo_explosion < 30:
                radio = self.tiempo_explosion * 3
                pygame.draw.circle(pantalla, AMARILLO, (int(self.x), int(self.y)), radio)
                pygame.draw.circle(pantalla, NARANJA, (int(self.x), int(self.y)), radio // 2)
    
    def explotar(self):
        if not self.explotada:
            self.explotada = True
            crear_particulas_explosion(self.x, self.y)
            return True
        return False
    
    def en_pantalla(self):
        return -50 < self.x < ANCHO + 50 and self.y < ALTO + 100

class Particula:
    def __init__(self, x, y, vx, vy, color, vida):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.vida = vida
        self.vida_max = vida
    
    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravedad ligera
        self.vida -= 1
    
    def dibujar(self, pantalla):
        if self.vida > 0:
            alpha = int(255 * (self.vida / self.vida_max))
            color_con_alpha = (*self.color[:3], alpha)
            tamaño = max(1, int(3 * (self.vida / self.vida_max)))
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), tamaño)
    
    def esta_viva(self):
        return self.vida > 0

def crear_particulas(x, y, color):
    """Crea partículas cuando se corta una fruta"""
    for _ in range(15):
        vx = random.uniform(-8, 8)
        vy = random.uniform(-12, -3)
        particula = Particula(x, y, vx, vy, color, 30)
        particulas.append(particula)

def crear_particulas_explosion(x, y):
    """Crea partículas de explosión"""
    for _ in range(25):
        vx = random.uniform(-15, 15)
        vy = random.uniform(-15, 15)
        color = random.choice([AMARILLO, NARANJA, ROJO])
        particula = Particula(x, y, vx, vy, color, 40)
        particulas.append(particula)

def generar_fruta():
    """Genera una nueva fruta desde abajo"""
    # Generar desde los lados con trayectoria hacia el centro
    lado = random.choice(['izquierda', 'derecha'])
    
    if lado == 'izquierda':
        x = random.randint(0, 100)
        # Ángulo hacia arriba y derecha (hacia el centro)
        angulo = random.uniform(-60, -120)
    else:
        x = random.randint(ANCHO - 100, ANCHO)
        # Ángulo hacia arriba y izquierda (hacia el centro)
        angulo = random.uniform(-60, -120)
    
    y = ALTO + 20  # Desde abajo de la pantalla
    
    velocidad = random.uniform(15, 22)
    velocidad_x = velocidad * math.cos(math.radians(angulo))
    velocidad_y = velocidad * math.sin(math.radians(angulo))
    
    # Ajustar velocidad_x según el lado para ir hacia el centro
    if lado == 'izquierda':
        velocidad_x = abs(velocidad_x)  # Asegurar que va hacia la derecha
    else:
        velocidad_x = -abs(velocidad_x)  # Asegurar que va hacia la izquierda
    
    color = random.choice(COLORES_FRUTAS)
    tamaño = random.randint(20, 35)
    return Fruta(x, y, velocidad_x, velocidad_y, color, tamaño)

def generar_bomba():
    """Genera una nueva bomba desde abajo"""
    # Generar desde los lados con trayectoria hacia el centro
    lado = random.choice(['izquierda', 'derecha'])
    
    if lado == 'izquierda':
        x = random.randint(0, 100)
        angulo = random.uniform(-60, -120)
    else:
        x = random.randint(ANCHO - 100, ANCHO)
        angulo = random.uniform(-60, -120)
    
    y = ALTO + 20  # Desde abajo de la pantalla
    
    velocidad = random.uniform(15, 22)
    velocidad_x = velocidad * math.cos(math.radians(angulo))
    velocidad_y = velocidad * math.sin(math.radians(angulo))
    
    # Ajustar velocidad_x según el lado para ir hacia el centro
    if lado == 'izquierda':
        velocidad_x = abs(velocidad_x)  # Asegurar que va hacia la derecha
    else:
        velocidad_x = -abs(velocidad_x)  # Asegurar que va hacia la izquierda
    
    return Bomba(x, y, velocidad_x, velocidad_y)

def calcular_intervalo_spawn():
    """Calcula el intervalo de spawn basado en el tiempo de juego"""
    # Empieza en 60 frames (1 segundo) y disminuye hasta 20 frames (0.33 segundos)
    tiempo_segundos = tiempo_juego / FPS
    intervalo_base = 60
    intervalo_minimo = 20
    
    # Reduce el intervalo 2 frames cada 5 segundos
    reduccion = (tiempo_segundos // 5) * 2
    intervalo = max(intervalo_minimo, intervalo_base - reduccion)
    
    return int(intervalo)

def detectar_corte_fruta(pos_mouse, fruta):
    """Detecta si el mouse está cerca de una fruta para cortarla"""
    distancia = math.sqrt((pos_mouse[0] - fruta.x)**2 + (pos_mouse[1] - fruta.y)**2)
    return distancia < fruta.tamaño + 10

def detectar_corte_bomba(pos_mouse, bomba):
    """Detecta si el mouse está cerca de una bomba"""
    distancia = math.sqrt((pos_mouse[0] - bomba.x)**2 + (pos_mouse[1] - bomba.y)**2)
    return distancia < 35

def dibujar_menu():
    """Dibuja el menú principal"""
    # Fondo gradiente
    for y in range(ALTO):
        color = (20 + y//10, 30 + y//15, 50 + y//8)
        pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))
    
    # Título con efecto
    titulo = fuente_grande.render("CORTA FRUTAS", True, AMARILLO)
    rect_titulo = titulo.get_rect(center=(ANCHO//2, 150))
    pantalla.blit(titulo, rect_titulo)
    
    # Subtítulo
    subtitulo = fuente_mediana.render("Estilo Fruit Ninja", True, BLANCO)
    rect_subtitulo = subtitulo.get_rect(center=(ANCHO//2, 200))
    pantalla.blit(subtitulo, rect_subtitulo)
    
    # Instrucciones
    instrucciones = [
        "Arrastra el mouse para cortar frutas",
        "¡Evita las bombas! Una bomba = Game Over",
        "Tienes 3 vidas (perdes 1 si dejas caer frutas)",
        "La dificultad aumenta con el tiempo",
        "",
        "Presiona ESPACIO para comenzar"
    ]
    
    y_inicio = 280
    for i, linea in enumerate(instrucciones):
        if linea:
            color = VERDE if "frutas" in linea else ROJO if "bombas" in linea else NARANJA if "dificultad" in linea else BLANCO
            texto = fuente_pequeña.render(linea, True, color)
            rect_texto = texto.get_rect(center=(ANCHO//2, y_inicio + i*30))
            pantalla.blit(texto, rect_texto)
    
    # Dibujar algunas frutas decorativas
    frutas_deco = [(200, 400, ROJO), (300, 450, VERDE), (700, 400, AMARILLO), (800, 450, NARANJA)]
    for x, y, color in frutas_deco:
        pygame.draw.circle(pantalla, color, (x, y), 25)
        pygame.draw.circle(pantalla, tuple(min(255, c + 50) for c in color), (x - 8, y - 8), 8)

def dibujar_hud():
    """Dibuja la interfaz de usuario"""
    # Puntuación
    texto_puntos = fuente_mediana.render(f"Puntos: {puntuacion}", True, AMARILLO)
    pantalla.blit(texto_puntos, (20, 20))
    
    # Vidas
    texto_vidas = fuente_mediana.render(f"Vidas: {vidas}", True, ROJO)
    pantalla.blit(texto_vidas, (ANCHO - 150, 20))
    
    # Tiempo de juego
    tiempo_seg = tiempo_juego // FPS
    texto_tiempo = fuente_pequeña.render(f"Tiempo: {tiempo_seg}s", True, BLANCO)
    pantalla.blit(texto_tiempo, (ANCHO//2 - 50, 20))
    
    # Dibujar corazones para las vidas
    for i in range(vidas):
        x = ANCHO - 100 + i * 25
        pygame.draw.circle(pantalla, ROJO, (x, 60), 8)
        pygame.draw.circle(pantalla, ROJO, (x + 8, 60), 8)
        pygame.draw.polygon(pantalla, ROJO, [(x - 8, 65), (x + 4, 80), (x + 16, 65)])

def dibujar_trail_mouse():
    """Dibuja el rastro del mouse"""
    for i, pos in enumerate(trail_mouse):
        if i > 0:
            alpha = int(255 * (i / len(trail_mouse)))
            grosor = max(1, i // 2)
            if i < len(trail_mouse) - 1:
                pygame.draw.line(pantalla, (255, 255, 255), pos, trail_mouse[i], grosor)

def dibujar_juego():
    """Dibuja el juego principal"""
    # Fondo
    for y in range(ALTO):
        color = (10 + y//20, 20 + y//25, 40 + y//15)
        pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))
    
    # Dibujar rastro del mouse
    dibujar_trail_mouse()
    
    # Dibujar frutas
    for fruta in frutas:
        fruta.dibujar(pantalla)
    
    # Dibujar bombas
    for bomba in bombas:
        bomba.dibujar(pantalla)
    
    # Dibujar partículas
    for particula in particulas:
        particula.dibujar(pantalla)
    
    # Dibujar HUD
    dibujar_hud()

def dibujar_game_over():
    """Dibuja la pantalla de game over"""
    # Fondo oscuro
    pantalla.fill((20, 20, 20))
    
    # Título
    titulo = fuente_grande.render("GAME OVER", True, ROJO)
    rect_titulo = titulo.get_rect(center=(ANCHO//2, 200))
    pantalla.blit(titulo, rect_titulo)
    
    # Puntuación final
    puntos_finales = fuente_mediana.render(f"Puntuación Final: {puntuacion}", True, AMARILLO)
    rect_puntos = puntos_finales.get_rect(center=(ANCHO//2, 280))
    pantalla.blit(puntos_finales, rect_puntos)
    
    # Tiempo sobrevivido
    tiempo_final = tiempo_juego // FPS
    tiempo_texto = fuente_mediana.render(f"Tiempo: {tiempo_final} segundos", True, VERDE)
    rect_tiempo = tiempo_texto.get_rect(center=(ANCHO//2, 320))
    pantalla.blit(tiempo_texto, rect_tiempo)
    
    # Opciones
    opciones = [
        "Presiona ESPACIO para jugar de nuevo",
        "Presiona ESC para volver al menú"
    ]
    
    for i, opcion in enumerate(opciones):
        texto_opcion = fuente_pequeña.render(opcion, True, BLANCO)
        rect_opcion = texto_opcion.get_rect(center=(ANCHO//2, 380 + i*30))
        pantalla.blit(texto_opcion, rect_opcion)

def reiniciar_juego():
    """Reinicia el juego"""
    global puntuacion, vidas, tiempo_spawn, frutas, bombas, particulas, trail_mouse, tiempo_juego
    puntuacion = 0
    vidas = 3
    tiempo_spawn = 0
    tiempo_juego = 0
    frutas.clear()
    bombas.clear()
    particulas.clear()
    trail_mouse.clear()

def manejar_eventos():
    """Maneja todos los eventos del juego"""
    global estado_juego, trail_mouse
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if estado_juego == "menu":
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = "juego"
            
            elif estado_juego == "game_over":
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = "juego"
                elif evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
            
            elif estado_juego == "juego":
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"
    
    # Actualizar rastro del mouse
    if pygame.mouse.get_pressed()[0] and estado_juego == "juego":
        pos_mouse = pygame.mouse.get_pos()
        trail_mouse.append(pos_mouse)
        if len(trail_mouse) > 15:
            trail_mouse.pop(0)
    else:
        trail_mouse.clear()

def actualizar_juego():
    """Actualiza la lógica del juego"""
    global tiempo_spawn, puntuacion, vidas, estado_juego, tiempo_juego
    
    if estado_juego != "juego":
        return
    
    # Incrementar contador de tiempo
    tiempo_juego += 1
    
    # Calcular intervalo de spawn dinámico
    intervalo_spawn = calcular_intervalo_spawn()
    
    # Generar nuevas frutas y bombas
    tiempo_spawn += 1
    if tiempo_spawn > intervalo_spawn:
        tiempo_spawn = 0
        if random.randint(0, 100) < 80:  # 80% probabilidad de fruta
            frutas.append(generar_fruta())
        else:  # 20% probabilidad de bomba
            bombas.append(generar_bomba())
    
    # Actualizar frutas
    for fruta in frutas[:]:
        fruta.actualizar()
        if not fruta.en_pantalla() and (fruta.cortada or fruta.y > ALTO):
            if not fruta.cortada and fruta.y > ALTO:
                # Fruta cayó sin ser cortada
                vidas -= 1
                if vidas <= 0:
                    estado_juego = "game_over"
            frutas.remove(fruta)
    
    # Actualizar bombas
    for bomba in bombas[:]:
        bomba.actualizar()
        if not bomba.en_pantalla():
            bombas.remove(bomba)
    
    # Actualizar partículas
    for particula in particulas[:]:
        particula.actualizar()
        if not particula.esta_viva():
            particulas.remove(particula)
    
    # Detectar cortes con el mouse
    if pygame.mouse.get_pressed()[0]:
        pos_mouse = pygame.mouse.get_pos()
        
        # Cortar frutas
        for fruta in frutas:
            if not fruta.cortada and detectar_corte_fruta(pos_mouse, fruta):
                if fruta.cortar(pos_mouse):
                    puntuacion += 10
        
        # Detectar bombas
        for bomba in bombas:
            if not bomba.explotada and detectar_corte_bomba(pos_mouse, bomba):
                if bomba.explotar():
                    # Tocar una bomba termina el juego inmediatamente
                    vidas = 0
                    estado_juego = "game_over"

def ejecutar_juego():
    """Bucle principal del juego"""
    ejecutando = True
    
    while ejecutando:
        # Manejar eventos
        manejar_eventos()
        
        # Actualizar juego
        actualizar_juego()
        
        # Dibujar según el estado
        if estado_juego == "menu":
            dibujar_menu()
        elif estado_juego == "juego":
            dibujar_juego()
        elif estado_juego == "game_over":
            dibujar_game_over()
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    ejecutar_juego()