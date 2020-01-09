import pygame
pygame.init()

screen = pygame.display.set_mode((250, 250))
pygame.display.set_caption("Key IDs")
screen.fill((255, 0, 0))
pygame.display.flip()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for key in range(0, len(pygame.key.get_pressed())):
        if pygame.key.get_pressed()[key] == 1:
            print(key)