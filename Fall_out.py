import pygame
import sys
import random
import math

pygame.init()

from display_config import init_display

pygame.display.set_caption("Fall Out")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 215, 0)
VERDE = (34, 139, 34)

FPS = 60
ANCHO = 1280
ALTO = 720

# Inicializar pantalla con resolucion desde game_settings.json
pantalla, ANCHO, ALTO = init_display(default_w=ANCHO, default_h=ALTO, title="Fall Out")

def cargar_imagenes():
    imagenes = {}
    archivos = {
        'menu': 'image/menu_fall_out.png',
        'pelota': 'image/pelota_playa.png',
        'fondo': 'image/fondo_juego_fall_out.png',
        'cangrejo': 'image/cangrejo.png',
        'coco': 'image/coco.png',
        'game_over': 'image/game_over_fall_out.png'
    }
    
    errores = []
    for clave, archivo in archivos.items():
        try:
            imagenes[clave] = pygame.image.load(archivo)
            print(f"✓ Cargado: {archivo}")
        except pygame.error as e:
            errores.append(f"✗ No se encontró: {archivo}")
            print(f"✗ Error con {archivo}: {e}")
    
    if errores:
        print("\n⚠ ARCHIVOS FALTANTES:")
        for error in errores:
            print(error)
        print("\nAsegúrate de tener estos archivos en la carpeta 'image'.")
        pygame.quit()
        sys.exit()
    
    print("\n✓ Todas las imágenes cargadas correctamente\n")
    return imagenes

def menu_principal(pantalla, imagenes):
    menu_img = pygame.transform.scale(imagenes['menu'], (ANCHO, ALTO))
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pantalla.blit(menu_img, (0, 0))
        pygame.display.flip()

def cuenta_regresiva(pantalla):
    fuente = pygame.font.Font(None, 144)
    
    for i in range(3, 0, -1):
        pantalla.fill(NEGRO)
        
        texto = fuente.render(str(i), True, BLANCO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
        
        pygame.display.flip()
        pygame.time.wait(800)
    
    pantalla.fill(NEGRO)
    go_texto = fuente.render("¡VAMOS!", True, VERDE)
    pantalla.blit(go_texto, (ANCHO//2 - go_texto.get_width()//2, ALTO//2 - go_texto.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(600)

def pantalla_fin_juego(pantalla, imagenes):
    game_over_img = pygame.transform.scale(imagenes['game_over'], (ANCHO, ALTO))
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False
        
        pantalla.blit(game_over_img, (0, 0))
        pygame.display.flip()

def crear_obstaculo(imagenes, tamaño):
    x = random.randint(0, ANCHO - tamaño)
    y = random.randint(-ALTO, -tamaño)
    tipo = random.choice(['pelota', 'coco'])
    return {
        'rect': pygame.Rect(x, y, tamaño, tamaño),
        'tipo': tipo,
        'imagen': imagenes[tipo],
        'rotacion': 0
    }

def dibujar_obstaculo(pantalla, obstaculo):
    rect = obstaculo['rect']
    imagen = pygame.transform.scale(obstaculo['imagen'], (rect.width, rect.height))
    
    if obstaculo['rotacion'] != 0:
        imagen = pygame.transform.rotate(imagen, obstaculo['rotacion'])
        nuevo_rect = imagen.get_rect(center=rect.center)
        pantalla.blit(imagen, nuevo_rect)
    else:
        pantalla.blit(imagen, rect)

def dibujar_jugador(pantalla, x, y, ancho_jugador, alto_jugador, imagen_cangrejo):
    imagen_escalada = pygame.transform.scale(imagen_cangrejo, (ancho_jugador, alto_jugador))
    pantalla.blit(imagen_escalada, (int(x), int(y)))

def dibujar_fondo(pantalla, imagen_fondo):
    fondo_escalado = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
    pantalla.blit(fondo_escalado, (0, 0))

def ejecutar_juego(pantalla, record_actual, imagenes):
    reloj = pygame.time.Clock()
    
    ancho_jugador = ANCHO // 15
    alto_jugador = ALTO // 20
    velocidad_jugador = ANCHO / 2.5
    tamaño_obstaculo = ANCHO // 20
    velocidad_obstaculo_inicial = ALTO / 2
    num_obstaculos = 4
    
    jugador_x = ANCHO//2 - ancho_jugador//2
    jugador_y = ALTO - alto_jugador - 10
    
    obstaculos = []
    for _ in range(num_obstaculos):
        obstaculos.append(crear_obstaculo(imagenes, tamaño_obstaculo))
    
    puntuacion = 0
    tiempo_transcurrido = 0.0
    
    cuenta_regresiva(pantalla)
    
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
        if jugador_x + ancho_jugador > ANCHO:
            jugador_x = ANCHO - ancho_jugador
        
        factor_velocidad = 1.0 + tiempo_transcurrido / 20.0
        velocidad_actual = velocidad_obstaculo_inicial * factor_velocidad
        
        for obstaculo in obstaculos:
            obstaculo['rect'].y += velocidad_actual * dt
            obstaculo['rotacion'] += dt * 90
            
            if obstaculo['rect'].top > ALTO:
                nuevo_obstaculo = crear_obstaculo(imagenes, tamaño_obstaculo)
                obstaculo.update(nuevo_obstaculo)
        
        rect_jugador = pygame.Rect(int(jugador_x), int(jugador_y), ancho_jugador, alto_jugador)
        
        for obstaculo in obstaculos:
            if rect_jugador.colliderect(obstaculo['rect']):
                es_record = puntuacion > record_actual
                nuevo_record = max(puntuacion, record_actual)
                jugar_otra_vez = pantalla_fin_juego(pantalla, imagenes)
                return nuevo_record, jugar_otra_vez
        
        puntuacion += dt * 15 * factor_velocidad
        
        dibujar_fondo(pantalla, imagenes['fondo'])
        
        for obstaculo in obstaculos:
            dibujar_obstaculo(pantalla, obstaculo)
        
        dibujar_jugador(pantalla, jugador_x, jugador_y, ancho_jugador, alto_jugador, imagenes['cangrejo'])
        
        fuente_puntos = pygame.font.Font(None, 56)
        texto_puntos = fuente_puntos.render(f"Puntos: {int(puntuacion)}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
        
        if record_actual > 0:
            fuente_record = pygame.font.Font(None, 32)
            texto_record = fuente_record.render(f"Récord: {int(record_actual)}", True, AMARILLO)
            pantalla.blit(texto_record, (10, 70))
        
        nivel_texto = pygame.font.Font(None, 32).render(f"Velocidad: x{factor_velocidad:.1f}", True, VERDE)
        pantalla.blit(nivel_texto, (ANCHO - nivel_texto.get_width() - 10, 10))
        
        pygame.display.flip()

def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    imagenes = cargar_imagenes()
    menu_principal(pantalla, imagenes)
    
    record = 0
    
    while True:
        nuevo_record, continuar = ejecutar_juego(pantalla, record, imagenes)
        record = nuevo_record
        
        if not continuar:
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()