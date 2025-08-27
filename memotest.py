import pygame
import sys
import random
import time
import math

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800,600))

pygame.display.set_caption("Memotest - Pygame")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (64, 64, 64)
AMARILLO = (255, 215, 0)
VERDE = (34, 139, 34)
ROJO = (220, 20, 60)
AZUL = (30, 144, 255)
MORADO = (138, 43, 226)
NARANJA = (255, 140, 0)
ROSA = (255, 20, 147)
CIAN = (0, 206, 209)
LIMA = (50, 205, 50)
DORADO = (255, 215, 0)

FPS = 60

def crear_particulas(x, y, color):
    particulas = []
    for _ in range(15):
        angulo = random.uniform(0, 2 * math.pi)
        velocidad = random.uniform(2, 6)
        particulas.append({
            'x': x,
            'y': y,
            'vx': math.cos(angulo) * velocidad,
            'vy': math.sin(angulo) * velocidad,
            'vida': 1.0,
            'color': color
        })
    return particulas

def actualizar_particulas(particulas, dt):
    for particula in particulas[:]:
        particula['x'] += particula['vx'] * dt * 60
        particula['y'] += particula['vy'] * dt * 60
        particula['vy'] += 5 * dt
        particula['vida'] -= dt * 2
        if particula['vida'] <= 0:
            particulas.remove(particula)

def dibujar_particulas(pantalla, particulas):
    for particula in particulas:
        tamaño = max(1, int(particula['vida'] * 4))
        try:
            pos = (int(particula['x']), int(particula['y']))
            pygame.draw.circle(pantalla, particula['color'], pos, tamaño)
        except:
            pass

def crear_carta(x, y, ancho, alto, color, simbolo):
    return {
        'rectangulo': pygame.Rect(x, y, ancho, alto),
        'color': color,
        'simbolo': simbolo,
        'volteada': False,
        'emparejada': False,
        'hover': False,
        'progreso_volteo': 0.0,
        'escala': 1.0,
        'intensidad_brillo': 0.0
    }

def actualizar_carta(carta, dt):
    volteo_objetivo = 1.0 if (carta['volteada'] or carta['emparejada']) else 0.0
    if carta['progreso_volteo'] != volteo_objetivo:
        velocidad = 8.0
        if carta['progreso_volteo'] < volteo_objetivo:
            carta['progreso_volteo'] = min(volteo_objetivo, carta['progreso_volteo'] + velocidad * dt)
        else:
            carta['progreso_volteo'] = max(volteo_objetivo, carta['progreso_volteo'] - velocidad * dt)
    
    escala_objetivo = 1.1 if carta['hover'] and not carta['emparejada'] else 1.0
    if carta['escala'] != escala_objetivo:
        velocidad_escala = 5.0
        if carta['escala'] < escala_objetivo:
            carta['escala'] = min(escala_objetivo, carta['escala'] + velocidad_escala * dt)
        else:
            carta['escala'] = max(escala_objetivo, carta['escala'] - velocidad_escala * dt)
    
    if carta['emparejada']:
        carta['intensidad_brillo'] = (math.sin(time.time() * 3) + 1) / 2

def dibujar_carta(pantalla, carta):
    centro_x = carta['rectangulo'].centerx
    centro_y = carta['rectangulo'].centery
    ancho_escalado = int(carta['rectangulo'].width * carta['escala'])
    alto_escalado = int(carta['rectangulo'].height * carta['escala'])
    rect_escalado = pygame.Rect(0, 0, ancho_escalado, alto_escalado)
    rect_escalado.center = (centro_x, centro_y)
    
    if carta['emparejada'] and carta['intensidad_brillo'] > 0:
        color_brillo = tuple(min(255, c + int(50 * carta['intensidad_brillo'])) for c in carta['color'])
        rect_brillo = rect_escalado.inflate(6, 6)
        pygame.draw.rect(pantalla, color_brillo, rect_brillo, border_radius=8)
    
    rect_sombra = rect_escalado.copy()
    rect_sombra.x += 3
    rect_sombra.y += 3
    pygame.draw.rect(pantalla, (50, 50, 50), rect_sombra, border_radius=8)
    
    if carta['progreso_volteo'] > 0.5:
        color_carta = carta['color']
        color_borde = BLANCO
    else:
        color_carta = GRIS_OSCURO if not carta['hover'] else GRIS
        color_borde = GRIS_CLARO
    
    pygame.draw.rect(pantalla, color_carta, rect_escalado, border_radius=8)
    pygame.draw.rect(pantalla, color_borde, rect_escalado, width=3, border_radius=8)
    
    if carta['progreso_volteo'] > 0.5 and carta['simbolo']:
        tamaño_fuente = min(ancho_escalado, alto_escalado) // 3
        fuente = pygame.font.Font(None, tamaño_fuente)
        texto = fuente.render(carta['simbolo'], True, BLANCO)
        rect_texto = texto.get_rect(center=rect_escalado.center)
        pantalla.blit(texto, rect_texto)
    
    elif carta['progreso_volteo'] <= 0.5:
        color_patron = tuple(min(255, c + 30) for c in color_carta)
        for i in range(3):
            for j in range(3):
                punto_x = rect_escalado.x + (i + 1) * rect_escalado.width // 4
                punto_y = rect_escalado.y + (j + 1) * rect_escalado.height // 4
                pygame.draw.circle(pantalla, color_patron, (punto_x, punto_y), 3)

def menu_resolucion(pantalla):
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_opciones = pygame.font.Font(None, 36)
    
    while True:
        for y in range(pantalla.get_height()):
            color = (0, 0, min(100, y // 6))
            pygame.draw.line(pantalla, color, (0, y), (pantalla.get_width(), y))
        
        titulo = fuente_titulo.render("MEMOTEST PRO", True, DORADO)
        rect_titulo = titulo.get_rect(center=(pantalla.get_width()//2, 100))
        
        sombra = fuente_titulo.render("MEMOTEST PRO", True, GRIS_OSCURO)
        rect_sombra = sombra.get_rect(center=(rect_titulo.centerx + 3, rect_titulo.centery + 3))
        pantalla.blit(sombra, rect_sombra)
        pantalla.blit(titulo, rect_titulo)
        
        opciones = [
            "Elige resolución:",
            "",
            "1) 800 x 600",
            "2) 960 x 720", 
            "3) 1024 x 768",
            "",
            "Presiona 1, 2 o 3"
        ]
        
        for i, opcion in enumerate(opciones):
            if opcion:
                color = AMARILLO if opcion.startswith(("1)", "2)", "3)")) else BLANCO
                texto = fuente_opciones.render(opcion, True, color)
                rect_texto = texto.get_rect(center=(pantalla.get_width()//2, 200 + i*40))
                pantalla.blit(texto, rect_texto)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.unicode == "1": return 800, 600
                if evento.unicode == "2": return 960, 720
                if evento.unicode == "3": return 1024, 768

def menu_modo(pantalla):
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_opciones = pygame.font.Font(None, 36)
    
    while True:
        for y in range(pantalla.get_height()):
            color = (0, min(100, y // 6), 0)
            pygame.draw.line(pantalla, color, (0, y), (pantalla.get_width(), y))
        
        titulo = fuente_titulo.render("SELECCIONAR MODO", True, LIMA)
        rect_titulo = titulo.get_rect(center=(pantalla.get_width()//2, 100))
        
        sombra = fuente_titulo.render("SELECCIONAR MODO", True, GRIS_OSCURO)
        rect_sombra = sombra.get_rect(center=(rect_titulo.centerx + 2, rect_titulo.centery + 2))
        pantalla.blit(sombra, rect_sombra)
        pantalla.blit(titulo, rect_titulo)
        
        opciones = [
            "Elige modo de juego:",
            "",
            "1) Un Jugador",
            "2) Dos Jugadores",
            "",
            "Presiona 1 o 2"
        ]
        
        for i, opcion in enumerate(opciones):
            if opcion:
                color = CIAN if opcion.startswith(("1)", "2)")) else BLANCO
                texto = fuente_opciones.render(opcion, True, color)
                rect_texto = texto.get_rect(center=(pantalla.get_width()//2, 180 + i*40))
                pantalla.blit(texto, rect_texto)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.unicode in ("1", "2"):
                    return int(evento.unicode)

def crear_tablero(ancho, alto, filas=4, columnas=5):
    total_cartas = filas * columnas
    
    datos_cartas = [
        (ROJO, "♥"), (VERDE, "♠"), (AZUL, "♦"), (MORADO, "♣"),
        (NARANJA, "★"), (ROSA, "●"), (CIAN, "▲"), (LIMA, "■"),
        (DORADO, "♪"), (BLANCO, "◆")
    ]
    
    pares = (datos_cartas * 2)[:total_cartas]
    random.shuffle(pares)
    
    margen = 20
    ancho_carta = min(120, (ancho - margen * (columnas + 1)) // columnas)
    alto_carta = min(150, (alto - 100 - margen * (filas + 1)) // filas)
    
    ancho_tablero = columnas * ancho_carta + (columnas - 1) * margen
    alto_tablero = filas * alto_carta + (filas - 1) * margen
    inicio_x = (ancho - ancho_tablero) // 2
    inicio_y = (alto - alto_tablero) // 2 - 25
    
    cartas = []
    indice = 0
    for f in range(filas):
        for c in range(columnas):
            x = inicio_x + c * (ancho_carta + margen)
            y = inicio_y + f * (alto_carta + margen)
            color, simbolo = pares[indice]
            cartas.append(crear_carta(x, y, ancho_carta, alto_carta, color, simbolo))
            indice += 1
    
    return cartas

def dibujar_interfaz(pantalla, ancho, alto, modo, puntos1, puntos2, turno, movimientos, tiempo_transcurrido):
    rect_interfaz = pygame.Rect(0, alto - 80, ancho, 80)
    pygame.draw.rect(pantalla, (20, 20, 40), rect_interfaz)
    pygame.draw.line(pantalla, BLANCO, (0, alto - 80), (ancho, alto - 80), 2)
    
    fuente = pygame.font.Font(None, 32)
    
    if modo == 1:
        texto_puntos = f"Puntos: {puntos1}"
        texto_movimientos = f"Movimientos: {movimientos}"
        texto_tiempo = f"Tiempo: {int(tiempo_transcurrido)}s"
        
        textos = [texto_puntos, texto_movimientos, texto_tiempo]
        espaciado = ancho // len(textos)
        
        for i, texto in enumerate(textos):
            renderizado = fuente.render(texto, True, BLANCO)
            x = espaciado * i + espaciado // 2 - renderizado.get_width() // 2
            pantalla.blit(renderizado, (x, alto - 50))
    else:
        texto_j1 = f"Jugador 1: {puntos1}"
        texto_j2 = f"Jugador 2: {puntos2}"
        texto_turno = f"Turno: Jugador {turno}"
        
        color1 = AMARILLO if turno == 1 else BLANCO
        j1_renderizado = fuente.render(texto_j1, True, color1)
        pantalla.blit(j1_renderizado, (20, alto - 50))
        
        color2 = AMARILLO if turno == 2 else BLANCO
        j2_renderizado = fuente.render(texto_j2, True, color2)
        pantalla.blit(j2_renderizado, (ancho - j2_renderizado.get_width() - 20, alto - 50))
        
        turno_renderizado = fuente.render(texto_turno, True, CIAN)
        turno_x = ancho // 2 - turno_renderizado.get_width() // 2
        pantalla.blit(turno_renderizado, (turno_x, alto - 50))

def ejecutar_juego(pantalla, ancho, alto, modo):
    reloj = pygame.time.Clock()
    
    filas, columnas = 4, 5
    cartas = crear_tablero(ancho, alto, filas, columnas)
    
    primera_carta = None
    segunda_carta = None
    verificando = False
    tiempo_verificacion = 0
    contador_emparejadas = 0
    movimientos = 0
    
    puntos1 = 0
    puntos2 = 0
    turno = 1
    
    todas_particulas = []
    tiempo_inicio = time.time()
    
    tiempo_vista_previa = 3.0
    inicio_vista_previa = time.time()
    for carta in cartas:
        carta['volteada'] = True
    
    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio
        
        if tiempo_actual - inicio_vista_previa > tiempo_vista_previa and tiempo_vista_previa > 0:
            for carta in cartas:
                if not carta['emparejada']:
                    carta['volteada'] = False
            tiempo_vista_previa = 0
        
        pos_raton = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and not verificando and tiempo_vista_previa == 0:
                for carta in cartas:
                    if carta['rectangulo'].collidepoint(pos_raton) and not carta['volteada'] and not carta['emparejada']:
                        carta['volteada'] = True
                        if primera_carta is None:
                            primera_carta = carta
                        elif segunda_carta is None:
                            segunda_carta = carta
                            verificando = True
                            tiempo_verificacion = tiempo_actual
                            movimientos += 1
                        break
        
        for carta in cartas:
            carta['hover'] = carta['rectangulo'].collidepoint(pos_raton) and not carta['volteada'] and not carta['emparejada'] and tiempo_vista_previa == 0
        
        if verificando and tiempo_actual - tiempo_verificacion > 1.0:
            if primera_carta['color'] == segunda_carta['color']:
                primera_carta['emparejada'] = True
                segunda_carta['emparejada'] = True
                contador_emparejadas += 2
                
                particulas1 = crear_particulas(primera_carta['rectangulo'].centerx, primera_carta['rectangulo'].centery, primera_carta['color'])
                particulas2 = crear_particulas(segunda_carta['rectangulo'].centerx, segunda_carta['rectangulo'].centery, segunda_carta['color'])
                todas_particulas.extend(particulas1)
                todas_particulas.extend(particulas2)
                
                if turno == 1:
                    puntos1 += 1
                else:
                    puntos2 += 1
            else:
                primera_carta['volteada'] = False
                segunda_carta['volteada'] = False
                if modo == 2:
                    turno = 2 if turno == 1 else 1
            
            primera_carta = None
            segunda_carta = None
            verificando = False
        
        for carta in cartas:
            actualizar_carta(carta, dt)
        
        actualizar_particulas(todas_particulas, dt)
        
        for y in range(alto - 80):
            intensidad = int(20 + 15 * math.sin(tiempo_transcurrido * 0.5 + y * 0.01))
            color = (intensidad, intensidad // 2, intensidad // 3)
            pygame.draw.line(pantalla, color, (0, y), (ancho, y))
        
        for carta in cartas:
            dibujar_carta(pantalla, carta)
        
        dibujar_particulas(pantalla, todas_particulas)
        
        dibujar_interfaz(pantalla, ancho, alto, modo, puntos1, puntos2, turno, movimientos, tiempo_transcurrido)
        
        if tiempo_vista_previa > 0:
            restante = tiempo_vista_previa - (tiempo_actual - inicio_vista_previa)
            if restante > 0:
                fuente = pygame.font.Font(None, 72)
                texto = f"Memoriza: {int(restante) + 1}"
                renderizado = fuente.render(texto, True, AMARILLO)
                rect_texto = renderizado.get_rect(center=(ancho//2, 50))
                
                sombra = fuente.render(texto, True, NEGRO)
                rect_sombra = sombra.get_rect(center=(rect_texto.centerx + 3, rect_texto.centery + 3))
                pantalla.blit(sombra, rect_sombra)
                pantalla.blit(renderizado, rect_texto)
        
        pygame.display.flip()
        
        if contador_emparejadas == len(cartas):
            pantalla.fill(NEGRO)
            
            particulas_victoria = []
            for i in range(20):
                x = random.randint(50, ancho-50)
                y = random.randint(50, alto//2)
                color = random.choice([ROJO, VERDE, AZUL, AMARILLO, MORADO, NARANJA])
                particulas_victoria.extend(crear_particulas(x, y, color))
            
            for _ in range(60):
                dt = reloj.tick(FPS) / 1000.0
                
                for y in range(alto):
                    intensidad = int(30 + 20 * math.sin(time.time() * 2 + y * 0.02))
                    color = (intensidad//3, intensidad//2, intensidad)
                    pygame.draw.line(pantalla, color, (0, y), (ancho, y))
                
                actualizar_particulas(particulas_victoria, dt)
                dibujar_particulas(pantalla, particulas_victoria)
                
                fuente_grande = pygame.font.Font(None, 96)
                fuente_pequeña = pygame.font.Font(None, 48)
                
                if modo == 1:
                    texto_victoria = "¡FELICITACIONES!"
                    texto_estadisticas = f"Completado en {movimientos} movimientos y {int(tiempo_transcurrido)}s"
                else:
                    if puntos1 > puntos2:
                        texto_victoria = "¡GANA JUGADOR 1!"
                    elif puntos2 > puntos1:
                        texto_victoria = "¡GANA JUGADOR 2!"
                    else:
                        texto_victoria = "¡EMPATE!"
                    texto_estadisticas = f"Jugador 1: {puntos1} - Jugador 2: {puntos2}"
                
                escala = 1.0 + 0.1 * math.sin(time.time() * 4)
                superficie_victoria = fuente_grande.render(texto_victoria, True, DORADO)
                ancho_victoria = int(superficie_victoria.get_width() * escala)
                alto_victoria = int(superficie_victoria.get_height() * escala)
                victoria_escalada = pygame.transform.scale(superficie_victoria, (ancho_victoria, alto_victoria))
                rect_victoria = victoria_escalada.get_rect(center=(ancho//2, alto//2 - 50))
                
                sombra = fuente_grande.render(texto_victoria, True, NEGRO)
                rect_sombra = sombra.get_rect(center=(rect_victoria.centerx + 4, rect_victoria.centery + 4))
                pantalla.blit(sombra, rect_sombra)
                pantalla.blit(victoria_escalada, rect_victoria)
                
                superficie_estadisticas = fuente_pequeña.render(texto_estadisticas, True, BLANCO)
                rect_estadisticas = superficie_estadisticas.get_rect(center=(ancho//2, alto//2 + 50))
                pantalla.blit(superficie_estadisticas, rect_estadisticas)
                
                pygame.display.flip()
            
            pygame.time.wait(2000)
            return

def principal():
    pantalla_temporal = pygame.display.set_mode((800, 600))
    ancho, alto = menu_resolucion(pantalla_temporal)
    pantalla = pygame.display.set_mode((ancho, alto))
    
    while True:
        modo = menu_modo(pantalla)
        ejecutar_juego(pantalla, ancho, alto, modo)
        
        fuente = pygame.font.Font(None, 48)
        fuente_pequeña = pygame.font.Font(None, 36)
        
        esperando = True
        while esperando:
            for y in range(alto):
                intensidad = int(40 + 20 * math.sin(time.time() + y * 0.01))
                color = (intensidad//4, intensidad//3, intensidad//2)
                pygame.draw.line(pantalla, color, (0, y), (ancho, y))
            
            mensaje1 = fuente.render("¡Juego Terminado!", True, AMARILLO)
            rect_mensaje1 = mensaje1.get_rect(center=(ancho//2, alto//2 - 60))
            
            sombra1 = fuente.render("¡Juego Terminado!", True, NEGRO)
            rect_sombra1 = sombra1.get_rect(center=(rect_mensaje1.centerx + 3, rect_mensaje1.centery + 3))
            pantalla.blit(sombra1, rect_sombra1)
            pantalla.blit(mensaje1, rect_mensaje1)
            
            mensaje2 = fuente_pequeña.render("ENTER = Jugar de nuevo", True, LIMA)
            rect_mensaje2 = mensaje2.get_rect(center=(ancho//2, alto//2 + 20))
            pantalla.blit(mensaje2, rect_mensaje2)
            
            mensaje3 = fuente_pequeña.render("ESC = Salir", True, ROJO)
            rect_mensaje3 = mensaje3.get_rect(center=(ancho//2, alto//2 + 60))
            pantalla.blit(mensaje3, rect_mensaje3)
            
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        esperando = False
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

if __name__ == "__main__":
    try:
        principal()
    except Exception as e:
        pygame.quit()
        print(f"Error: {e}")
        sys.exit(1)