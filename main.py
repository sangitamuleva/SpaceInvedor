import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# set display
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space_bg.jpg')
# title and caption of window
pygame.display.set_caption("Space Invador")

icon = pygame.image.load('spaceship.png')

pygame.display.set_icon(icon)


# background music
mixer.music.load('background.mp3')
mixer.music.play(-1)
# player image

playerImg = pygame.image.load('launch.png')
playerX = 370
playerY = 480
playerX_change = 0

# Multiple enamy
enamyImg = []
enamyX = []
enamyY = []
enamyX_change = []
enamyY_change = []
no_of_enamy=6

for i in range(6):
    # enemy image
    enamyImg.append( pygame.image.load('invedor.png'))
    enamyX.append(random.randint(0, 730))
    enamyY.append(random.randint(50, 150))
    enamyX_change.append( 3)
    enamyY_change.append(40)

# bullet image
bulleImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10

bullet_state = "ready"

score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
# ready = cant see the bullet on the screen
# fire =bullet is moving

def show_score(x,y):
    score=font.render("Score :" + str(score_value) , True ,(255,255,255))
    screen.blit(score,(x,y))

# set image function
def player(x, y):
    screen.blit(playerImg, (x, y))


# set image function
def enamy(x, y,i):
    screen.blit(enamyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulleImg, (x + 16, y + 10))


def isCollision(enamyX, enamyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enamyX - bulletX, 2)) + (math.pow(enamyY - bulletY, 2)))

    if distance < 27:
        return True
    else:
        return False

game_over_font=pygame.font.Font('freesansbold.ttf',72)


def game_over_text():
    game_over = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (200, 200))
# game loop
running = True

while running:
    # fill color
    screen.fill((0, 0, 0))

    # if u want set bg
    screen.blit(background, (0, 0))

    # print(playerX)
    for e in pygame.event.get():
        # for close game
        if e.type == pygame.QUIT:
            running = False

        #     moving object
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                playerX_change = -5

            if e.key == pygame.K_RIGHT:
                playerX_change = 5

            if e.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                playerX_change = 0

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # boundary set for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730

    # boundary set for enemy movement multiple enamy
    for i in range(no_of_enamy):
        # game over condition
        if enamyY[i] > 350:
            for j in range(no_of_enamy):
                enamyY[j]=2000
            game_over_text()
            break
        enamyX[i] += enamyX_change[i]
        if enamyX[i] <= 0:
            enamyX_change[i] = 3
            enamyY[i] += enamyY_change[i]
        elif enamyX[i] >= 730:
            enamyX_change[i] = -3
            enamyY[i] += enamyY_change[i]

        collision = isCollision(enamyX[i], enamyY[i], bulletX, bulletY)
        if collision:
            collission_sound = mixer.Sound('explosion.wav')
            collission_sound.play()
            #     collision occured set bullet state and bullet cordinate
            bulletY = 480
            bullet_state="ready"
            score_value +=1
            enamyX[i] = random.randint(0, 730)
            enamyY[i] = random.randint(50, 150)
        enamy(enamyX[i], enamyY[i],i)

    # display image
    player(playerX, playerY)
    show_score(textX,textY)
    # if we changing anything on screen display need to update
    pygame.display.update()
