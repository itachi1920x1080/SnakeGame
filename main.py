import pygame
import sys


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
runing = True

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    screen.fill((0,0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
