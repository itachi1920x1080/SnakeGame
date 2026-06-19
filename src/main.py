import pygame
import sys
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
WIDTH = 800 #Width of the screen
HEIGHT = 600 #Height of the screen

screen = pygame.display.set_mode((WIDTH,HEIGHT))

try:
    background = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "background.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = None

def scale_image(img, target_width=None, target_height=None):
    if not img: return None
    w, h = img.get_size()
    if target_width and not target_height:
        target_height = int(h * (target_width / w))
    elif target_height and not target_width:
        target_width = int(w * (target_height / h))
    return pygame.transform.smoothscale(img, (target_width, target_height))

try:
    snake_head_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "snake_head.png")).convert_alpha()
    snake_head_img = scale_image(snake_head_img, target_width=35)
except:
    snake_head_img = None

try:
    snake_body_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "snake_body.png")).convert_alpha()
    snake_body_img = scale_image(snake_body_img, target_width=30)
except:
    snake_body_img = None

try:
    snake_tail_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "snake_tail.png")).convert_alpha()
    snake_tail_img = scale_image(snake_tail_img, target_width=30)
except:
    snake_tail_img = None

try:
    apple_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "apple.png")).convert_alpha()
    apple_img = scale_image(apple_img, target_width=30)
except:
    apple_img = None

try:
    snake_turn_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "snake_turn.png")).convert_alpha()
    snake_turn_img = scale_image(snake_turn_img, target_width=30)
except:
    snake_turn_img = None

try:
    menu_logo_img = pygame.image.load(os.path.join(BASE_DIR, "assets", "images", "menu_logo.png")).convert_alpha()
    menu_logo_img = scale_image(menu_logo_img, target_width=400)
except:
    menu_logo_img = None
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def load_high_score():
    try:
        with open(os.path.join(BASE_DIR, "score.txt"), "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(os.path.join(BASE_DIR, "score.txt"), "w") as f:
        f.write(str(score))

try:
    eat_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "eat.wav"))
except:
    eat_sound = None

game_over = False
paused = False
game_state = "menu"

# Snake
snake = [(400,300)]
dx = 30
dy = 0

snake_size = 30
base_speed = 5
speed = base_speed
snake_length = 1

#Food
food_size = 25
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
                dx, dy = 30, 0
                snake_length = 1
                score = 0
                speed = base_speed
                game_over = False
                game_state = "playing"
            if event.key == pygame.K_RETURN:
                if game_state == "menu":
                    # Reset game on start
                    snake = [(400, 300)]
                    dx, dy = 30, 0
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
        if menu_logo_img:
            rect = menu_logo_img.get_rect(center=(WIDTH//2, 150))
            screen.blit(menu_logo_img, rect.topleft)
        else:
            title = go_font.render("SNAKE GAME", True, (0, 255, 0))
            screen.blit(title, (250, 180))

        start = font.render("ENTER - Start", True, (255, 255, 255))
        exit_text = font.render("ESC - Exit", True, (255, 255, 255))

        screen.blit(start, (290, 250))
        screen.blit(exit_text, (300, 300))

    elif game_state == "playing" or game_state == "game_over":
        if game_state == "playing" and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dx=-30
                dy=0
            elif keys[pygame.K_RIGHT]:
                dx=30
                dy=0
            elif keys[pygame.K_UP]:
                dy=-30
                dx=0
            elif keys[pygame.K_DOWN]:
                dy=30
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
                if snake_head_img:
                    if dx == 30: angle = 0
                    elif dx == -30: angle = 180
                    elif dy == -30: angle = 90
                    elif dy == 30: angle = -90
                    else: angle = 0
                    
                    head_rotated = pygame.transform.rotate(snake_head_img, angle)
                    rect = head_rotated.get_rect(center=(segment[0] + snake_size//2, segment[1] + snake_size//2))
                    screen.blit(head_rotated, rect.topleft)
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], snake_size, snake_size))
            elif i == len(snake) - 1 and snake_tail_img and len(snake) > 1:
                prev_segment = snake[i-1]
                diff_x = prev_segment[0] - segment[0]
                diff_y = prev_segment[1] - segment[1]
                if diff_x > 0: angle = 0
                elif diff_x < 0: angle = 180
                elif diff_y < 0: angle = 90
                elif diff_y > 0: angle = -90
                else: angle = 0
                
                tail_rotated = pygame.transform.rotate(snake_tail_img, angle)
                rect = tail_rotated.get_rect(center=(segment[0] + snake_size//2, segment[1] + snake_size//2))
                screen.blit(tail_rotated, rect.topleft)
            else:
                if snake_body_img:
                    prev_segment = snake[i-1]
                    next_segment = snake[i+1]
                    
                    diff_x_prev = prev_segment[0] - segment[0]
                    diff_y_prev = prev_segment[1] - segment[1]
                    diff_x_next = next_segment[0] - segment[0]
                    diff_y_next = next_segment[1] - segment[1]
                    
                    if diff_x_prev == -diff_x_next and diff_y_prev == -diff_y_next:
                        # Moving straight
                        if diff_x_prev != 0: # Moving horizontally
                            body_rotated = snake_body_img
                        else: # Moving vertically
                            body_rotated = pygame.transform.rotate(snake_body_img, 90)
                        rect = body_rotated.get_rect(center=(segment[0] + snake_size//2, segment[1] + snake_size//2))
                        screen.blit(body_rotated, rect.topleft)
                    else:
                        # It's a turn
                        if 'snake_turn_img' in globals() and snake_turn_img:
                            if (diff_x_prev == 30 and diff_y_next == 30) or (diff_x_next == 30 and diff_y_prev == 30):
                                angle = 180  # Right and Down
                            elif (diff_x_prev == -30 and diff_y_next == 30) or (diff_x_next == -30 and diff_y_prev == 30):
                                angle = 90 # Left and Down
                            elif (diff_x_prev == -30 and diff_y_next == -30) or (diff_x_next == -30 and diff_y_prev == -30):
                                angle = 0 # Left and Up
                            elif (diff_x_prev == 30 and diff_y_next == -30) or (diff_x_next == 30 and diff_y_prev == -30):
                                angle = -90  # Right and Up
                            else:
                                angle = 0
                                
                            body_rotated = pygame.transform.rotate(snake_turn_img, angle)
                        else:
                            # fallback to straight body
                            if diff_x_prev != 0:
                                body_rotated = snake_body_img
                            else:
                                body_rotated = pygame.transform.rotate(snake_body_img, 90)
                        
                        rect = body_rotated.get_rect(center=(segment[0] + snake_size//2, segment[1] + snake_size//2))
                        screen.blit(body_rotated, rect.topleft)
                else:
                    pygame.draw.rect(screen, (0, 180, 0), (segment[0], segment[1], snake_size, snake_size))

        food_rect = pygame.Rect(food_x, food_y, food_size, food_size)
        if apple_img:
            rect = apple_img.get_rect(center=(food_x + food_size//2, food_y + food_size//2))
            screen.blit(apple_img, rect.topleft)
        else:
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
