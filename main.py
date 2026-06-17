import pygame
import sys


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Player
snake_x = 375
snake_y = 275
snake_size = 50
speed = 5


runing = True

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    # Keyvord input

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_x-=speed
    elif keys[pygame.K_RIGHT]:
        snake_x+=speed
    elif keys[pygame.K_UP]:
        snake_y-=speed
    elif keys[pygame.K_DOWN]:
        snake_y+=speed  

    # draw
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0), pygame.Rect(snake_x, snake_y, snake_size, snake_size))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
