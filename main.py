import pygame
import sys


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Player
player_x = 375
player_y = 275
player_size = 50
speed = 5


runing = True

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    # Keyvord input

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x-=speed
    elif keys[pygame.K_RIGHT]:
        player_x+=speed
    elif keys[pygame.K_UP]:
        player_y-=speed
    elif keys[pygame.K_DOWN]:
        player_y+=speed

    # draw
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0), pygame.Rect(player_x, player_y, player_size, player_size))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
