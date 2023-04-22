import pygame
from game.constants import WHITE, HEIGHT

class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win) -> None:
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move_up(self) -> bool:  
        if self.y - self.VELOCITY >= 0:
            self.y -= self.VELOCITY
            return True
        return False
    
    def move_down(self) -> bool:
        if self.y + self.VELOCITY + self.height <= HEIGHT:
            self.y += self.VELOCITY
            return True
        return False
            