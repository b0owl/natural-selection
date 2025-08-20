import pygame  # type: ignore

pygame.init()

background_color = (255, 255, 255)
screen = pygame.display.set_mode((300, 300))
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
