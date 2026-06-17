import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game_over = False

# Snake
snake = [(400,300)]
dx = 20
dy =0

snake_size = 20
# speed = 2
snake_length = 1

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
        dx=-20
        dy=0
    elif keys[pygame.K_RIGHT]:
        dx=20
        dy=0
    elif keys[pygame.K_UP]:
        dy=-20
        dx=0
    elif keys[pygame.K_DOWN]:
        dy=20
        dx=0


    if not game_over:
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)
        snake.insert(0, new_head)
        
        if head_x < 0 or head_x>=WIDTH or head_y <0 or head_y>=HEIGHT:
            game_over = True
        if snake[0] in snake[1:]:
            game_over = True
        if len(snake) > snake_length:
            snake.pop()
    else:
        if keys[pygame.K_r]:
            game_over = False
            snake = [(400, 300)]
            dx = 20
            dy = 0
            snake_length = 1
            score = 0

    # draw
    screen.fill((0,0,0))
    for segment in snake:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (segment[0], segment[1], 20, 20)
        )

    food_rect = pygame.Rect(food_x, food_y,food_size, food_size)
    pygame.draw.rect(screen, (255,0,0), food_rect)

    head_rect = pygame.Rect(snake[0][0],snake[0][1],snake_size,snake_size)
    if not game_over and head_rect.colliderect(food_rect):
        food_x = random.randint(0,WIDTH-food_size)
        food_y=random.randint(0,HEIGHT-food_size)
        snake_length+=1
        score += 1
        print("Yum Yum ")
    
    font = pygame.font.SysFont(None,30)
    score_txt = font.render("Score : " +str(score),True,(255,255,255))
    screen.blit(score_txt,(10,10))
    
    
    pygame.display.update()
    clock.tick(15)

pygame.quit()
sys.exit()
