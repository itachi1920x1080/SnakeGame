import pygame
import sys
import random

pygame.init()
WIDTH = 800 #Width of the screen
HEIGHT = 600 #Height of the screen

screen = pygame.display.set_mode((WIDTH,HEIGHT))

try:
    background = pygame.image.load("assets/images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = None
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def load_high_score():
    try:
        with open("score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("score.txt", "w") as f:
        f.write(str(score))

try:
    eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
except:
    eat_sound = None

game_over = False
paused = False
game_state = "menu"

# Snake
snake = [(400,300)]
dx = 20
dy = 0

snake_size = 20
base_speed = 5
speed = base_speed
snake_length = 1

#Food
food_size = 20
food_x = random.randint(0, WIDTH - food_size)
food_y = random.randint(0, HEIGHT - food_size)

# score 
score = 0
high_score = load_high_score()

# Fonts
font = pygame.font.SysFont(None, 30)
go_font = pygame.font.SysFont(None, 50)


runing = True

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                runing = False
            if event.key == pygame.K_p and game_state == "playing":
                paused = not paused
            if event.key == pygame.K_r and game_state == "game_over":
                snake = [(400, 300)]
                dx, dy = 20, 0
                snake_length = 1
                score = 0
                speed = base_speed
                game_over = False
                game_state = "playing"
            if event.key == pygame.K_RETURN:
                if game_state == "menu":
                    # Reset game on start
                    snake = [(400, 300)]
                    dx, dy = 20, 0
                    snake_length = 1
                    score = 0
                    speed = base_speed
                    game_over = False
                    game_state = "playing"
                    paused = False
                elif game_state == "game_over":
                    game_state = "menu"
                    game_over = False
                    paused = False

    if background:
        screen.blit(background, (0,0))
    else:
        screen.fill((0,0,0))

    if game_state == "menu":
        title = go_font.render("SNAKE GAME", True, (0, 255, 0))
        start = font.render("ENTER - Start", True, (255, 255, 255))
        exit_text = font.render("ESC - Exit", True, (255, 255, 255))

        screen.blit(title, (250, 180))
        screen.blit(start, (290, 250))
        screen.blit(exit_text, (300, 300))

    elif game_state == "playing" or game_state == "game_over":
        if game_state == "playing" and not paused:
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

            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)
            snake.insert(0, new_head)
            
            if head_x < 0 or head_x>=WIDTH or head_y <0 or head_y>=HEIGHT:
                game_over = True
                game_state = "game_over"
            if snake[0] in snake[1:]:
                game_over = True
                game_state = "game_over"
            if len(snake) > snake_length:
                snake.pop()

            head_rect = pygame.Rect(snake[0][0],snake[0][1],snake_size,snake_size)
            food_rect = pygame.Rect(food_x, food_y,food_size, food_size)
            if head_rect.colliderect(food_rect):
                food_x = random.randint(0,WIDTH-food_size)
                food_y = random.randint(0,HEIGHT-food_size)
                snake_length += 1
                score += 1
                if eat_sound:
                    eat_sound.play()

        # draw
        for i, segment in enumerate(snake):
            if i == 0:
                color = (0, 255, 0)  # Head
            else:
                color = (0, 180, 0)  # Body
            pygame.draw.rect(
                screen,
                color,
                (segment[0], segment[1], 20, 20)
            )

        food_rect = pygame.Rect(food_x, food_y,food_size, food_size)
        pygame.draw.rect(screen, (255,0,0), food_rect)

        score_txt = font.render("Score : " +str(score),True,(255,255,255))
        screen.blit(score_txt,(10,10))
        
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (650, 10))

        help_text = font.render("P=Pause  R=Restart  ESC=Exit", True, (255, 255, 255))
        screen.blit(help_text, (10, 560))
        
        if paused:
            pause_text = font.render("PAUSED - Press P", True, (255, 255, 0))
            screen.blit(pause_text, (250, 250))
            
        if game_state == "game_over":
            if score > high_score:
                save_high_score(score)
                high_score = score
                
            over_text = go_font.render("GAME OVER", True, (255, 0, 0))
            score_text_go = font.render(f"Score: {score}", True, (255, 255, 255))
            high_text = font.render(f"High Score: {high_score}", True, (255, 215, 0))
            restart_text = font.render("Press R to Restart", True, (200, 200, 200))
            menu_text = font.render("Press ENTER for Menu", True, (200, 200, 200))

            screen.blit(over_text, (270, 200))
            screen.blit(score_text_go, (300, 250))
            screen.blit(high_text, (300, 300))
            screen.blit(restart_text, (300, 350))
            screen.blit(menu_text, (270, 400))
    
    pygame.display.update()
    
    speed = base_speed + (score // 3)
    clock.tick(speed)

pygame.quit()
sys.exit()
