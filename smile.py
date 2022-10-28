import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((211, 211, 211))

circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 1)

circle(screen, (139, 0, 0), (150, 170), 20)
circle(screen, (0, 0, 0), (150, 170), 20, 1)

circle(screen, (139, 0, 0), (250, 170), 15)
circle(screen, (0, 0, 0), (250, 170), 15, 1)

circle(screen, (0, 0, 0), (150, 170), 10)
circle(screen, (0, 0, 0), (250, 170), 7)

rect(screen, (0, 0, 0), (150, 230, 100, 20))

rect(screen, (0, 0, 0), (100, 120, 70, 10))
rect(screen, (0, 0, 0), (233, 140, 70, 10))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
