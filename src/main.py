import sys
import random
import pygame
# Utilidades
from interfaz.utils.constants import WHITE, GRAY, RED, GREEN
from interfaz.utils.constants import FPS, CAR_SPAWN_CHANCE, CAR_SPAWN_SPEED
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

# Variables globales para las listas de coches
vertical_queue = []
horizontal_queue = []
active_cars = []
incoming_cars = []


def draw_window(lights):
    global vertical_queue, horizontal_queue, active_cars, incoming_cars
    
    # Fondo
    WIN.fill(WHITE)

    # Calles
    pygame.draw.rect(WIN, GRAY, (300, 0, 200, HEIGHT))  # vertical
    pygame.draw.rect(WIN, GRAY, (0, 300, WIDTH, 200))  # horizontal

    # Combinar todas las listas para dibujar
    all_cars = incoming_cars + vertical_queue + horizontal_queue + active_cars
    
    # Coches
    for car in all_cars:
        car.draw(WIN)

    # Semáforos
    for light in lights:
        light.draw(WIN)
    
    # Información de debug
    font = pygame.font.Font(None, 18)
    
    # Separar coches por tipo
    incoming_cars_list = [car for car in incoming_cars if hasattr(car, 'is_incoming') and car.is_incoming]
    vertical_cars_list = [car for car in vertical_queue if car.direction == "down"]
    horizontal_cars_list = [car for car in horizontal_queue if car.direction == "right"]
    active_cars_list = [car for car in active_cars if hasattr(car, 'is_in_intersection') and car.is_in_intersection]
    
    total_text = font.render(f"Total: {len(all_cars)}", True, (0, 0, 0))
    WIN.blit(total_text, (10, 10))
    
    incoming_text = font.render(f"Llegando: {len(incoming_cars_list)}", True, (0, 0, 0))
    vertical_text = font.render(f"Cola Vertical: {len(vertical_cars_list)}", True, (0, 0, 0))
    horizontal_text = font.render(f"Cola Horizontal: {len(horizontal_cars_list)}", True, (0, 0, 0))
    active_text = font.render(f"En Intersección: {len(active_cars_list)}", True, (0, 0, 0))
    
    WIN.blit(incoming_text, (10, 30))
    WIN.blit(vertical_text, (10, 50))
    WIN.blit(horizontal_text, (10, 70))
    WIN.blit(active_text, (10, 90))
    
    # Mostrar estado de los semáforos
    vertical_light = "Verde" if lights[0].color == GREEN else "Rojo"
    horizontal_light = "Verde" if lights[1].color == GREEN else "Rojo"
    
    light_v_text = font.render(f"Semáforo V: {vertical_light}", True, (0, 0, 0))
    light_h_text = font.render(f"Semáforo H: {horizontal_light}", True, (0, 0, 0))
    
    WIN.blit(light_v_text, (10, 110))
    WIN.blit(light_h_text, (10, 130))
    
    # Mostrar tiempo restante del semáforo
    if lights[0].color == RED:
        # Si está en rojo, mostrar cuánto durará en verde
        next_green_duration_v = ((FPS*5) + ((FPS*2) * len(vertical_queue))) / FPS
        time_v_text = font.render(f"Tiempo que durará V: {round(next_green_duration_v, 1)}s", True, (0, 0, 0))
        WIN.blit(time_v_text, (10, 150))
    else:
        # Si está en verde, mostrar cuánto falta para cambiar a rojo
        time_remaining = (lights[0].green_time - lights[0].timer) / FPS
        time_v_text = font.render(f"Tiempo restante V: {round(time_remaining, 1)}s", True, (0, 0, 0))
        WIN.blit(time_v_text, (10, 150))
    
    if lights[1].color == RED:
        # Si está en rojo, mostrar cuánto durará en verde
        next_green_duration_h = ((FPS*5) + ((FPS*2) * len(horizontal_queue))) / FPS
        time_h_text = font.render(f"Tiempo que durará H: {round(next_green_duration_h, 1)}s", True, (0, 0, 0))
        WIN.blit(time_h_text, (10, 170))
    else:
        # Si está en verde, mostrar cuánto falta para cambiar a rojo
        time_remaining = (lights[1].green_time - lights[1].timer) / FPS
        time_h_text = font.render(f"Tiempo restante H: {round(time_remaining, 1)}s", True, (0, 0, 0))
        WIN.blit(time_h_text, (10, 170))

    pygame.display.update()


def main():
    global vertical_queue, horizontal_queue, active_cars, incoming_cars
    
    run = True
    # Limpiar las listas globales al inicio
    vertical_queue.clear()
    horizontal_queue.clear()
    active_cars.clear()
    incoming_cars.clear()
    
    lights = [
        TrafficLight(370, 270, "vertical"),  # arriba
        TrafficLight(270, 370, "horizontal"),  # izquierda
    ]

    spawn_timer = 0
    # Variable para controlar qué semáforo está activo
    active_light_index = 0  # 0 = vertical, 1 = horizontal
    max_cars_per_lane = 3

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Generar coches cada cierto tiempo (solo si hay espacio en la cola)
        spawn_timer += 1
        if spawn_timer > CAR_SPAWN_SPEED:  # cada ~1 segundos intentar generar un coche
            spawn_probability = CAR_SPAWN_CHANCE  # 25% de probabilidad de generar un coche
            if random.random() < spawn_probability:
                # Seleccionar calle seudo-aleatoriamente
                direction = random.choice(["down", "right"])
                
                # Solo generar coche si hay espacio en la cola correspondiente
                can_spawn = False
                if direction == "down" and len(vertical_queue) < max_cars_per_lane:
                    can_spawn = True
                elif direction == "right" and len(horizontal_queue) < max_cars_per_lane:
                    can_spawn = True
                
                if can_spawn:
                    if direction == "down": 
                        # Crear coche fuera de la pantalla (arriba) que se moverá hacia la cola
                        new_car = Car(380, -50, "down")
                        new_car.is_incoming = True  # Marcar como coche que está llegando
                        incoming_cars.append(new_car)
                    elif direction == "right":
                        # Crear coche fuera de la pantalla (izquierda) que se moverá hacia la cola
                        new_car = Car(-50, 420, "right")
                        new_car.is_incoming = True  # Marcar como coche que está llegando
                        incoming_cars.append(new_car)
            spawn_timer = 0

        # Mover coches que están llegando hacia las colas
        cars_to_move_to_queue = []
        for car in incoming_cars:
            if car.direction == "down":
                # Mover hacia abajo hasta llegar a la posición de la cola
                if car.rect.y < 200 - (len(vertical_queue) + 1) * 50:
                    car.rect.y += 1  # Movimiento gradual hacia abajo
                else:
                    # Cuando llega a la posición de la cola, moverlo a la cola
                    car.is_incoming = False
                    vertical_queue.append(car)
                    cars_to_move_to_queue.append(car)
            elif car.direction == "right":
                # Mover hacia la derecha hasta llegar a la posición de la cola
                if car.rect.x < 200 - (len(horizontal_queue) + 1) * 50:
                    car.rect.x += 1  # Movimiento gradual hacia la derecha
                else:
                    # Cuando llega a la posición de la cola, moverlo a la cola
                    car.is_incoming = False
                    horizontal_queue.append(car)
                    cars_to_move_to_queue.append(car)
        
        # Remover coches que ya llegaron a la cola
        for car in cars_to_move_to_queue:
            incoming_cars.remove(car)

        # Contar coches esperando en cada semáforo
        waiting_vertical = len(vertical_queue)
        waiting_horizontal = len(horizontal_queue)

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

        # Mover coches de las colas a activos si el semáforo está en verde
        # Solo un coche por dirección puede cruzar a la vez
        vertical_active = [car for car in active_cars if car.direction == "down"]
        horizontal_active = [car for car in active_cars if car.direction == "right"]
        
        if lights[0].color == GREEN and vertical_queue and len(vertical_active) == 0:
            # Mover el primer coche de la cola vertical a activos gradualmente
            car = vertical_queue[0]
            # Mover hacia el semáforo gradualmente
            if car.rect.y < 200:
                car.rect.y += 1  # Movimiento gradual
            else:
                # Cuando llega al semáforo, moverlo a activos
                vertical_queue.pop(0)
                active_cars.append(car)
                # Reorganizar la cola vertical (mover hacia el semáforo)
                for i, queued_car in enumerate(vertical_queue):
                    queued_car.rect.y = 200 - (i + 1) * 50
        
        if lights[1].color == GREEN and horizontal_queue and len(horizontal_active) == 0:
            # Mover el primer coche de la cola horizontal a activos gradualmente
            car = horizontal_queue[0]
            # Mover hacia el semáforo gradualmente
            if car.rect.x < 200:
                car.rect.x += 1  # Movimiento gradual
            else:
                # Cuando llega al semáforo, moverlo a activos
                horizontal_queue.pop(0)
                active_cars.append(car)
                # Reorganizar la cola horizontal (mover hacia el semáforo)
                for i, queued_car in enumerate(horizontal_queue):
                    queued_car.rect.x = 200 - (i + 1) * 50

        # Mover coches activos
        for car in active_cars:
            # Determinar qué semáforo controla este coche
            if car.direction in ["up", "down"]:
                controlling_light = lights[0]  # vertical
            else:
                controlling_light = lights[1]  # horizontal
            
            car.move(controlling_light, active_cars)

        # Limpiar coches que ya cruzaron la intersección
        active_cars = [car for car in active_cars if not (
            (car.direction == "down" and car.rect.y > 500) or
            (car.direction == "right" and car.rect.x > 500)
        )]

        # Dibujar la ventana
        draw_window(lights)


if __name__ == "__main__":
    main()
