import pygame, sys
from random import randint 
from particles import Particle, CheckCollision, UpdateCollision
from pygame import Color, mouse


size = width, height = 600,400

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode(size=size)
clock = pygame.time.Clock()

# Initialize game objects
pts = []
#for i in range(500):
#    pts.append(
#        Particle(randint(0,width),randint(0,height),5)
#    )

# Game loop
running = True
while running:

    # 60 FPS
    dt = clock.tick(120)/1000
    
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse.get_pressed()[0]:
                mx,my = mouse.get_pos()
                pts.append(
                    Particle(mx,my,5)
                )
    
    # Draw loop
    screen.fill(Color(0,0,0))
    for pt in pts:
        pt.draw(screen)

    pygame.display.flip()

    # Update particles
    for pt in pts:
        pt.update(dt)
        pt.apply_pbc(width,height)
    
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            if CheckCollision(pts[i],pts[j]):
                UpdateCollision(pts[i],pts[j])

