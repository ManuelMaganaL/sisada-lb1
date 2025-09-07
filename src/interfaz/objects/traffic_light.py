import pygame
from typing import Literal
from interfaz.utils.constants import RED, GREEN, FPS


class TrafficLight:
    def __init__(self, x: int, y: int, orientation: Literal["vertical", "horizontal"]):
        """
        Inicializa un semáforo en la posición (x, y) con una orientación dada.
        Args:
            x (int): Posición x inicial del semáforo.
            y (int): Posición y inicial del semáforo.
            orientation (str): Orientación del semáforo ("vertical" o "horizontal").
        """
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = RED
        self.timer = 0
        self.orientation = orientation
        self.green_time = FPS*5 # Default 5 segundos
        self.red_time = FPS*5 # Default 5 segundos


    def update(self, cars_waiting: int):
        """
        Actualiza el estado del semáforo basado en el número de coches esperando.
        Args:
            cars_waiting (int): Número de coches esperando en la intersección.
        """
        # Autoajuste: más coches esperando = más tiempo en verde
        # Minimo de 5 segundos + 1 segundo por coche en espera
        self.green_time = (FPS*5) + FPS * cars_waiting
        self.green_time = min(self.green_time, FPS*10)  # máx. 10 segundos

        self.timer += 1
        if self.color == GREEN and self.timer > self.green_time:
            self.color = RED
            self.timer = 0
        elif self.color == RED and self.timer > self.red_time:
            self.color = GREEN
            self.timer = 0


    def draw(self, win: pygame.Surface):
        """
        Dibuja el semáforo en la ventana dada.
        Args:
            win: La ventana de Pygame donde se dibuja el semáforo.
        """
        pygame.draw.rect(win, self.color, self.rect)
