##########################################################
#                                                        #
#     Developed by Cavad, Leyla, Tofik, Omer             #
#                                                        #
##########################################################

import random
import math
import pygame
from pygame import mixer

pygame.init()    # Intialize the pygame

screen = pygame.display.set_mode((800, 600))  # create the screen

background = pygame.image.load('Space Game Pygame V1/image/background.png')



# Caption and Icon
pygame.display.set_caption("Space Game Pygame V1")
icon = pygame.image.load('Space Game Pygame V1/image/ufo.png')
pygame.display.set_icon(icon)

# oyuncu
oyuncuImg = pygame.image.load('Space Game Pygame V1/image/player.png')
oyuncuX = 370
oyuncuY = 480
oyuncuX_change = 0

# dusmen
dusmenImg = []
dusmenX = []
dusmenY = []
dusmenX_change = []
dusmenY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    dusmenImg.append(pygame.image.load('Space Game Pygame V1/image/enemy.png'))
    dusmenX.append(random.randint(0, 736))
    dusmenY.append(random.randint(50, 150))
    dusmenX_change.append(4)
    dusmenY_change.append(40)

# Ready - You can't see the raket on the screen
# Fire - The raket is currently moving

raketImg = pygame.image.load('Space Game Pygame V1/image/bullet.png')
raketX = 0
raketY = 480
raketX_change = 0
raketY_change = 10
raket_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def xal_hesabla(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (225, 250))


def oyuncu(x, y):
    screen.blit(oyuncuImg, (x, y))


def dusmen(x, y, i):
    screen.blit(dusmenImg[i], (x, y))


def fire_raket(x, y):
    global raket_state
    raket_state = "fire"
    screen.blit(raketImg, (x + 16, y + 10))


def isCollision(dusmenX, dusmenY, raketX, raketY):
    distance = math.sqrt(math.pow(dusmenX - raketX, 2) + (math.pow(dusmenY - raketY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Oyunun esas dovru burdadi
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))         # Background Image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                oyuncuX_change = -5
            if event.key == pygame.K_RIGHT:
                oyuncuX_change = 5
            if event.key == pygame.K_SPACE:
                if raket_state is "ready":
                    mixer.Sound("Space Game Pygame V1/sound/lazer.wav").play()
                    # Get the current x cordinate of the spaceship
                    raketX = oyuncuX
                    fire_raket(raketX, raketY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                oyuncuX_change = 0

    oyuncuX += oyuncuX_change
    if oyuncuX <= 0:
        oyuncuX = 0
    elif oyuncuX >= 736:
        oyuncuX = 736

    # dusmen Movement
    for i in range(num_of_enemies):

        # Game Over
        if dusmenY[i] > 440:
            for j in range(num_of_enemies):
                dusmenY[j] = 2000
            game_over_text()
            break

        dusmenX[i] += dusmenX_change[i]
        if dusmenX[i] <= 0:
            dusmenX_change[i] = 4
            dusmenY[i] += dusmenY_change[i]
        elif dusmenX[i] >= 736:
            dusmenX_change[i] = -4
            dusmenY[i] += dusmenY_change[i]

        # Collision
        collision = isCollision(dusmenX[i], dusmenY[i], raketX, raketY)
        if collision:
            mixer.Sound("Space Game Pygame V1/sound/explosion.wav").play()
            raketY = 480
            raket_state = "ready"
            score_value += 1
            dusmenX[i] = random.randint(0, 736)
            dusmenY[i] = random.randint(50, 150)

        dusmen(dusmenX[i], dusmenY[i], i)

    # raket Movement
    if raketY <= 0:
        raketY = 480
        raket_state = "ready"

    if raket_state is "fire":
        fire_raket(raketX, raketY)
        raketY -= raketY_change

    oyuncu(oyuncuX, oyuncuY)
    xal_hesabla(textX, testY)
    pygame.display.update()