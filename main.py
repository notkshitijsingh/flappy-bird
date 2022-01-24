#importing modules
import pygame
import sys
import random

#functions
def game_floor():
    screen.blit(floor_base, (floor_x_pos, 450))
    screen.blit(floor_base, (floor_x_pos + 283.5, 450))

def background_moving():
    screen.blit(background, (background_x_pos, 0))
    screen.blit(background, (background_x_pos + 283.5, 0))

def check_collision(pipes):
    #check if pipe is hit
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    #check if floor is hit
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        die_sound.play()
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipe_pos-150))
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1.5

    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

#initialising pygame
pygame.init()
clock = pygame.time.Clock()

#importing assets
screen = pygame.display.set_mode((283.5, 512))
background = pygame.image.load("assets/background-day.png").convert()
bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
floor_base = pygame.image.load("assets/base.png").convert()
message = pygame.image.load("assets/message.png").convert_alpha()

jump_sound = pygame.mixer.Sound("sounds/jump.wav")
die_sound = pygame.mixer.Sound("sounds/die.wav")

#variables
gravity = 0.125

bird_movement = 0
bird_rect = bird.get_rect(center = (50, 256))

floor_x_pos = 0
background_x_pos = 0

game_active = True
game_over_rect = message.get_rect(center = (141.75, 256))

#building pipes
pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

#setting up a loop for the window
while True:
    for event in pygame.event.get():
        #setting up a quit case
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #setting up a playing case
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and game_active:
            bird_movement = 0
            bird_movement -= 3.5
            jump_sound.play()
        if pressed[pygame.K_SPACE] and not game_active:
            bird_rect.center = (50,256)
            bird_movement = 0
            pipe_list.clear()
            game_active = True
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
#making the game work
    #creating the background
    background_x_pos -= 0.125
    background_moving()

    if background_x_pos <= -283.5:
        background_x_pos = 0
    #running loop on game
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        #draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        #check for collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, (game_over_rect))
    #creating the floor
    floor_x_pos -= 0.5
    game_floor()

    if floor_x_pos <= -283.5:
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(120)
