import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE
import time
import tkinter as tk
from tkinter import messagebox
from playsound import playsound

pygame.init()
pygame.mixer.init()
global addd,flag
addd = 20 
flag = True
x = 1200
y = 700
start_time = time.time()
scrn = pygame.display.set_mode((x, y))
pygame.display.set_caption('Pong Random')
display = pygame.display.set_mode((x, y))
pygame.display.set_caption("Bouncing Ball")

# Load and scale the image to fit the window
background_image = pygame.image.load("unnamed.png").convert()
background_image = pygame.transform.scale(background_image, (x, y))

# Set up ball properties
speed_change = 0.5
ball_radius = 20
ball_color = (0, 255, 0)  # Red
ball_speed = [0.5, 0.5]  # Initial speed in x and y directions

# paddle properties
paddle_height = 200
paddle_width = 20
paddle_color = (0, 0, 255)
paddle_color2 = (255, 0, 0)
paddle_position = [100, 350 - (paddle_height / 2)]
paddle_position2 = [1100, 350 - (paddle_height / 2)]

button_width = 300
button_height = 50

# Set up the initial position of the ball
ball_position = [x // 2, y // 2]

def move_up(paddle_position, pixels):
    paddle_position[1] -= pixels
    if paddle_position[1] <= 0:
        paddle_position[1] = 0

# paddle movement functions
def move_down(paddle_position, pixels):
    paddle_position[1] += pixels
    if paddle_position[1] >= (700 - paddle_height):
        paddle_position[1] = (700 - paddle_height)
        
        
def startgame():
    
    ready_button_pressed = False
    button_rect = pygame.Rect(x // 2 - 75, y // 2 - 25, 150, 50)
    global flag,addd
    flag=False 
    addd = 20
    while not ready_button_pressed:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                ready_button_pressed = True

        scrn.blit(background_image, (0, 0))
    
        button_rect = pygame.Rect((x - button_width) // 2, (y - button_height) // 2, button_width, button_height)
        pygame.draw.rect(scrn, (0, 255, 0), button_rect, )
        ready_text = font.render("press sapce when ready", True, (255, 255, 255))
        scrn.blit(ready_text, (button_rect.centerx - ready_text.get_width() // 2, button_rect.centery - ready_text.get_height() // 2))
        score(player_1_score, player_2_score)
        pygame.draw.rect(scrn, paddle_color, (int(paddle_position[0]), int(paddle_position[1]), paddle_width, paddle_height))
        pygame.draw.rect(
        scrn, paddle_color2, (int(paddle_position2[0]), int(paddle_position2[1]), paddle_width, paddle_height)
        )
         
        
        pygame.display.update()

font = pygame.font.Font(None, 36)

# sets the player scores
global player_1_score
global player_2_score
player_1_score = 0
player_2_score = 0

def score(player_1_score, player_2_score):
    if player_1_score == 10 or player_2_score == 10:
        if player_1_score > player_2_score:
            print("Player 1 WINS!")
            
            
        else:
            print("Player 2 WINS!")
            
        pygame.quit()
        exit()
    else:
        score_text = font.render(f"Player 1: {player_1_score}  Player 2: {player_2_score}", True, (255, 255, 255))
        scrn.blit(score_text, (x // 2 - score_text.get_width() // 2, 10))

status = True
startgame()
while status:
    for event in pygame.event.get():
        if event.type == QUIT:
            status = False

    # Draw background
    scrn.blit(background_image, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_up(paddle_position, 1)
    if keys[pygame.K_s]:
        move_down(paddle_position, 1)
    if keys[pygame.K_UP]:
        move_up(paddle_position2, 1)
    if keys[pygame.K_DOWN]:
        move_down(paddle_position2, 1)

    # Update ball position
    ball_position[0] += ball_speed[0]
    ball_position[1] += ball_speed[1]

    # Bounce off the walls
    # bounce off paddle
    paddles = [paddle_position, paddle_position2]
    if flag == True:
        addd = -20
    else:
        addd = 20
    for paddle in paddles:
        if (
            paddle[0] <= ball_position[0] + addd <= paddle[0] + paddle_width
            and paddle[1] <= ball_position[1] <= paddle[1] + paddle_height
        ):
            
            # Adjust ball speed
            speed_factor = 1.04
            ball_speed[0] *= -speed_factor + 0.02
            ball_speed[1] *= speed_factor
            flag = not flag
            pygame.mixer.Sound("blipSelect.wav").play()
    # left and right wall
    if ball_position[0] - ball_radius <= 0:
        pygame.mixer.Sound("explosion.wav").play()
        player_2_score += 1
        score(player_1_score, player_2_score)
        startgame()
        ball_speed[0] = 0.5
        ball_speed[1] = 0.5
        start_time = time.time()
        ball_position = [x // 2, y // 2]
        paddle_position = [100, 350 - (paddle_height / 2)]
        paddle_position2 = [1100, 350 - (paddle_height / 2)]
        score(player_1_score, player_2_score)

    elif ball_position[0] + ball_radius >= x:
        pygame.mixer.Sound("explosion.wav").play()
        player_1_score += 1
        startgame()
        score(player_1_score, player_2_score)
        ball_speed[0] = 0.5
        ball_speed[1] = 0.5
        start_time = time.time()
        ball_position = [x // 2, y // 2]
        paddle_position = [100, 350 - (paddle_height / 2)]
        paddle_position2 = [1100, 350 - (paddle_height / 2)]

        

    # top and bottom wall
    if ball_position[1] - ball_radius < 0 or ball_position[1] + ball_radius > y:
        ball_speed[1] = -ball_speed[1]
        pygame.mixer.Sound("blipSelectDeep.wav").play()
        

    # Draw the ball on top of the background
    score(player_1_score, player_2_score)
    pygame.draw.rect(scrn, paddle_color, (int(paddle_position[0]), int(paddle_position[1]), paddle_width, paddle_height))
    pygame.draw.rect(
        scrn, paddle_color2, (int(paddle_position2[0]), int(paddle_position2[1]), paddle_width, paddle_height)
    )
    pygame.draw.circle(scrn, ball_color, (int(ball_position[0]), int(ball_position[1])), ball_radius)

    # Draw player scores at the top of the window

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
