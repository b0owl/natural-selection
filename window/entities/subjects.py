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
    def __init__(self, parent1, parent2, color):
        super().__init__(
            color=color,
            coord=((0, 0)),

            ## p1
            P1speed=parent1.speed,
            P1friendliness=parent1.friendliness,
            P1aggression=parent1.aggression,
            P1mut_rate=parent1.mut_rate,
            P1pot_offspring=parent1.pot_offspring,

            ## p2
            P2speed=parent1.speed,
            P2friendliness=parent1.friendliness,
            P2aggression=parent1.aggression,
            P2mut_rate=        parent1.mut_rate,
            P2pot_offspring=   parent1.pot_offspring
        )

        # Apply mutations
        self.apply_mutations()

    def apply_mutations(self):
        self.speed = self.P1speed + self.P2speed
        self.friendliness = self.P1friendliness + self.P2friendliness
        self.aggression = self.P1aggression + self.p2aggression
        self.mut_rate = self.P1mut_rate + self.P2_mut_rate

        # Mutate potential offspring
        self.set_offspring()
