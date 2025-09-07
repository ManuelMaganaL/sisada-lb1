import sys
import random
import pygame
# Utilidades
from interfaz.utils.constants import WHITE, GRAY, FPS, RED
# Objetos de la simulacion
from interfaz.objects.car import Car
from interfaz.objects.traffic_light import TrafficLight


# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de tráfico con autoajuste")

# Reloj
clock = pygame.time.Clock()


def draw_window(cars, lights):
    # Fondo
    WIN.fill(WHITE)

    # Calles
    pygame.draw.rect(WIN, GRAY, (300, 0, 200, HEIGHT))  # vertical
    pygame.draw.rect(WIN, GRAY, (0, 300, WIDTH, 200))  # horizontal

    # Coches
    for car in cars:
        car.draw(WIN)

    # Semáforos
    for light in lights:
        light.draw(WIN)

    pygame.display.update()


def main():
    run = True
    cars = []
    lights = [
        TrafficLight(370, 270, "vertical"),  # arriba
        TrafficLight(270, 370, "horizontal"),  # izquierda
    ]

    spawn_timer = 0
    # Variable para controlar qué semáforo está activo
    active_light_index = 0  # 0 = vertical, 1 = horizontal

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Generar coches cada cierto tiempo
        spawn_timer += 1
        if spawn_timer > 30:  # cada ~0.5 segundos
            # Seleccionar calle seudo-aleatoriamente
            direction = random.choice(["down", "right"])
            
            if direction == "down": 
                cars.append(Car(380, -40, "down")) # De arriba a abajo
            elif direction == "right":
                cars.append(Car(-40, 420, "right")) # De izquierda a derecha
            spawn_timer = 0 # Reiniciar timer

        # Contar coches esperando en cada semáforo
        waiting_vertical = 0
        waiting_horizontal = 0
        
        for car in cars:
            # Contar coches esperando en la calle vertical (dirección down)
            if car.direction == "down" and car.rect.y < 300 and car.rect.y > 200:
                waiting_vertical += 1
            # Contar coches esperando en la calle horizontal (dirección right)  
            elif car.direction == "right" and car.rect.x < 300 and car.rect.x > 200:
                waiting_horizontal += 1

        # Actualizar semáforos con alternancia
        for i, light in enumerate(lights):
            if i == active_light_index:
                # El semáforo activo se actualiza normalmente
                if light.orientation == "vertical":
                    light.update(waiting_vertical)
                else:
                    light.update(waiting_horizontal)
                
                # Si el semáforo activo cambió a rojo, cambiar al otro
                if light.color == RED and light.timer == 0:
                    active_light_index = 1 - active_light_index
            else:
                # El semáforo inactivo se mantiene en rojo
                light.color = RED
                light.timer = 0

        # Mover coches
        for car in cars:
            # Determinar qué semáforo controla este coche
            if car.direction in ["up", "down"]:
                # Coches verticales son controlados por el semáforo vertical
                controlling_light = lights[0]  # vertical
            else:
                # Coches horizontales son controlados por el semáforo horizontal
                controlling_light = lights[1]  # horizontal
            
            car.move(controlling_light)

        # Limpiar coches que ya cruzaron la intersección
        cars = [car for car in cars if not (
            (car.direction == "down" and car.rect.y > 500) or  # Pasó la intersección vertical
            (car.direction == "right" and car.rect.x > 500)    # Pasó la intersección horizontal
        )]

        draw_window(cars, lights)


if __name__ == "__main__":
    main()
