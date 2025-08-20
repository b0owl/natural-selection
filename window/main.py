from entities import subjects
import random

def create_parents(parents, max_speed, max_friendliess, max_aggersion, max_offspring, max_mut_rate, min_mut_rate):  
    starting_coords = ((0, 0))
    parent_color = ((255, 255, 255)) # white

    PARENTS = []

    speed           = random.uniform(0.1,          max_speed       ) # set to 0.1 to guarentee entity can move
    friendliness    = random.uniform(0,            max_friendliess )
    aggression      = random.uniform(0,            max_aggersion   )
    pot_offspring   = random.randint(0,            max_offspring   )
    mut_rate        = random.uniform(min_mut_rate, max_mut_rate    ) # if 0 offspring will be identical

    for parent in range(parents): 
        PARENTS.append(
            subjects.Parent(starting_coords, parent_color, speed, friendliness, aggression, mut_rate, pot_offspring)
        )

    return PARENTS

parents = create_parents(6, 5, 0.3, 0.3, 2, 0.5, 0.1) # sorry for the magic numbers lmao

def create_children(parent1, parent2):
    pass # <- logic here
    # hopping off now
    