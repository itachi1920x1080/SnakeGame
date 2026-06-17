import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Snake
snake_x = 375
snake_y = 275
snake_size = 50
speed = 5

#Food
food_size = 20
food_x=random.randint(0,WIDTH-food_size)
food_y=random.randint(0,HEIGHT-food_size)

# score 
score = 0


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
    snake_rect= pygame.Rect(snake_x, snake_y,snake_size, snake_size)
    pygame.draw.rect(screen,(0,255,0),snake_rect)

    food_rect = pygame.Rect(food_x, food_y,food_size, food_size)
    pygame.draw.rect(screen, (255,0,0), food_rect)
    if snake_rect.colliderect(food_rect):
        food_x = random.randint(0,WIDTH-food_size)
        food_y=random.randint(0,HEIGHT-food_size)
        speed+=1
        score += 1
        print("Yum Yum ")

    font = pygame.font.SysFont(None,30)
    score_txt = font.render("Score : " +str(score),True,(255,255,255))
    screen.blit(score_txt,(10,10))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
