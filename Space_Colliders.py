# Modules
import random
import time
import pygame
from pygame import mixer

mixer.init()
pygame.font.init()

# Setting display dimensions
(WIDTH, HEIGHT) = (500, 750)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Colliders! v1.1')

# Loading images
SPACE_BACKGROUND = pygame.image.load('space.jpg')
SPACE_JET = pygame.image.load('space_jet.png')
ASTEROID = pygame.image.load('asteroid.png')

# Loading sounds & setting their volume
crash_sound = pygame.mixer.Sound('crash_sound.mp3')
dodge_sound = pygame.mixer.Sound('dodge_sound.mp3')
bg_sound = pygame.mixer.Sound('bgMusic.mp3')

crash_sound.set_volume(2.5)
dodge_sound.set_volume(1)
bg_sound.set_volume(0.5)

# Defining key attributes
WHITE = (255, 255, 255)
ORANGE = (255, 95, 31)
RED = (255, 0, 0)
YELLOW = (255, 195, 0)
jet_x, jet_y, px = 200, 590, 0.5
ASTEROID_START_Y = -800
HITBOX = 100

# Defining fonts
FONT_LARGE = pygame.font.SysFont('Bahnschrift', 32)
FONT_SMALL = pygame.font.SysFont('Bahnschrift', 16)


def main(x, y, vel):
    # Spawning the asteroid at a random X location
    _x = random.randint(0, 406)
    _y = -800
    astDodged = 0
    # Game speed
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(2500)
        SCREEN.blit(SPACE_BACKGROUND, (0, 0))
        SCREEN.blit(SPACE_JET, (x, y))
        SCREEN.blit(ASTEROID, (_x, _y))

        # User quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Key pressing detection
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            # Moving the jet if possible
            if x - vel > 0:
                x -= vel
        if key[pygame.K_RIGHT]:
            if x + vel < WIDTH - 100:
                x += vel

        _y += vel
        rectJet = pygame.Rect(x, y, HITBOX, HITBOX)
        rectAst = pygame.Rect(_x, _y, HITBOX, HITBOX)

        # Checking if the jet collided with an asteroid
        if rectJet.colliderect(rectAst):
            bg_sound.stop()
            pygame.mixer.Sound.play(crash_sound)
            time.sleep(3)
            running = False

        # If the asteroid left the screen, add 1 point to dodged
        # asteroids and put the asteroid in its starting position
        if _y >= HEIGHT:
            pygame.mixer.Sound.play(dodge_sound)
            _y = ASTEROID_START_Y
            # Spawning the asteroid at a random X location
            _x = random.randint(0, 406)
            astDodged += 1

        # Printing the amount of dodged asteroids and some more info
        astDodged_print = FONT_LARGE.render(f"{astDodged}", True, WHITE)
        if 20 <= astDodged < 35:
            astDodged_print = FONT_LARGE.render(f"{astDodged}", True, YELLOW)
        elif 35 <= astDodged < 50:
            astDodged_print = FONT_LARGE.render(f"{astDodged}", True, ORANGE)
        elif astDodged >= 50:
            astDodged_print = FONT_LARGE.render(f"{astDodged}", True, RED)

        SCREEN.blit(astDodged_print, (10, 10))
        CREDITS_1_print = FONT_SMALL.render(f"Created by Ivaylo Georgiev", True, WHITE)
        CREDITS_2_print = FONT_SMALL.render(f"© TU-VARNA 2023", True, WHITE)
        SCREEN.blit(CREDITS_1_print, (150, 705))
        SCREEN.blit(CREDITS_2_print, (185, 725))

        # Updating the display every iteration
        pygame.display.update()


while True:
    pygame.mixer.Sound.play(bg_sound)
    main(jet_x, jet_y, px)
