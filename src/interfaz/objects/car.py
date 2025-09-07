import pygame
from typing import Literal, List, Optional
from interfaz.utils.constants import BLUE, GREEN, YELLOW
from interfaz.utils.constants import CAR_SPEED
from interfaz.objects.traffic_light import TrafficLight


class Car:
    def __init__(self, x: int, y: int, direction: Literal["down", "right"]):    
        """
        Inicializa un coche en la posición (x, y) con una dirección dada.
        Args:
            x (int): Posición x inicial del coche.
            y (int): Posición y inicial del coche.
            direction (str): Dirección del coche ("up", "down", "left", "right").
        """    
        self.direction = direction
        self.speed = CAR_SPEED
        self.is_waiting = False
        self.is_in_intersection = False

        # Rota el rectangulo (coche) segun la calle por la que va
        if direction in ["up", "down"]:
            self.rect = pygame.Rect(x, y, 20, 40)
        else:
            self.rect = pygame.Rect(x, y, 40, 20)


    def move(self, light: TrafficLight, other_cars: List['Car']):
        """
        Mueve el coche en su dirección si el semáforo está en verde o si ya está en la intersección.
        Args:
            light (TrafficLight): El semáforo que controla el movimiento del coche.
            other_cars (List[Car]): Lista de otros coches para detectar colisiones.
        """
        # Verificar si el coche está en la zona de intersección
        self.is_in_intersection = False
        
        if self.direction == "down":
            # Para coches que van hacia abajo, están en intersección si están entre y=200 y y=500
            self.is_in_intersection = 200 <= self.rect.y <= 500
        elif self.direction == "right":
            # Para coches que van hacia la derecha, están en intersección si están entre x=200 y x=500
            self.is_in_intersection = 200 <= self.rect.x <= 500
        
        # TEMPORAL: Simplificar movimiento - solo verificar semáforo
        # El coche puede moverse si:
        # 1. El semáforo está en verde, O ya está en la intersección
        if light.color == GREEN or self.is_in_intersection:
            self.is_waiting = False
            if self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
        else:
            self.is_waiting = True

    def _check_collision(self, other_cars: List['Car']) -> bool:
        """
        Verifica si este coche colisionaría con otros coches al moverse.
        Args:
            other_cars (List[Car]): Lista de otros coches.
        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        # Crear un rectángulo temporal para la próxima posición
        next_rect = self.rect.copy()
        
        if self.direction == "down":
            next_rect.y += self.speed
        elif self.direction == "up":
            next_rect.y -= self.speed
        elif self.direction == "left":
            next_rect.x -= self.speed
        elif self.direction == "right":
            next_rect.x += self.speed
        
        # Verificar colisión simple con otros coches en la misma dirección
        for other_car in other_cars:
            if (other_car != self and 
                other_car.direction == self.direction and
                next_rect.colliderect(other_car.rect)):
                return True
        
        return False


    def draw(self, win: pygame.Surface):
        """
        Dibuja el coche en la ventana dada.
        Args:
            win: La ventana de Pygame donde se dibuja el coche.
        """
        # Cambiar color según el estado del coche
        if self.is_waiting:
            color = YELLOW  # Amarillo para coches esperando
        elif self.is_in_intersection:
            color = GREEN   # Verde para coches en intersección
        else:
            color = BLUE    # Azul para coches en movimiento normal
        
        # Dibujar el coche sin borde
        pygame.draw.rect(win, color, self.rect)
