import pygame
from typing import Literal
from interfaz.utils.constants import BLUE, GREEN
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

        # Rota el rectangulo (coche) segun la calle por la que va
        if direction in ["up", "down"]:
            self.rect = pygame.Rect(x, y, 20, 40)
        else:
            self.rect = pygame.Rect(x, y, 40, 20)


    def move(self,  light: TrafficLight):
        """
        Mueve el coche en su dirección si el semáforo está en verde o si ya está en la intersección.
        Args:
            light (TrafficLight): El semáforo que controla el movimiento del coche.
        """
        # Verificar si el coche está en la zona de intersección
        in_intersection = False
        
        if self.direction == "down":
            # Para coches que van hacia abajo, están en intersección si están entre y=200 y y=500
            in_intersection = 200 <= self.rect.y <= 500
        elif self.direction == "right":
            # Para coches que van hacia la derecha, están en intersección si están entre x=200 y x=500
            in_intersection = 200 <= self.rect.x <= 500
        
        # El coche puede moverse si:
        # 1. El semáforo está en verde, O
        # 2. Ya está en la intersección (para que no se quede a mitad de calle)
        if light.color == GREEN or in_intersection:
            if self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed


    def draw(self, win: pygame.Surface):
        """
        Dibuja el coche en la ventana dada.
        Args:
            win: La ventana de Pygame donde se dibuja el coche.
        """
        pygame.draw.rect(win, BLUE, self.rect)
