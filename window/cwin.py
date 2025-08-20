import pygame  # type: ignore
import time 

pygame.init()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((900, 900), pygame.RESIZABLE)
pygame.display.set_caption('nats')  # natural selection
screen.fill(background_color)

running = True

def startWin(do, delay=0):  # main loop
    global running
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)
        do(screen)
        pygame.display.flip()
        clock.tick(60)

        time.sleep(delay)
