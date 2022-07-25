import pygame
from pygame.draw import circle
import random
import math
from utils import HSV2RGB, BoxMullerNormal


class Particle:
    def __init__(self,x,y,a):
        self.x = x
        self.y = y
        self.a = a
        self.color = [int(val) for val in HSV2RGB(random.randint(0,360),1,1)]
        #print(self.color)
        self.vx = 50*BoxMullerNormal()
        self.vy = 50*BoxMullerNormal()

    def draw(self,screen):
        circle(
            surface=screen,
            color=self.color,
            center=(self.x,self.y),
            radius=self.a,width=0)
    
    def update(self,dt):
        self.x  += self.vx *dt
        self.y  += self.vy *dt
    
    def apply_pbc(self,width,height):
        self.x %= width
        self.y %= height

def CheckCollision(part1, part2):
    d2 = (part1.x - part2.x)**2 + (part1.y-part2.y)**2
    s2 = (part1.a + part2.a)**2
    if d2 < s2:
        return True
    return False 

def UpdateCollision(part1,part2):
    # Normal vector 
    nx = part2.x-part1.x
    ny = part2.y-part1.y
    n2 = nx*nx + ny*ny
    n  = math.sqrt(n2)
    
    # Project velocity 
    dot1 = nx*part1.vx + ny*part1.vy
    dot2 = nx*part2.vx + ny*part2.vy

    vproj1x,vproj1y = nx*dot1/n2, ny*dot1/n2
    vproj2x,vproj2y = nx*dot2/n2, ny*dot2/n2

    # Update velocity
    #print('Before: ', part1.vx**2 + part1.vy**2 + part2.vx**2 + part2.vy**2)
    part1.vx += -vproj1x + vproj2x
    part1.vy += -vproj1y + vproj2y
    part2.vx += +vproj1x - vproj2x
    part2.vy += +vproj1y - vproj2y
    #print('After: ', part1.vx**2 + part1.vy**2 + part2.vx**2 + part2.vy**2)

    # Final seperation vector 
    a = 1.0*(part1.a + part2.a)
    ax = nx*a/n
    ay = ny*a/n
    #print(ax*ax+ay*ay)

    # Displace particles so that CM unchange (Assume equal mass)
    part1.x += 0.5*(nx-ax)
    part1.y += 0.5*(ny-ay)
    part2.x -= 0.5*(nx-ax)
    part2.y -= 0.5*(ny-ay)
