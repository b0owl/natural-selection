## DEMO CODE
## Dont run unless testing subject drawing funtionality
import pygame  # type: ignore
import sys, os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cwin import screen, startWin
from subjects import Subject

demo = Subject((150, 150), (0, 0, 0))  
demo2 = Subject((150, 150), (0, 255, 0)) 

def do(screen):
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    demo.move((dx, dy))
    demo.draw_circle(demo.color, 5, screen)
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    demo2.move((dx, dy))
    demo2.draw_circle(demo2.color, 5, screen)

startWin(do)
