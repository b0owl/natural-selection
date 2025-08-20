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
        # Store parent stats on the child
        self.P1speed = parent1.speed
        self.P1friendliness = parent1.friendliness
        self.P1aggression = parent1.aggression
        self.P1mut_rate = parent1.mut_rate
        self.P1pot_offspring = parent1.pot_offspring

        self.P2speed = parent2.speed
        self.P2friendliness = parent2.friendliness
        self.P2aggression = parent2.aggression
        self.P2mut_rate = parent2.mut_rate
        self.P2pot_offspring = parent2.pot_offspring

        speed = self.P1speed + self.P2speed
        friendliness = self.P1friendliness + self.P2friendliness
        aggression = self.P1aggression + self.P2aggression
        mut_rate = self.P1mut_rate + self.P2mut_rate
        pot_offspring = self.P1pot_offspring + self.P2pot_offspring

        super().__init__(
            speed=speed,
            friendliness=friendliness,
            aggression=aggression,
            mut_rate=mut_rate,
            pot_offspring=pot_offspring,
            color=color,
            coord=(0, 0)
        )

        self.apply_mutations()

    def apply_mutations(self):
        import random
        self.speed += random.randint(-1, 1)
        self.friendliness += random.randint(-1, 1)
        self.aggression += random.randint(-1, 1)
        self.mut_rate += random.uniform(-0.01, 0.01)
        self.pot_offspring += random.randint(-1, 1)
