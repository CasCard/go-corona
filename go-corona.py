import pygame
import random
import os
import time

# pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

win = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Go-corona")

walkRight = [pygame.image.load('assets/images/R1.png'), pygame.image.load('assets/images/R2.png'),
             pygame.image.load('assets/images/R3.png'),
             pygame.image.load('assets/images/R4.png'), pygame.image.load('assets/images/R5.png'),
             pygame.image.load('assets/images/R6.png'),
             pygame.image.load('assets/images/R7.png'), pygame.image.load('assets/images/R8.png'),
             pygame.image.load('assets/images/R9.png')]
walkLeft = [pygame.image.load('assets/images/L1.png'), pygame.image.load('assets/images/L2.png'),
            pygame.image.load('assets/images/L3.png'),
            pygame.image.load('assets/images/L4.png'), pygame.image.load('assets/images/L5.png'),
            pygame.image.load('assets/images/L6.png'),
            pygame.image.load('assets/images/L7.png'), pygame.image.load('assets/images/L8.png'),
            pygame.image.load('assets/images/L9.png')]
bg = pygame.image.load('assets/images/bg.png')
char = pygame.image.load('assets/images/standing.png')
banner=pygame.image.load('assets/images/break_the_chain.png')
bulletImage=pygame.image.load('assets/images/bullet.png')


clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('assets/audio/bullet.ogg')
hitSound = pygame.mixer.Sound('assets/audio/hit.ogg')
music = pygame.mixer.music.load('assets/audio/music.ogg')
pygame.mixer.music.play(-1)
score = 0


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 25
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = False
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win,(255,0,0),self.hitbox,2)

        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if (self.right):
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 370
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 50)
        text = font1.render('Maintain Social distancing', 1, (255, 0, 0))
        win.blit(text, (400 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y,radius,facing):
        self.x = x
        self.y = y
        self.radius=radius
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self):
        win.blit(bulletImage, (self.x, self.y))


class enemy(object):
    walkRight = [pygame.image.load('assets/images/R1E.png'), pygame.image.load('assets/images/R2E.png'),
                 pygame.image.load('assets/images/R3E.png'),
                 pygame.image.load('assets/images/R4E.png'), pygame.image.load('assets/images/R5E.png'),
                 pygame.image.load('assets/images/R6E.png'),
                 pygame.image.load('assets/images/R7E.png'), pygame.image.load('assets/images/R8E.png'),
                 pygame.image.load('assets/images/R9E.png'),
                 pygame.image.load('assets/images/R10E.png'), pygame.image.load('assets/images/R11E.png')]
    walkLeft = [pygame.image.load('assets/images/L1E.png'), pygame.image.load('assets/images/L2E.png'),
                pygame.image.load('assets/images/L3E.png'),
                pygame.image.load('assets/images/L4E.png'), pygame.image.load('assets/images/L5E.png'),
                pygame.image.load('assets/images/L6E.png'),
                pygame.image.load('assets/images/L7E.png'), pygame.image.load('assets/images/L8E.png'),
                pygame.image.load('assets/images/L9E.png'),
                pygame.image.load('assets/images/L10E.png'), pygame.image.load('assets/images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.velocity = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

        if self.velocity > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(win, (255, 0, 0),self.hitbox, 2)

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    win.blit(banner,(10,10))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (350, 10))
    man.draw(win)
    corona.draw(win)
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)

man = player(200, 370, 64, 64)
corona = enemy(100, 370, 64, 64, 780)
shootLoop = 0
bullets = []
run = True

while run:
    clock.tick(27)

    if corona.visible == True:
        if man.hitbox[1] < corona.hitbox[1] + corona.hitbox[3] and man.hitbox[1] + man.hitbox[3] > corona.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > corona.hitbox[0] and man.hitbox[0] < corona.hitbox[0] + corona.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1

    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < corona.hitbox[1] + corona.hitbox[3] and bullet.y + bullet.radius > corona.hitbox[
            1]:
            if bullet.x + bullet.radius > corona.hitbox[0] and bullet.x - bullet.radius < corona.hitbox[0] + \
                    corona.hitbox[2]:
                hitSound.play()
                corona.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.width // 2),6, facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 800 - man.velocity - man.width:
        man.x += man.velocity
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
