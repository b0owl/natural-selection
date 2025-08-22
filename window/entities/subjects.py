import pygame
import random

class Parent:
    def __init__(self, sight, coord, color, speed, friendliness, aggression, mut_rate, pot_offspring):
        self.coord         = coord
        self.color         = color
        self.speed         = speed
        self.friendliness  = friendliness
        self.aggression    = aggression
        self.mut_rate      = mut_rate
        self.pot_offspring = pot_offspring
        self.sight         = sight

        self.pos = coord 

        self.set_offspring()

        self.gender = random.choice(['M', 'F'])
        self.mated = False

        self.food_eaten_count = 0


    def set_offspring(self):
        self.pot_offspring = random.randint(0, self.pot_offspring)

    def move(self, modifier):
        x, y = self.coord
        dx, dy = modifier
        self.coord = (x + dx, y + dy)
        self.pos = self.coord 

    def draw(self, color, size, screen):
        pygame.draw.circle(screen, color, (int(self.coord[0]), int(self.coord[1])), size)

    def scan_mates(self, sight, parents):
        closest_mate = None
        min_distance = float('inf')  # start with infinite distance

        for potential_mate in parents:
            if potential_mate is not self and self.gender != potential_mate.gender:
                dx = self.pos[0] - potential_mate.pos[0]
                dy = self.pos[1] - potential_mate.pos[1]
                distance = (dx**2 + dy**2)**0.5  # Euclidean distance

                if distance <= sight and distance < min_distance:
                    closest_mate = potential_mate
                    min_distance = distance

        return closest_mate  
    
    def has_mated(self):
        self.mated = True 

    def eaten(self):
        self.food_eaten_count += 1

    def reset_eaten(self):
        self.food_eaten_count = 0
    


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

        self.gender = random.choice(['M', 'F'])

        speed = self.P1speed / self.P2speed
        friendliness = self.P1friendliness + self.P2friendliness
        aggression = self.P1aggression + self.P2aggression
        mut_rate = self.P1mut_rate + self.P2mut_rate
        pot_offspring = self.P1pot_offspring + self.P2pot_offspring

        super().__init__(
            sight=(parent1.sight + parent2.sight) / 2,  
            coord=(150, 150),
            color=color,
            speed=speed,
            friendliness=friendliness,
            aggression=aggression,
            mut_rate=mut_rate,
            pot_offspring=pot_offspring
        )


        self.apply_mutations()

    def apply_mutations(self):
        pass

class Food:
    def __init__(self, coords, color, size):
        self.coords = coords 
        self.color  = color   
        self.size   = size    

    def draw(self, screen):
        rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.color, rect)
