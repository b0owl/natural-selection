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
food_to_generate = 50
food = create_food(food_to_generate, rect, buffer=10)
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

def create_bar_graph(screen, rows, coords, bar_width, max_height, values, scale=1, color=(0, 255, 0), font=None):
    x_start, y_start = coords
    
    # Draw bars
    for i in range(rows):
        if i >= len(values):
            break
        bar_height = min(values[i] * scale, max_height)
        rect = pygame.Rect(
            x_start + i * (bar_width + 5),  # 5 pixels spacing
            y_start - bar_height,
            bar_width,
            bar_height
        )
        pygame.draw.rect(screen, color, rect)
    
    total_width = rows * bar_width + (rows - 1) * 5
    border_rect = pygame.Rect(x_start - 2, y_start - max_height - 2, total_width + 4, max_height + 4)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)  # 2px thick white border

    if font is None:
        font = pygame.font.SysFont(None, 20)
    
    for i in range(0, max_height + 1, max(1, max_height // 5)):
        label = font.render(str(i), True, (255, 255, 255))
        screen.blit(label, (x_start - label.get_width() - 5, y_start - i - label.get_height() // 2))


def create_line_graph(screen, rows, coords, max_height, values, scale=1, color=(0, 255, 0), avg_speed_line_width=2, font=None):
    x_start, y_start = coords
    spacing = 5
    points = []

    for i in range(rows):
        if i >= len(values):
            break
        x = x_start + i * spacing
        y = y_start - min(values[i] * scale, max_height)
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, avg_speed_line_width)

    for point in points:
        pygame.draw.circle(screen, color, point, 1)

    total_width = (rows - 1) * spacing
    border_rect = pygame.Rect(x_start - 2, y_start - max_height - 2, total_width + 4, max_height + 4)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

    if font is None:
        font = pygame.font.SysFont(None, 20)

    for i in range(0, max_height + 1, max(1, max_height // 5)):
        label = font.render(str(i), True, (255, 255, 255))
        screen.blit(label, (x_start - label.get_width() - 5, y_start - i - label.get_height() // 2))



coordsBar = (1555, 300)   
bar_width = 20
max_heightBar = 100
valuesBar = []
scaleBar = 1

avg_speed_coords_line = (1555, 420) 
avg_speed_max_heightline = 100
avg_speed_values_line = []
avg_speed_scale_line = 6
avg_speed_line_width = 1 

avg_speed: int

for i in range(70):
    avg_speed_values_line.append(0)

def do(screen):  
    global avg_speed_values_line, valuesBar
    global avg_speed
    global dt, food_to_generate, food
    global day, t_remaining, elapsed_time

    # ----- initlize graph -----
    rowsBar = len(valuesBar)
    rowsLine = len(avg_speed_values_line)

    create_bar_graph(screen, rowsBar, coordsBar, bar_width, max_heightBar, valuesBar, scaleBar, color=(0, 200, 255))
    create_line_graph(screen, rowsLine, avg_speed_coords_line, avg_speed_max_heightline, avg_speed_values_line, scale=avg_speed_scale_line, color=(0,200,255), avg_speed_line_width=2)

    
    # write stuff
    font = pygame.font.Font(None, 12)  
    text_surface_1 = font.render("AVG SPEED OVER TIMME", True, (255, 255, 255))  # True = anti-alias, color = white
    x_1, y_1 = 1555, 430 
    screen.blit(text_surface_1, (x_1, y_1))


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

    # ----- get avg speed ----- 
    total_speeds = sum(parent.speed for parent in parents) + sum(child.speed for child in children)
    total_count = len(parents) + len(children)
    avg_speed = total_speeds / total_count if total_count > 0 else 0
    print(avg_speed)
    print(avg_speed_values_line)

    
    # ----- update day timer -----
    elapsed_time += dt
    t_remaining -= dt
    if day == 1 and not getattr(create_line_graph, "_done", False):
        avg_speed_values_line[0] = total_speeds
        create_line_graph._done = True


    if t_remaining <= 0 or len(food) == 0:
        day += 1
        male = 0
        female = 0 
        avg_speed_values_line[day] = avg_speed

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
            parent.coord = (random.randint(0, 800), rect.bottom)
            parent.reset_eaten()
            parent.mated = False
            
        for child in children:
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