import random
import pygame

(WIDTH, HEIGHT) = (500, 750)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Colliders!')
SPACE_BACKGROUND = pygame.image.load('space.jpg')
SPACE_JET = pygame.image.load('space_jet.png')
ASTEROID = pygame.image.load('asteroid.png')
WHITE = (255, 255, 255)

jet_x, jet_y, px = 200, 590, 1
asteroid_start_y = -800
pygame.font.init()
FONT_LARGE = pygame.font.SysFont("Bahnschrift", 32)
FONT_SMALL = pygame.font.SysFont("Bahnschrift", 16)
HITBOX = 100


def main(x, y, vel):
    _x = random.randint(0, 406)
    _y = -800
    astDodged = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(2000)
        SCREEN.blit(SPACE_BACKGROUND, (0, 0))
        SCREEN.blit(SPACE_JET, (x, y))
        SCREEN.blit(ASTEROID, (_x, _y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if x - vel > 0:
                x -= vel
        if key[pygame.K_RIGHT]:
            if x + vel < WIDTH - 100:
                x += vel

        _y += vel
        rectJet = pygame.Rect(x, y, HITBOX, HITBOX)
        rectAst = pygame.Rect(_x, _y, HITBOX, HITBOX)

        if rectJet.colliderect(rectAst):
            running = False

        if _y >= HEIGHT:
            _y = asteroid_start_y
            _x = random.randint(0, 406)
            astDodged += 1

        astDodged_print = FONT_LARGE.render(f"{astDodged}", True, WHITE)
        SCREEN.blit(astDodged_print, (10, 10))
        CREDITS_1_print = FONT_SMALL.render(f"Created By Ivaylo Georgiev", True, WHITE)
        CREDITS_2_print = FONT_SMALL.render(f"© TU-VARNA 2023", True, WHITE)
        SCREEN.blit(CREDITS_1_print, (145, 705))
        SCREEN.blit(CREDITS_2_print, (180, 725))

        pygame.display.update()


main(jet_x, jet_y, px)
