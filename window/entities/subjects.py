import pygame # type: ignore 

class Subject:
    def __init__(self, coord, color):
        self.coord = coord
        self.color = color

    def move(self, modifier):
        x, y = self.coord
        dx, dy = modifier
        self.coord = (x + dx, y + dy)

    def draw_circle(self, color, size, screen):
        pygame.draw.circle(screen, color, self.coord, size)

