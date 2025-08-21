from entities import subjects
import random
import math
import cwin 
import pygame 

def create_parents(parents, max_speed, max_friendliess, max_aggersion, max_offspring, max_mut_rate, min_mut_rate, max_sight, rect):  
    PARENTS = []

    for _ in range(parents):
        # random stats
        speed        = random.uniform(0.1, max_speed)
        friendliness = random.uniform(0, max_friendliess)
        aggression   = random.uniform(0, max_aggersion)
        pot_offspring = random.randint(0, max_offspring)
        mut_rate     = random.uniform(min_mut_rate, max_mut_rate)
        sight        = random.uniform(1, max_sight)

        # random starting position within rect
        x = random.randint(rect.left + 10, rect.right - 10)
        y = random.randint(rect.top + 10, rect.bottom - 10)
        starting_coords = (x, y)

        # create the parent first
        parent = subjects.Parent(sight, starting_coords, (255, 255, 255), speed, friendliness, aggression, mut_rate, pot_offspring)

        if parent.gender == 'M':
            parent.color = (0, 0, 255)   # blue
        else:
            parent.color = (255, 105, 180)  # pink

        PARENTS.append(parent)

    return PARENTS



"""
 Takes args:
 parents                 -> set to 12
 max_speed               -> set to 5
 max_friendliess         -> set to 0.3
 max_aggresion           -> set to 0.3
 max_offspring           -> set to 2
 max_mut_rate            -> set to 0.5
 min_mut_rate            -> set to 0.1
 sight (in px)           -> set to 50
"""
rect = pygame.Rect(50, 100, 1500, 800)
parents = create_parents(12, 5, 0.3, 0.3, 2, 0.5, 0.1, 300, rect) # sorry for the magic numbers lmao

def create_children():
    global parents 

    pairs = 0
    CHILDREN = []
    for pair in range(len(parents)):
        pairs += 1

    possible_children = pairs / 2 

    if isinstance(possible_children, float):
        for child in range(math.floor(possible_children)):
            CHILDREN.append(subjects.Child(parents[child], parents[child+1], (0, 255, 0)))
    else:
        for child in range(math.floor(possible_children)):
            CHILDREN.append(subjects.Child(parents[child], parents[child+1], (0, 255, 0)))

    return CHILDREN

children = create_children()

def create_food(amt, rect, buffer=0):
    FOOD = []
    for _ in range(amt):
        x = random.randint(rect.left + buffer, rect.right - buffer - 30)  # 30 = food width
        y = random.randint(rect.top  + buffer, rect.bottom - buffer - 30) # 30 = food height

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        size = (30, 30)
        FOOD.append(subjects.Food(coords=(x, y), color=color, size=size))
    return FOOD


food = create_food(10, rect, buffer=10)

def do(screen):

    color = (255, 255, 255)  # white
    buffer = 10
    pygame.draw.rect(screen, color, rect, width=2)

    # ----- draw food -----
    for f in food:
        f.draw(screen)


    for parent in parents:
        # ----- find closest mate -----
        mate = parent.scan_mates(parent.sight, parents)
        dx = dy = 0  # default movement

        # ----- find closest food -----
        closest_food = None
        min_food_dist = float('inf')
        for f in food:
            food_center = (f.coords[0] + f.size[0] // 2, f.coords[1] + f.size[1] // 2)
            dx_f = food_center[0] - parent.coord[0]
            dy_f = food_center[1] - parent.coord[1]
            dist_f = (dx_f**2 + dy_f**2)**0.5

            if dist_f < parent.sight and dist_f < min_food_dist:
                min_food_dist = dist_f
                closest_food = f

        # ----- decide target -----
        if closest_food is not None:
            # move toward food
            target = (closest_food.coords[0] + closest_food.size[0] // 2,
                      closest_food.coords[1] + closest_food.size[1] // 2)
            stop_distance = 5
        elif mate is not None:
            # move toward mate
            target = mate.coord
            stop_distance = 20
        else:
            # random wandering
            dx = parent.speed * random.uniform(-1, 1)
            dy = parent.speed * random.uniform(-1, 1)
            target = None

        # ----- calculate movement -----
        if target is not None:
            dx = target[0] - parent.coord[0]
            dy = target[1] - parent.coord[1]
            distance = (dx**2 + dy**2)**0.5

            if distance > stop_distance:
                attraction_strength = 5.0
                dx = (dx / distance) * parent.speed * attraction_strength
                dy = (dy / distance) * parent.speed * attraction_strength
            else:
                dx = dy = 0

                # eat food if reached
                if closest_food is not None and closest_food in food:
                    food.remove(closest_food)

        # ----- update position -----
        x = min(max(parent.coord[0] + dx, rect.left + buffer), rect.right - buffer)
        y = min(max(parent.coord[1] + dy, rect.top + buffer), rect.bottom - buffer)
        parent.coord = (x, y)

        # draw parent
        parent.draw(parent.color, 10, screen)

    # ----- update children -----
    for child in children:
        dx = child.speed * random.uniform(-1, 1)
        dy = child.speed * random.uniform(-1, 1)
        x = min(max(child.coord[0] + dx, rect.left + buffer), rect.right - buffer)
        y = min(max(child.coord[1] + dy, rect.top + buffer), rect.bottom - buffer)
        child.coord = (x, y)
        child.draw(child.color, 8, screen)

    # ----- draw table -----
    data = [
        ["Test", "Test4", "Test5"],  # header
        ["Test1", 23,      95],
        ["Test2", 30,      88],
        ["Test3", 25,      92],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
        [''     , '',      ''],
    ]
    table_x, table_y = 1570, 100
    cell_width, cell_height = 100, 40
    font = pygame.font.Font(None, 24)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            cell_rect = pygame.Rect(
                table_x + j * cell_width,
                table_y + i * cell_height,
                cell_width,
                cell_height
            )
            pygame.draw.rect(screen, (255, 255, 255), cell_rect, 2)
            text_surf = font.render(str(value), True, (255, 255, 255))
            screen.blit(text_surf, (table_x + j * cell_width + 5, table_y + i * cell_height + 5))



cwin.startWin(do, 0.1)
