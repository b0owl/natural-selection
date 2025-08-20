import pygame  # type: ignore
import random

class Parent:
    def __init__(self, coord, color, speed, friendliness, aggression, mut_rate, pot_offspring):
        self.coord         = coord
        self.color         = color
        self.speed         = speed
        self.friendliness  = friendliness
        self.aggression    = aggression
        self.mut_rate      = mut_rate
        self.pot_offspring = pot_offspring

        self.set_offspring()

    def set_offspring(self):
        # Randomize potential offspring between 0 and the max
        self.pot_offspring = random.randint(0, self.pot_offspring)

    def move(self, modifier):
        x, y = self.coord
        dx, dy = modifier
        self.coord = (x + dx, y + dy)

    def draw_circle(self, color, size, screen):
        pygame.draw.circle(screen, color, self.coord, size)


class Child(Parent):
    def __init__(self, parent, color):
        super().__init__(
            color=color,
            coord=parent.coord,
            speed=parent.speed,
            friendliness=parent.friendliness,
            aggression=parent.aggression,
            mut_rate=parent.mut_rate,
            pot_offspring=parent.pot_offspring
        )

        # Apply mutations
        self.apply_mutations()

    def apply_mutations(self):
        # Mutate speed (0-100)
        self.speed = max(0, min(100, self.speed + random.randint(-5, 5)))

        # Mutate friendliness and aggression (0-1 float)
        self.friendliness = min(1, max(0, self.friendliness + random.uniform(-self.mut_rate, self.mut_rate)))
        self.aggression = min(1, max(0, self.aggression + random.uniform(-self.mut_rate, self.mut_rate)))

        # Mutate mutation slightly (0-1)
        self.mut_rate = min(1, max(0, self.mut_rate + random.uniform(-0.01, 0.01)))

        # Mutate potential offspring
        self.set_offspring()
