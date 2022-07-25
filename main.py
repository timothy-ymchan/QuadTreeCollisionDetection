import pygame, sys
from random import randint 
from particles import Particle, CheckCollision, UpdateCollision
from pygame import Color, mouse
from quadtree import Quadtree, Rectangle


size = width, height = 600,600

# Initialize pygame and screen
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size=size)
pygame.display.set_caption('2D n-body collision')
clock = pygame.time.Clock()

# Initialize game objects
pts = []
for i in range(500):
    pts.append(
        Particle(randint(10,width-10),randint(10,height-10),5)
    )
font = pygame.font.SysFont('Comic Sans MS',20)
quadtree_checker = True

# Game loop
running = True
while running:

    # 60 FPS
    dt = clock.tick(120)/1000
    
    # Event loop
    quadtree = Quadtree(Rectangle(0,0,width,height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse.get_pressed()[0]:
                mx,my = mouse.get_pos()
                pts.append(
                    Particle(mx,my,5)
                )
                #quadtree.insert(pts[-1])
            elif mouse.get_pressed()[2]:
                quadtree_checker  = not quadtree_checker 
            #elif mouse.get_pressed()[2]:
            #    mx,my = mouse.get_pos()
            #    box_checker.x, box_checker.y = mx-box_checker.w//2,my-box_checker.h//2

    pygame.display.flip()

    # Update particles
    for pt in pts:
        pt.update(dt)
        pt.apply_pbc(width,height)
        quadtree.insert(pt)

    if quadtree_checker:
        search_box = Rectangle(0,0,40,40)
        for pt1 in pts:
            search_box.x = pt1.x - search_box.w/2
            search_box.y = pt1.y - search_box.h/2
            for pt2 in quadtree.get_particle_in_rect(search_box):
                if CheckCollision(pt1,pt2) and pt1 != pt2:
                    UpdateCollision(pt1,pt2)
    else:
        for i in range(len(pts)):
            for j in range(i+1,len(pts)):
                if CheckCollision(pts[i],pts[j]):
                    UpdateCollision(pts[i],pts[j])

    # Draw loop
    screen.fill(Color(0,0,0))
    for pt in pts:
        pt.draw(screen)
    #quadtree.draw(screen)
    
    # Display collision check mode 
    mode = 'ON' if quadtree_checker else 'OFF'
    text_surf = font.render(f'QUADTREE: {mode}',True,(255,255,255))
    screen.blit(text_surf,(0,0))

    del quadtree
