from entities import subjects
import random
import math
import cwin 
import pygame, time

def create_parents(parents, max_speed, 
                   max_friendliess, max_aggersion, 
                   max_offspring, max_mut_rate,
                   min_mut_rate, min_sight, max_sight, rect,
                   min_energy, max_energy):  
    PARENTS = []

    for _ in range(parents):
        # random stats
        speed         = random.uniform(0.1, max_speed             )
        friendliness  = random.uniform(0, max_friendliess         )
        aggression    = random.uniform(0, max_aggersion           )
        pot_offspring = random.randint(0, max_offspring           )
        mut_rate      = random.uniform(min_mut_rate, max_mut_rate )
        sight         = random.uniform(min_sight, max_sight       )
        energy        = random.uniform(min_energy, max_energy     )

        # random starting position within rect
        x = random.randint(rect.left + 10, rect.right - 10)
        y = random.randint(rect.top + 10, rect.bottom - 10)
        starting_coords = (x, y)

        # create the parent first
        parent = subjects.Parent(sight, starting_coords, (255, 255, 255), speed, friendliness, aggression, mut_rate, pot_offspring, energy)

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

parents = create_parents(50, 5, 0.3, 0.3, 2, 0.5, 0.1, 300, 300, rect, 10, 100) # sorry for the magic numbers lmao
food_to_generate = 500
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
    pygame.draw.rect(screen, (255, 255, 255), border_rect, 1) 

def create_line_graph(screen, rows, coords, values, graph_height=None, scale=1, color=(0, 255, 0), avg_speed_line_width=2, font=None):
    x_start, y_start = coords
    spacing = 5
    points = []

    max_height = graph_height if graph_height is not None else max(values) * scale

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
    border_thickness = 1 
    border_rect = pygame.Rect(x_start - border_thickness, y_start - max_height - border_thickness,
                              total_width + 2 * border_thickness, max_height + 2 * border_thickness)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, border_thickness)


coords_bar_population_size = (1555, 290)   
bar_width_population_size = 3
max_height_bar_population_size = 100
values_bar_population_size = []
scale_bar_population_size = 1

food_bar_amount_coords = (1555, 420)
food_bar_amount_size = 3
food_bar_amount_max_size = 100
food_bar_amount_values = []
food_bar_amount_scale = 1

avg_speed_coords_line = (1555, 550) 
avg_speed_max_heightline = 20
avg_speed_values_line = []
avg_speed_scale_line = 1
avg_speed_line_width = 1 

avg_speed_coords_line_daily = (1555, 690) 
avg_speed_max_heightline_daily = 20
avg_speed_values_line_daily = []
avg_speed_scale_line_daily = 1
avg_speed_line_width_daily = 1 

avg_speed: int

d1_graph_done = False # this basically justs checks if the data for the graphs
                      # has been plotted for day 1  

for i in range(70):
    avg_speed_values_line.append(0)
    avg_speed_values_line_daily.append(0)

for i in range(44):
    values_bar_population_size.append(0)
    food_bar_amount_values.append(0)

def do(screen):  
    global avg_speed_values_line, values_bar_population_size
    global avg_speed, d1_graph_done
    global dt, food_to_generate, food
    global day, t_remaining, elapsed_time
    global avg_speed_values_line_daily

    # ----- calculate avg speed -----
    total_speeds = sum(parent.speed for parent in parents) + sum(child.speed for child in children)
    total_count = len(parents) + len(children)
    avg_speed = total_speeds / total_count if total_count > 0 else 0

    # ----- update live line graph -----
    MAX_POINTS = 70  # width of the graph
    if len(avg_speed_values_line) >= MAX_POINTS:
        avg_speed_values_line.pop(0)  # remove oldest point
    avg_speed_values_line.append(avg_speed * 30)  # scale factor

    # ----- initialize graph -----
    rows_bar_population_size = len(values_bar_population_size)
    rows_bar_food_amount = len(food_bar_amount_values)
    rows_line_avg_speed = len(avg_speed_values_line)
    rows_line_avg_speed_daily = len(avg_speed_values_line_daily)

    create_bar_graph(
        screen, 
        rows_bar_population_size, 
        coords_bar_population_size, 
        bar_width_population_size, 
        max_height_bar_population_size, 
        values_bar_population_size, 
        scale_bar_population_size, 
        color=(255, 255, 255)
    )

    create_bar_graph(
        screen, 
        rows_bar_food_amount, 
        food_bar_amount_coords, 
        food_bar_amount_size, 
        food_bar_amount_max_size, 
        food_bar_amount_values, 
        food_bar_amount_size, 
        color=(58, 168, 36)
    )

    create_line_graph(
        screen,
        rows_line_avg_speed,
        avg_speed_coords_line,
        avg_speed_values_line,
        graph_height=100,   
        scale=avg_speed_scale_line,
        color=(255, 108, 3),
        avg_speed_line_width=2
    )

    create_line_graph(
        screen,
        rows_line_avg_speed_daily,
        avg_speed_coords_line_daily,
        avg_speed_values_line_daily,
        graph_height=100,   
        scale=avg_speed_scale_line_daily,
        color=(255, 108, 3),
        avg_speed_line_width=2
    )

    # ----- write labels -----
    font = pygame.font.Font(None, 12)  
    text_surface_avg_speed_over_time = font.render("AVG SPEED OVER TIME", True, (106, 160, 247))
    x_avg_speed_over_time, y_avg_speed_over_time = 1555, 555
    screen.blit(text_surface_avg_speed_over_time, (x_avg_speed_over_time, y_avg_speed_over_time))

    text_surface_avg_speed_over_gen = font.render("AVG SPEED OVER GENERATIONS", True, (106, 160, 247))
    x_avg_speed_over_gen, y_avg_speed_over_gen = 1555, 700
    screen.blit(text_surface_avg_speed_over_gen, (x_avg_speed_over_gen, y_avg_speed_over_gen))

    text_pop_over_gen = font.render("POPULATION OVER GENERATIONS", True, (106, 160, 247))
    x_pop_over_gen, y_pop_over_gen = 1555, 300 
    screen.blit(text_pop_over_gen, (x_pop_over_gen, y_pop_over_gen))

    # ----- counters -----
    male = 0
    female = 0
    color = (255, 255, 255)
    buffer = 10
    pygame.draw.rect(screen, color, rect, width=2)

    # ----- draw food -----
    for f in food:
        f.draw(screen)

    # ----- update parents -----
    for parent in parents:
        mate = parent.scan_mates(parent.sight, parents)
        dx = dy = 0

        # find closest food
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

        # decide target
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

        # gender count
        if parent.gender == 'M':
            male += 1
        else:
            female += 1

        # movement
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
                # mating
                if mate is not None and parent.gender != mate.gender and not parent.mated and parent.food_eaten_count >= 2:
                    parent.has_mated()
                    new_child = child_cb(parent, mate, screen)
                    children.append(new_child)
                    parent.coords = (rect.left, random.randint(0, 800))
                # eat food
                if closest_food is not None and closest_food in food:
                    parent.eaten()
                    food.remove(closest_food)
                    parent.energy += random.randint(5, 10)

        # update position
        new_dx = min(max(parent.coord[0] + dx, rect.left + buffer), rect.right - buffer) - parent.coord[0]
        new_dy = min(max(parent.coord[1] + dy, rect.top + buffer), rect.bottom - buffer) - parent.coord[1]
        parent.move((new_dx, new_dy))

        # draw
        parent.draw(parent.color, 10, screen)

    # ----- update children -----
    i = 0
    while i < len(children):
        child = children[i]
        closest_food = None
        min_food_dist = float('inf')

        # find closest food
        for f in food:
            food_center = (f.coords[0] + f.size[0] // 2, f.coords[1] + f.size[1] // 2)
            dx_f = food_center[0] - child.pos[0]
            dy_f = food_center[1] - child.pos[1]
            dist_f = (dx_f**2 + dy_f**2)**0.5
            if dist_f < child.sight and dist_f < min_food_dist:
                min_food_dist = dist_f
                closest_food = f

        mate = child.scan_mates(child.sight, children)

        if closest_food is not None:
            target = (closest_food.coords[0] + closest_food.size[0] // 2,
                    closest_food.coords[1] + closest_food.size[1] // 2)
            stop_distance = 5
        elif mate is not None:
            target = mate.coord
            stop_distance = 20
        else:
            dx = child.speed * random.uniform(-1, 1)
            dy = child.speed * random.uniform(-1, 1)
            target = None

        if target is not None:
            dx = target[0] - child.coord[0]
            dy = target[1] - child.coord[1]
            distance = (dx**2 + dy**2)**0.5
            if distance > stop_distance:
                attraction_strength = 5.0
                dx = (dx / distance) * child.speed * attraction_strength
                dy = (dy / distance) * child.speed * attraction_strength
            else:
                dx = dy = 0
                # eating
                if closest_food is not None and pygame.Rect(closest_food.coords, closest_food.size).collidepoint(child.coord):
                    child.eaten()
                    food.remove(closest_food)
                    child.energy += random.randint(5, 7)

                # mating
                if mate is not None and child.gender != mate.gender and not child.mated and child.food_eaten_count >= 2:
                    child.has_mated()
                    mate.has_mated()
                    new_child = child_cb(child, mate, screen)
                    children.append(new_child)

                    # promote children to parents
                    parents.append(child)
                    parents.append(mate)
                    del children[i]  # remove the current child
                    children.remove(mate)  # remove mate
                    i -= 1  
                    break 

        # update gender counts
        if child.gender == 'M':
            male += 1
        else:
            female += 1

        # apply movement
        new_dx = min(max(child.coord[0] + dx, rect.left + buffer), rect.right - buffer) - child.coord[0]
        new_dy = min(max(child.coord[1] + dy, rect.top + buffer), rect.bottom - buffer) - child.coord[1]
        child.move((new_dx, new_dy))
        child.draw(child.color, 10, screen)

        i += 1


    # ----- update day timer -----
    elapsed_time += dt
    t_remaining -= dt

    if day == 1 and not d1_graph_done:
        avg_speed_values_line_daily[1] = avg_speed * 30
        total = len(children) + len(parents)
        values_bar_population_size[1] = total / 10
        food_bar_amount_values[1] = len(food) / 20
        d1_graph_done = True

    if t_remaining <= 0 or len(food) == 0:
        day += 1
        male = 0
        female = 0

        avg_speed_values_line_daily[day] = avg_speed * 30
        total = len(children) + len(parents)

        values_bar_population_size[day] = total / 10

        # kill parents
        for i in reversed(range(len(parents))):
            parent = parents[i]
            if parent.food_eaten_count < 1 or parent.energy <= 0:
                del parents[i]

        for i in reversed(range(len(children))):
            child = children[i]
            if child.age >= child.min_age_before_death:
                if child.food_eaten_count < 1 or child.energy <= 0:
                    del children[i]

        # generate more food
        if food_to_generate > math.floor(food_to_generate / 2):
            food_to_generate -= math.floor(food_to_generate / 4)
        else:
            food_to_generate = 200

        food = create_food(food_to_generate, rect, buffer=10)

        for parent in parents:
            parent.coord = (random.randint(0, 800), rect.bottom)
            parent.reset_eaten()
            parent.mated = False
            
        for child in children:
            child.coord = (random.randint(0, 800), rect.top)
            child.reset_eaten()
            child.mated = False

        food_bar_amount_values[day] = len(food) / 20
        

        t_remaining = 15
        elapsed_time = 0
    
    if day == 20:
        values_bar_population_size = []
        for i in range(20):
            values_bar_population_size.append(0)

    if day == 70:
        avg_speed_values_line = []
        avg_speed_values_line_daily = []
        for i in range(70):
            avg_speed_values_line.append(0)
            avg_speed_values_line_daily.append(0)

    # ----- draw table -----
    data = [
        ["Day", "Time", "Male", "Female", "Food"],
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

    # ----- if no more entities hang ----- 
    if len(children) + len(parents) == 0:
        while True:
            time.sleep(0.0000000001)

dt = 0.1
cwin.startWin(do, 0.1)  