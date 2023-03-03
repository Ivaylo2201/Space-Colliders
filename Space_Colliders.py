
# TOP WHITE NUMBER - TOTAL DODGED ASTEROIDS
# TOP PURPLE NUMBER - TOTAL DESTROYED ASTEROIDS
# TOP RED NUMBER - CURRENT AMOUNT OF REMAINING ENERGY
# TOP ORANGE TEXT - CURRENT HIGHSCORE
# BOTTOM LEFT TEXT - CURRENT VERSION OF THE GAME
# BOTTOM MIDDLE TEXT - CREATOR & COPYRIGHT

# CONTROLS:
# LEFT -> LEFT ARROW
# RIGHT -> RIGHT ARROW
# SHOOT LASER -> SPACE

# DODGING 10 ASTEROIDS REFUNDS 250 ENERGY IF THE ENERGY
# WON'T SURPASS THE MAX ENERGY POSSIBLE, IN THE OTHER CASE
# SET THE ENERGY TO THE MAX ENERGY POSSIBLE

# Modules
import random
import time
import pygame
from pygame import mixer

mixer.init()
pygame.font.init()

# Setting display dimensions, caption and icon
(WIDTH, HEIGHT) = (500, 750)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Colliders!')
pygame.display.set_icon(pygame.image.load("asteroid.png"))

# Loading images
SPACE_BACKGROUND = pygame.image.load('space.jpg')
SPACE_JET = pygame.image.load('space_jet.png')
ASTEROID = pygame.image.load('asteroid.png')
LASER = pygame.image.load('laser.png')

# Loading sounds & setting their volumes
crash_sound = pygame.mixer.Sound('crash_sound.mp3')
dodge_sound = pygame.mixer.Sound('dodge_sound.mp3')
laser_sound = pygame.mixer.Sound('laser_sound.mp3')
bg_sound = pygame.mixer.Sound('bgMusic.mp3')
new_highscore_sound = pygame.mixer.Sound('new_highscore_sound.mp3')
new_highscore_voiceover = pygame.mixer.Sound('new_highscore_voiceover.mp3')
energy_refund_sound = pygame.mixer.Sound('energy_refund_sound.mp3')

crash_sound.set_volume(2.5)
dodge_sound.set_volume(1)
bg_sound.set_volume(0.5)
new_highscore_sound.set_volume(1.3)
new_highscore_voiceover.set_volume(0.7)
energy_refund_sound.set_volume(2)

# Defining colors & key attributes
WHITE = (255, 255, 255)
ORANGE = (255, 95, 31)
RED = (255, 0, 0)
DARK_RED = (151, 5, 29)
YELLOW = (255, 195, 0)
PURPLE = (148, 13, 198)

JET_X, JET_Y = 200, 590
MOVEMENT_PIXELS = 0.5
ASTEROID_START_Y = -800
HITBOX = 100
MAX_ENERGY = 1000
ENERGY_REFUND = 250
TICK_RATE = 2500

# Defining fonts
FONT_LARGE = pygame.font.SysFont('Bahnschrift', 32)
FONT_SMALL = pygame.font.SysFont('Bahnschrift', 16)


def main(x, y, vel):
    # Spawning the asteroid at a random X location
    asteroid_x = random.randint(0, 406)
    asteroid_y = ASTEROID_START_Y
    asteroids_dodged = 0
    asteroids_destroyed = 0
    new_highscore = True
    # Game speed
    clock = pygame.time.Clock()
    energy_available = MAX_ENERGY
    # Creating the file if it does not exist.
    open("highscores.txt", "a")

    running = True
    while running:
        # Reading the highscore & converting it to an integer
        highscores = open("highscores.txt", "r")
        highscoreINT = [int(x) for x in highscores.read().split()]
        if len(highscoreINT) > 0:
            highscore = max(highscoreINT)
        else:
            highscore = 0

        clock.tick(TICK_RATE)
        SCREEN.blit(SPACE_BACKGROUND, (0, 0))
        SCREEN.blit(SPACE_JET, (x, y))
        SCREEN.blit(ASTEROID, (asteroid_x, asteroid_y))
        HIGHSCORE = FONT_LARGE.render(f"{highscore}", True, ORANGE)
        SCREEN.blit(HIGHSCORE, (10, 100))

        # User quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Creating rectangles for the jet and the asteroids
        rectJet = pygame.Rect(x, y, HITBOX, HITBOX)
        rectAst = pygame.Rect(asteroid_x, asteroid_y, HITBOX, HITBOX)

        # Key pressing detection
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            # Moving the jet if possible
            if x - vel > 0:
                x -= vel

        if key[pygame.K_RIGHT]:
            # Moving the jet if possible
            if x + vel < WIDTH - 100:
                x += vel

        if key[pygame.K_SPACE]:
            # Checking if the jet can shoot a laser
            if energy_available > 0:
                SCREEN.blit(LASER, (x + 44.5, y - 90))
                pygame.mixer.Sound.play(laser_sound)
                rectLaser = pygame.Rect(x + 35, y - 90, 30, 15)
                energy_available -= 1

                # If the laser collides with an asteroid - destroy the asteroid
                if rectLaser.colliderect(rectAst):
                    asteroid_y = ASTEROID_START_Y
                    # Spawning the asteroid at a random X location
                    asteroid_x = random.randint(0, 406)
                    asteroids_destroyed += 1

                    if asteroids_destroyed > highscore:
                        if new_highscore:
                            laser_sound.stop()
                            pygame.mixer.Sound.play(new_highscore_sound)
                            pygame.mixer.Sound.play(new_highscore_voiceover)

                        add_highscore = open('highscores.txt', 'w')
                        add_highscore.write(str(asteroids_destroyed))
                        add_highscore.close()
                        new_highscore = False

        asteroid_y += vel

        # Checking if the jet has collided with an asteroid
        if rectJet.colliderect(rectAst):
            bg_sound.stop()
            laser_sound.stop()
            pygame.mixer.Sound.play(crash_sound)
            time.sleep(3)
            running = False

        # If the asteroid left the screen, add 1 point to dodged
        # asteroids and put the asteroid in its starting position
        if asteroid_y >= HEIGHT:
            pygame.mixer.Sound.play(dodge_sound)
            asteroid_y = ASTEROID_START_Y
            # Spawning the asteroid at a random X location
            asteroid_x = random.randint(0, 406)
            asteroids_dodged += 1

            if asteroids_dodged % 10 == 0:
                pygame.mixer.Sound.play(energy_refund_sound)
                if energy_available + ENERGY_REFUND <= MAX_ENERGY:
                    energy_available += ENERGY_REFUND
                else:
                    energy_available = MAX_ENERGY

        # Printing the amount of dodged asteroids, destroyed asteroids & energy left
        asteroids_dodged_counter = FONT_LARGE.render(f"{asteroids_dodged}", True, WHITE)
        asteroids_destroyed_counter = FONT_LARGE.render(f"{asteroids_destroyed}", True, PURPLE)
        energy_counter = FONT_LARGE.render(f"{format(energy_available, '.0f')}", True, DARK_RED)

        # Additional info
        credit_creator = FONT_SMALL.render(f"Created by Ivaylo Georgiev", True, WHITE)
        credit_copyright = FONT_SMALL.render(f"© TU-VARNA 2023", True, WHITE)
        current_version = FONT_SMALL.render("v1.3", True, WHITE)

        # / Different colors depending on the amount of dodged asteroids /
        if 20 <= asteroids_dodged < 35:
            asteroids_dodged_counter = FONT_LARGE.render(f"{asteroids_dodged}", True, YELLOW)
        elif 35 <= asteroids_dodged < 50:
            asteroids_dodged_counter = FONT_LARGE.render(f"{asteroids_dodged}", True, ORANGE)
        elif asteroids_dodged >= 50:
            asteroids_dodged_counter = FONT_LARGE.render(f"{asteroids_dodged}", True, RED)

        # Blitting the info
        SCREEN.blit(asteroids_dodged_counter, (10, 10))
        SCREEN.blit(asteroids_destroyed_counter, (10, 40))
        SCREEN.blit(energy_counter, (10, 70))
        SCREEN.blit(credit_creator, (150, 705))
        SCREEN.blit(credit_copyright, (185, 725))
        SCREEN.blit(current_version, (10, 725))

        # Updating the display every iteration
        pygame.display.update()


while True:
    # Background sound
    pygame.mixer.Sound.play(bg_sound)
    main(JET_X, JET_Y, MOVEMENT_PIXELS)
