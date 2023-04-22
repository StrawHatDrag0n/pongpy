import pygame
import math
import random
from game.constants import WHITE    

class Ball:
    COLOR = WHITE
    VELOCITY = 4


    def __init__(self, x, y, radius) -> None:
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius

        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_velocity = pos * abs(math.cos(angle) * self.VELOCITY)
        self.y_velocity = math.sin(angle) * self.VELOCITY
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y 

        angle = self._get_random_angle(-30, 30, [0])
        y_vel = math.sin(angle) * self.VELOCITY

        self.x_velocity *= -1
        self.y_velocity = y_vel