from entities import subjects
import random
import math
import cwin 
import pygame 

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

parents = create_parents(12, 5, 0.3, 0.3, 2, 0.5, 0.1) # sorry for the magic numbers lmao

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


rect = pygame.Rect(20, 100, 1500, 800)
food = create_food(3, rect, buffer=10)

def do(screen):
    #---------------#
    # vvvvvvvvvvvvv #
    # SET VARIABLES #
    # ^^^^^^^^^^^^^ #
    #---------------#

    rect = pygame.Rect(20, 100, 1500, 800)  # boundary box
    color = (255, 255, 255)                 # white
    buffer = 10
    # draw the rectangle outline
    pygame.draw.rect(screen, color, rect, width=2)

    #----------------------#
    # vvvvvvvvvvvvvvvvvvvv #
    # DRAW PARENT/CHILDREN #
    # ^^^^^^^^^^^^^^^^^^^^ #
    #----------------------#

    for parent in parents:
        dx = parent.speed * random.uniform(-50, 50) 
        dy = parent.speed * random.uniform(-50, 50) 
        parent.move((dx, dy))

        # clamp to rectangle bounds
        x, y = parent.coord
        x = max(rect.left, min(x, rect.right)) 
        y = max(rect.top,  min(y, rect.bottom)) 
        parent.coord = (x, y)

        parent.draw(parent.color, 10, screen)
        
    for child in children:
        dx = child.speed * random.uniform(-50, 50) 
        dy = child.speed * random.uniform(-50, 50)
        child.move((dx, dy))

        # clamp to rectangle bounds
        x, y = child.coord
        x = max(rect.left + buffer, min(x, rect.right - buffer))
        y = max(rect.top  + buffer, min(y, rect.bottom - buffer))
        child.coord = (x, y)

        child.draw(child.color, 8, screen)
    

    for f in food:
        f.draw(screen)


    #------------#
    # vvvvvvvvvv #
    # DRAW TABLE #
    # ^^^^^^^^^^ #
    #------------#

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

    table_x, table_y = 1530, 100  

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
            pygame.draw.rect(screen, (255, 255, 255), cell_rect, 2)  # outline
            text_surf = font.render(str(value), True, (255, 255, 255))
            screen.blit(text_surf, (table_x + j * cell_width + 5, table_y + i * cell_height + 5))


cwin.startWin(do)
