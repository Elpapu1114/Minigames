import pygame
import sys
import random
import math

pygame.init()

ANCHO = 1000
ALTO = 700
FPS = 60
GRAVEDAD = 0.5

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

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Corta Frutas - Fruit Ninja Style")
reloj = pygame.time.Clock()
fuente_grande = pygame.font.Font(None, 48)
fuente_mediana = pygame.font.Font(None, 32)
fuente_pequeña = pygame.font.Font(None, 24)

try:
    bg_menu = pygame.image.load("image/fondo_menu_ninja_fruit.png")
    bg_menu = pygame.transform.scale(bg_menu, (ANCHO, ALTO))
    print("Fondo de menú cargado correctamente")
except Exception as e:
    print(f"Error al cargar fondo de menú: {e}")
    bg_menu = None

try:
    bg_game = pygame.image.load("image/fondo_ninja_fruit.png")
    bg_game = pygame.transform.scale(bg_game, (ANCHO, ALTO))
    print("Fondo de juego cargado correctamente")
except Exception as e:
    print(f"Error al cargar fondo de juego: {e}")
    bg_game = None

try:
    bg_gameover = pygame.image.load("image/fondo_game_over_ninja_fruit.png")
    bg_gameover = pygame.transform.scale(bg_gameover, (ANCHO, ALTO))
    print("Fondo de game over cargado correctamente")
except Exception as e:
    print(f"Error al cargar fondo de game over: {e}")
    bg_gameover = None

imagenes_frutas = {}
frutas_nombres = ["banana", "manzanafinal", "sandia", "anana"]

for fruta in frutas_nombres:
    try:
        img = pygame.image.load(f"image/{fruta}.png")
        img = pygame.transform.scale(img, (80, 80))
        imagenes_frutas[fruta] = img
    except:
        print(f"No se pudo cargar la imagen: {fruta}.png")
        imagenes_frutas[fruta] = None

estado_juego = "menu" 
puntuacion = 0
vidas = 3
tiempo_spawn = 0
frutas = []
bombas = []
cortes = []
particulas = []
trail_mouse = []
tiempo_juego = 0

class Fruta:
    def __init__(self, x, y, velocidad_x, velocidad_y, tipo_fruta):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.tipo_fruta = tipo_fruta
        self.imagen = imagenes_frutas[tipo_fruta]
        self.cortada = False
        self.tiempo_corte = 0
        self.mitades = []
        self.angulo = 0
        self.velocidad_rotacion = random.uniform(-5, 5)
        self.linea_corte = None
    
    def actualizar(self):
        if not self.cortada:
            self.x += self.velocidad_x
            self.y += self.velocidad_y
            self.velocidad_y += GRAVEDAD
            self.angulo += self.velocidad_rotacion
        else:
            for mitad in self.mitades:
                mitad['x'] += mitad['vx']
                mitad['y'] += mitad['vy']
                mitad['vy'] += GRAVEDAD
                mitad['angulo'] += mitad['rot']
            self.tiempo_corte += 1
    
    def dibujar(self, pantalla):
        if self.imagen is None:
            pygame.draw.circle(pantalla, ROJO, (int(self.x), int(self.y)), 30)
            return
        
        if not self.cortada:
            img_rotada = pygame.transform.rotate(self.imagen, self.angulo)
            rect = img_rotada.get_rect(center=(int(self.x), int(self.y)))
            pantalla.blit(img_rotada, rect)
        else:
            if self.linea_corte:
                for mitad in self.mitades:
                    img_rotada = pygame.transform.rotate(mitad['surf'], mitad['angulo'])
                    rect = img_rotada.get_rect(center=(int(mitad['x']), int(mitad['y'])))
                    pantalla.blit(img_rotada, rect)
    
    def cortar(self, pos_inicio, pos_fin):
        if not self.cortada and self.imagen:
            self.cortada = True

            dx = pos_fin[0] - pos_inicio[0]
            dy = pos_fin[1] - pos_inicio[1]
            angulo_corte = math.atan2(dy, dx)

            self.linea_corte = {
                'inicio': (pos_inicio[0] - self.x, pos_inicio[1] - self.y),
                'fin': (pos_fin[0] - self.x, pos_fin[1] - self.y),
                'angulo': angulo_corte
            }

            img_original = self.imagen.copy()
            ancho, alto = img_original.get_size()

            mitad1 = img_original.copy()
            mitad2 = img_original.copy()

            for x in range(ancho):
                for y in range(alto):
                    rel_x = x - ancho/2
                    rel_y = y - alto/2
                    
                    cross = rel_x * math.sin(angulo_corte) - rel_y * math.cos(angulo_corte)
                    
                    if cross < 0:
                        color = mitad2.get_at((x, y))
                        mitad2.set_at((x, y), (color[0], color[1], color[2], 0))
                    else:
                        color = mitad1.get_at((x, y))
                        mitad1.set_at((x, y), (color[0], color[1], color[2], 0))

            velocidad_sep = 3
            vx1 = -velocidad_sep * math.sin(angulo_corte) + self.velocidad_x * 0.5
            vy1 = velocidad_sep * math.cos(angulo_corte) + random.uniform(-8, -5)
            vx2 = velocidad_sep * math.sin(angulo_corte) + self.velocidad_x * 0.5
            vy2 = -velocidad_sep * math.cos(angulo_corte) + random.uniform(-8, -5)
            
            self.mitades = [
                {
                    'x': self.x - 5, 
                    'y': self.y, 
                    'vx': vx1, 
                    'vy': vy1,
                    'surf': mitad1,
                    'angulo': self.angulo,
                    'rot': random.uniform(-10, -5)
                },
                {
                    'x': self.x + 5, 
                    'y': self.y, 
                    'vx': vx2, 
                    'vy': vy2,
                    'surf': mitad2,
                    'angulo': self.angulo,
                    'rot': random.uniform(5, 10)
                }
            ]
            
            crear_particulas(self.x, self.y, AMARILLO)
            return True
        return False
    
    def en_pantalla(self):
        return -100 < self.x < ANCHO + 100 and self.y < ALTO + 150

class Bomba:
    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.explotada = False
        self.tiempo_explosion = 0
        self.angulo = 0
        self.velocidad_rotacion = random.uniform(-3, 3)
    
    def actualizar(self):
        if not self.explotada:
            self.x += self.velocidad_x
            self.y += self.velocidad_y
            self.velocidad_y += GRAVEDAD
            self.angulo += self.velocidad_rotacion
        else:
            self.tiempo_explosion += 1
    
    def dibujar(self, pantalla):
        if not self.explotada:
            pygame.draw.circle(pantalla, NEGRO, (int(self.x), int(self.y)), 25)
            pygame.draw.circle(pantalla, GRIS_OSCURO, (int(self.x), int(self.y)), 20)

            mecha_x = self.x + 10 * math.cos(math.radians(self.angulo))
            mecha_y = self.y - 25 + 10 * math.sin(math.radians(self.angulo))
            
            pygame.draw.line(pantalla, MARRON, (int(self.x), int(self.y - 25)), 
                           (int(mecha_x), int(mecha_y)), 3)

            if random.randint(0, 10) > 7:
                pygame.draw.circle(pantalla, AMARILLO, (int(mecha_x), int(mecha_y)), 3)
        else:
            if self.tiempo_explosion < 30:
                radio = self.tiempo_explosion * 3
                pygame.draw.circle(pantalla, AMARILLO, (int(self.x), int(self.y)), radio)
                pygame.draw.circle(pantalla, NARANJA, (int(self.x), int(self.y)), radio // 2)
                pygame.draw.circle(pantalla, ROJO, (int(self.x), int(self.y)), radio // 4)
    
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
        self.vy += 0.2
        self.vida -= 1
    
    def dibujar(self, pantalla):
        if self.vida > 0:
            tamaño = max(1, int(4 * (self.vida / self.vida_max)))
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), tamaño)
    
    def esta_viva(self):
        return self.vida > 0

def crear_particulas(x, y, color):
    for _ in range(20):
        vx = random.uniform(-10, 10)
        vy = random.uniform(-15, -5)
        particula = Particula(x, y, vx, vy, color, 35)
        particulas.append(particula)

def crear_particulas_explosion(x, y):
    for _ in range(30):
        vx = random.uniform(-18, 18)
        vy = random.uniform(-18, 18)
        color = random.choice([AMARILLO, NARANJA, ROJO])
        particula = Particula(x, y, vx, vy, color, 45)
        particulas.append(particula)

def generar_fruta():
    lado = random.choice(['izquierda', 'derecha'])
    
    if lado == 'izquierda':
        x = random.randint(0, 100)
        angulo = random.uniform(-60, -120)
    else:
        x = random.randint(ANCHO - 100, ANCHO)
        angulo = random.uniform(-60, -120)
    
    y = ALTO + 40
    
    velocidad = random.uniform(16, 23)
    velocidad_x = velocidad * math.cos(math.radians(angulo))
    velocidad_y = velocidad * math.sin(math.radians(angulo))
    
    if lado == 'izquierda':
        velocidad_x = abs(velocidad_x)
    else:
        velocidad_x = -abs(velocidad_x)
    
    tipo_fruta = random.choice(frutas_nombres)
    return Fruta(x, y, velocidad_x, velocidad_y, tipo_fruta)

def generar_bomba():
    lado = random.choice(['izquierda', 'derecha'])
    
    if lado == 'izquierda':
        x = random.randint(0, 100)
        angulo = random.uniform(-60, -120)
    else:
        x = random.randint(ANCHO - 100, ANCHO)
        angulo = random.uniform(-60, -120)
    
    y = ALTO + 40
    
    velocidad = random.uniform(16, 23)
    velocidad_x = velocidad * math.cos(math.radians(angulo))
    velocidad_y = velocidad * math.sin(math.radians(angulo))
    
    if lado == 'izquierda':
        velocidad_x = abs(velocidad_x)
    else:
        velocidad_x = -abs(velocidad_x)
    
    return Bomba(x, y, velocidad_x, velocidad_y)

def calcular_intervalo_spawn():
    tiempo_segundos = tiempo_juego / FPS
    intervalo_base = 60
    intervalo_minimo = 20
    reduccion = (tiempo_segundos // 5) * 2
    intervalo = max(intervalo_minimo, intervalo_base - reduccion)
    return int(intervalo)

def detectar_corte_fruta(pos_mouse, fruta):
    distancia = math.sqrt((pos_mouse[0] - fruta.x)**2 + (pos_mouse[1] - fruta.y)**2)
    return distancia < 50

def detectar_corte_bomba(pos_mouse, bomba):
    distancia = math.sqrt((pos_mouse[0] - bomba.x)**2 + (pos_mouse[1] - bomba.y)**2)
    return distancia < 35

def dibujar_menu():
    if bg_menu:
        pantalla.blit(bg_menu, (0, 0))
    else:
        for y in range(ALTO):
            color = (20 + y//10, 30 + y//15, 50 + y//8)
            pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))

def dibujar_hud():
    texto_puntos = fuente_mediana.render(f"Puntos: {puntuacion}", True, AMARILLO)
    pantalla.blit(texto_puntos, (20, 20))
    
    texto_vidas = fuente_mediana.render(f"Vidas: {vidas}", True, ROJO)
    pantalla.blit(texto_vidas, (ANCHO - 150, 20))
    
    tiempo_seg = tiempo_juego // FPS
    texto_tiempo = fuente_pequeña.render(f"Tiempo: {tiempo_seg}s", True, BLANCO)
    pantalla.blit(texto_tiempo, (ANCHO//2 - 50, 20))
    
    for i in range(vidas):
        x = ANCHO - 100 + i * 25
        pygame.draw.circle(pantalla, ROJO, (x, 60), 8)
        pygame.draw.circle(pantalla, ROJO, (x + 8, 60), 8)
        pygame.draw.polygon(pantalla, ROJO, [(x - 8, 65), (x + 4, 80), (x + 16, 65)])

def dibujar_trail_mouse():
    for i in range(len(trail_mouse) - 1):
        if i > 0:
            alpha = int(255 * (i / len(trail_mouse)))
            grosor = max(2, i // 2)
            pygame.draw.line(pantalla, (255, 255, 255), trail_mouse[i], trail_mouse[i + 1], grosor)

def dibujar_juego():
    if bg_game:
        pantalla.blit(bg_game, (0, 0))
    else:
        for y in range(ALTO):
            color = (10 + y//20, 20 + y//25, 40 + y//15)
            pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))
    
    dibujar_trail_mouse()
    
    for fruta in frutas:
        fruta.dibujar(pantalla)
    
    for bomba in bombas:
        bomba.dibujar(pantalla)
    
    for particula in particulas:
        particula.dibujar(pantalla)
    
    dibujar_hud()

def dibujar_game_over():
    if bg_gameover:
        pantalla.blit(bg_gameover, (0, 0))
    else:
        pantalla.fill((20, 20, 20))
        titulo = fuente_grande.render("GAME OVER", True, ROJO)
        rect_titulo = titulo.get_rect(center=(ANCHO//2, 200))
        pantalla.blit(titulo, rect_titulo)
        
        puntos_finales = fuente_mediana.render(f"Puntuación Final: {puntuacion}", True, AMARILLO)
        rect_puntos = puntos_finales.get_rect(center=(ANCHO//2, 280))
        pantalla.blit(puntos_finales, rect_puntos)
        
        tiempo_final = tiempo_juego // FPS
        tiempo_texto = fuente_mediana.render(f"Tiempo: {tiempo_final} segundos", True, VERDE)
        rect_tiempo = tiempo_texto.get_rect(center=(ANCHO//2, 320))
        pantalla.blit(tiempo_texto, rect_tiempo)
        
        opciones = [
            "Presiona ESPACIO para jugar de nuevo",
            "Presiona M para volver al menú",
            "Presiona ESC para salir"
        ]
        
        for i, opcion in enumerate(opciones):
            texto_opcion = fuente_pequeña.render(opcion, True, BLANCO)
            rect_opcion = texto_opcion.get_rect(center=(ANCHO//2, 380 + i*30))
            pantalla.blit(texto_opcion, rect_opcion)

def reiniciar_juego():
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
    global estado_juego, trail_mouse
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if estado_juego == "menu":
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = "juego"
            
            elif estado_juego == "game_over":
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()
                    estado_juego = "juego"
                elif evento.key == pygame.K_m:
                    estado_juego = "menu"
            
            elif estado_juego == "juego":
                if evento.key == pygame.K_p:
                    estado_juego = "menu"
    
    if pygame.mouse.get_pressed()[0] and estado_juego == "juego":
        pos_mouse = pygame.mouse.get_pos()
        trail_mouse.append(pos_mouse)
        if len(trail_mouse) > 20:
            trail_mouse.pop(0)
    else:
        trail_mouse.clear()

def actualizar_juego():
    global tiempo_spawn, puntuacion, vidas, estado_juego, tiempo_juego
    
    if estado_juego != "juego":
        return
    
    tiempo_juego += 1
    intervalo_spawn = calcular_intervalo_spawn()
    
    tiempo_spawn += 1
    if tiempo_spawn > intervalo_spawn:
        tiempo_spawn = 0
        if random.randint(0, 100) < 80:
            frutas.append(generar_fruta())
        else:
            bombas.append(generar_bomba())
    
    for fruta in frutas[:]:
        fruta.actualizar()
        if not fruta.en_pantalla() and (fruta.cortada or fruta.y > ALTO):
            if not fruta.cortada and fruta.y > ALTO:
                vidas -= 1
                if vidas <= 0:
                    estado_juego = "game_over"
            frutas.remove(fruta)
    
    for bomba in bombas[:]:
        bomba.actualizar()
        if not bomba.en_pantalla():
            bombas.remove(bomba)
    
    for particula in particulas[:]:
        particula.actualizar()
        if not particula.esta_viva():
            particulas.remove(particula)
    
    if pygame.mouse.get_pressed()[0] and len(trail_mouse) >= 2:
        pos_actual = pygame.mouse.get_pos()
        pos_anterior = trail_mouse[-2] if len(trail_mouse) >= 2 else trail_mouse[-1]
        
        for fruta in frutas:
            if not fruta.cortada and detectar_corte_fruta(pos_actual, fruta):
                if fruta.cortar(pos_anterior, pos_actual):
                    puntuacion += 10
        
        for bomba in bombas:
            if not bomba.explotada and detectar_corte_bomba(pos_actual, bomba):
                if bomba.explotar():
                    vidas = 0
                    estado_juego = "game_over"

def ejecutar_juego():
    ejecutando = True
    
    while ejecutando:
        manejar_eventos()
        actualizar_juego()
        
        if estado_juego == "menu":
            dibujar_menu()
        elif estado_juego == "juego":
            dibujar_juego()
        elif estado_juego == "game_over":
            dibujar_game_over()
        
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    ejecutar_juego()
