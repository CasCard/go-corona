
import pygame
import random
import os
pygame.init()

win=pygame.display.set_mode((500,500))

pygame.display.set_caption("go-corona")

x=50
y=50
width=30
height=60
velocity=5

run=True
while run:
    pygame.time.delay(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x>velocity:
        x-=velocity
    if keys[pygame.K_RIGHT] and x<500-width:
        x+=velocity
    if keys[pygame.K_UP]:
        y-= velocity
    if keys[pygame.K_DOWN]:
        y+= velocity

    win.fill((0,209,143))
    pygame.draw.rect(win,(255,0,0),(x,y,width,height))


    pygame.display.update()

pygame.quit()


