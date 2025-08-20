## DEMO CODE
## Dont run unless testing subject drawing functionality
import pygame  # type: ignore
import sys, os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cwin import screen, startWin
from subjects import Parent, Child

try:
    os.system('cls')
except:
    os.system('clear')

# Create parents
parents = [
    Parent((150, 150), (255, 255, 255), speed=50, friendliness=0.5, aggression=0.5, mut_rate=0.1, pot_offspring=3),
    Parent((200, 150), (255, 255, 255), speed=60, friendliness=0.3, aggression=0.7, mut_rate=0.2, pot_offspring=4),
    Parent((250, 150), (255, 255, 255), speed=40, friendliness=0.7, aggression=0.4, mut_rate=0.05, pot_offspring=2)
]

# Create children from parents
children = [
    Child(parents[0], (0, 255, 0)),
    Child(parents[1], (0, 255, 0)),
    Child(parents[2], (0, 255, 0)),
]

# For printing
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

for idx, parent in enumerate(parents, start=1):
    print(f"\033[95m[PARENT{idx}] speed={parent.speed}, friendliness={parent.friendliness:.2f}, "
          f"aggression={parent.aggression:.2f}, mut_rate={parent.mut_rate:.2f}, "
          f"pot_offspring={parent.pot_offspring}\033[0m")

for idx, child in enumerate(children, start=1):
    print(f"\033[93m[CHILD{idx}] speed={child.speed}, friendliness={child.friendliness:.2f}, "
          f"aggression={child.aggression:.2f}, mut_rate={child.mut_rate:.2f}, "
          f"pot_offspring={child.pot_offspring}")

def do(screen):
    for parent in parents:
        dx = random.randint(-1, 5)
        dy = random.randint(-1, 5)
        parent.move((dx, dy))
        parent.draw_circle(parent.color, 10, screen)

    for child in children:
        dx = random.randint(-1, 5)
        dy = random.randint(-1, 5)
        child.move((dx, dy))
        child.draw_circle(child.color, 8, screen)


startWin(do)
