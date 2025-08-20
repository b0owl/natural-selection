import pygame  # type: ignore
import os

# Set window position before creating it
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"

pygame.init()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((1030, 1000))
pygame.display.set_caption('nats')  # natural selection
screen.fill(background_color)

running = True

def startWin(do):  # main loop
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
