import pygame
import random
import math

from pygame import mixer

pygame.init()

# create screen

screen = pygame.display.set_mode((800, 600))

# Background

bg = pygame.image.load('bg.png')  # background img
mixer.music.load('music.wav')
mixer.music.play(-1)

# title and icon

pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player

playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerimg, (x, y))  # draw


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
  enemyimg.append(pygame.image.load('enemy.png'))
  enemyX.append(random.randint(0, 735))  # to spawn in random places within the range mentioned
  enemyY.append(random.randint(20, 150))
  enemyX_change.append(2)
  enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # draw


# bullet

# ready means bullet isnt visible
# fire means its been fired and visible

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    s = font.render("Score :" + str(score), True, (250, 250, 0))
    screen.blit(s, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))  # inorder to shoot bullet from centre of spaceship


def iscollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if dist < 27:
        return True
    else:
        return False

# game loop

run = True
while run:

    # RGB values for screen bg

    screen.fill((0, 200, 10))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # To check Which aroow key is being pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX  # Gets the current co=ordinate of x value
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # To generate player ship

    playerX += playerX_change  # to change position of player

    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:                   # not 800 as our spaceship image size is 64 bits
        playerX = 735

    # enemy movement

    for i in range (no_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
          enemyX_change[i] = 2
          enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:                 # not 800 as our enemy image size is 64 bits
           enemyX_change[i] = -2
           enemyY[i] += enemyY_change[i]


           # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
               explosion_Sound = mixer.Sound('explosion.wav')
               explosion_Sound.play()
               bulletY = 480
               bullet_state = "ready"
               score += 1
               enemyX[i] = random.randint(0, 735)
               enemyY[i] = random.randint(20, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"  # To fire repeated bullets after one bullet reaches out of scope

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
