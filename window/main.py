from entities import subjects
import random
import math
import cwin 
import pygame 

def create_parents(parents, max_speed, 
                   max_friendliess, max_aggersion, 
                   max_offspring, max_mut_rate,
                   min_mut_rate, min_sight, max_sight, rect):  
    PARENTS = []

    for _ in range(parents):
        # random stats
        speed        = random.uniform(0.1, max_speed)
        friendliness = random.uniform(0, max_friendliess)
        aggression   = random.uniform(0, max_aggersion)
        pot_offspring = random.randint(0, max_offspring)
        mut_rate     = random.uniform(min_mut_rate, max_mut_rate)
        sight        = random.uniform(min_sight, max_sight)

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


rect = pygame.Rect(5, 100, 1500, 800)

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


def create_food(amt, rect, buffer=0):
    FOOD = []
    for _ in range(amt):
        x = random.randint(rect.left + buffer, rect.right - buffer - 30)  # 30 = food width
        y = random.randint(rect.top  + buffer, rect.bottom - buffer - 30) # 30 = food height

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        size = (30, 30)
        FOOD.append(subjects.Food(coords=(x, y), color=color, size=size))
    return FOOD



day = 1
t_remaining = 15
elapsed_time = 0  # tracks elapsed time
dt = 0

"""
 Takes args:
 parents                 -> set to 12
 max_speed               -> set to 5
 max_friendliess         -> set to 0.3
 max_aggresion           -> set to 0.3
 max_offspring           -> set to 2
 max_mut_rate            -> set to 0.5
 min_mut_rate            -> set to 0.1
 min_sight               -> locked to sight
 sight (in px)           -> set to 30

 sorry if this is outdated lol, too lazy to change it whenever i change an arg
"""
parents = create_parents(100, 5, 0.3, 0.3, 2, 0.5, 0.1, 300, 300, rect) # sorry for the magic numbers lmao
food_to_generate = 200
food = create_food(food_to_generate, rect, buffer=10)
#children = create_children()
children = []

def child_cb(parent1, parent2, screen):
    child = subjects.Child(parent1, parent2, (0, 255, 0))
    if child.gender == 'M':
        child.color = (7, 29, 74)
    else:
        child.color = (163, 36, 150)
    x = parent1.pos[0]
    y = parent1.pos[1]

    child.draw(child.color, 8, screen)
    
    return child

def do(screen):  
    global dt, food_to_generate, food
    global day, t_remaining, elapsed_time

    male = 0
    female = 0
    color = (255, 255, 255)  # white
    buffer = 10
    pygame.draw.rect(screen, color, rect, width=2)

    # ----- draw food -----
    for f in food:
        f.draw(screen)

    # ----- update parents -----
    for parent in parents:
        # ----- find closest mate -----
        mate = parent.scan_mates(parent.sight, parents)
        dx = dy = 0  # default movement

        # ----- find closest food -----
        closest_food = None
        min_food_dist = float('inf')
        for f in food:
            food_center = (f.coords[0] + f.size[0] // 2, f.coords[1] + f.size[1] // 2)
            dx_f = food_center[0] - parent.pos[0]
            dy_f = food_center[1] - parent.pos[1]
            dist_f = (dx_f**2 + dy_f**2)**0.5

            if dist_f < parent.sight and dist_f < min_food_dist:
                min_food_dist = dist_f
                closest_food = f

        # ----- decide target -----
        if closest_food is not None:
            target = (closest_food.coords[0] + closest_food.size[0] // 2,
                      closest_food.coords[1] + closest_food.size[1] // 2)
            stop_distance = 5
        elif mate is not None:
            target = mate.coord
            stop_distance = 20
        else:
            dx = parent.speed * random.uniform(-1, 1)
            dy = parent.speed * random.uniform(-1, 1)
            target = None


        # ----- check gender ----- 
        if parent.gender == 'M':
            male += 1
        else:
            female += 1

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
                dx = dy = 0  # STOP MOVING
                
                # ----- mating -----
                if mate is not None:
                    if parent.gender != mate.gender and not parent.mated and parent.food_eaten_count >= 2:
                        parent.has_mated()
                        new_child = child_cb(parent, mate, screen)
                        children.append(new_child)
                        parent.coords = (rect.left, random.randint(0, 800))

                # eat food if reached
                if closest_food is not None and closest_food in food:
                    parent.eaten()
                    food.remove(closest_food)



        # ----- update position -----
        x = min(max(parent.coord[0] + dx, rect.left + buffer), rect.right - buffer)
        y = min(max(parent.coord[1] + dy, rect.top + buffer), rect.bottom - buffer)
        parent.coord = (x, y)

        # draw parent
        parent.draw(parent.color, 10, screen)
            
    # ----- update children -----
    for child in children:
        # ----- find closest food -----
        closest_food = None
        min_food_dist = float('inf')
        for f in food:
            food_center = (f.coords[0] + f.size[0] // 2, f.coords[1] + f.size[1] // 2)
            dx_f = food_center[0] - child.pos[0]
            dy_f = food_center[1] - child.pos[1]
            dist_f = (dx_f**2 + dy_f**2)**0.5

            if dist_f < child.sight and dist_f < min_food_dist:
                min_food_dist = dist_f
                closest_food = f

        # ----- decide target -----
        if closest_food is not None:
            target = (closest_food.coords[0] + closest_food.size[0] // 2,
                    closest_food.coords[1] + closest_food.size[1] // 2)
            stop_distance = 5
        else:
            dx = child.speed * random.uniform(-1, 1)
            dy = child.speed * random.uniform(-1, 1)
            target = None

        # ----- calculate movement -----
        if target is not None:
            dx = target[0] - child.coord[0]
            dy = target[1] - child.coord[1]
            distance = (dx**2 + dy**2)**0.5

            if distance > stop_distance:
                attraction_strength = 5.0
                dx = (dx / distance) * child.speed * attraction_strength
                dy = (dy / distance) * child.speed * attraction_strength
            else:
                dx = dy = 0  # STOP MOVING

                if closest_food is not None:
                    food_rect = pygame.Rect(closest_food.coords, closest_food.size)
                    if food_rect.collidepoint(child.coord): 
                        child.eaten()
                        food.remove(closest_food)

        # ----- check gender ----- 
        if child.gender == 'M':
            male += 1
        else:
            female += 1
            
        # ----- update position -----
        x = min(max(child.coord[0] + dx, rect.left + buffer), rect.right - buffer)
        y = min(max(child.coord[1] + dy, rect.top + buffer), rect.bottom - buffer)
        child.coord = (x, y)

        # draw child
        child.draw(child.color, 10, screen)

    
    # ----- update day timer -----
    elapsed_time += dt
    t_remaining -= dt
    if t_remaining <= 0:
        day += 1
        male = 0
        female = 0

        # ----- kill parents -----
        for i in reversed(range(len(parents))):
            parent = parents[i]

            # kill if could not eat
            if parent.food_eaten_count < 1:
                del parents[i]  

        for i in reversed(range(len(children))):
            child = children[i]

            # kill if could not eat
            if child.food_eaten_count < 1:
                del children[i]
        
        # ----- generate more food -----
        if food_to_generate > 10:
            food_to_generate -= 5
        else:
            food_to_generate = 30
        food = create_food(food_to_generate, rect, buffer=10)

        for parent in parents:
            print(f'Parent {parent} has eaten {parent.food_eaten_count} food')
            parent.coord = (random.randint(0, 800), rect.bottom)
            parent.reset_eaten()
            parent.mated = False
            
        for child in children:
            print(f'Child {child} has eaten {child.food_eaten_count} food')
            child.coord = (random.randint(0, 800), rect.top)
            child.reset_eaten()
            child.mated = False

        t_remaining = 15
        elapsed_time = 0


    # ----- draw table -----
    data = [
        ["Day", "Time", "Male", "Female", "Food"],  # header
        [day, int(t_remaining), male, female, len(food)],
    ]
    table_x, table_y = 1525, 100
    cell_width, cell_height = 75, 40
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

dt = 0.1
cwin.startWin(do, 0.1)  