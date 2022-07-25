import math 
import random

def RGB2HSV(r,g,b):
    """
    Conversion from RGB to HSV
    (https://www.had2know.org/technology/hsv-rgb-conversion-formula-calculator.html)
    """
    M = max(r,g,b)
    m = min(r,g,b)
    V = M/255
    if M > 0:
        S = 1-m/M
    elif M == 0:
        S = 0

    k = r-0.5*g-0.5*b
    q = math.sqrt(r*r+g*g+b*b-r*g-r*b-g*b)

    
    H = math.acos(k/q)
    if b > g:
        H = 2*math.pi-H
    
    H *= 180/math.pi
    return H,S,V

def HSV2RGB(h,s,v):
    """
    Conversion from HSV to RGB
    (https://www.had2know.org/technology/hsv-rgb-conversion-formula-calculator.html)
    """
    M = 255*v
    m = M*(1-s)

    k = abs((h/60) % 2 -1)
    #print((h/60) % 2)
    z = (M-m)*(1-k)
    h %= 360

    if 0 <= h and h < 60:
        r = M
        g = z+m 
        b = m 
    elif 60 <= h and h < 120:
        r = z+m 
        g = M 
        b = m 
    elif 120 <= h and h < 180:
        r = m 
        g = M 
        b = z+m
    elif 180 <= h and h < 240:
        r = m 
        g = z+m 
        b = M 
    elif 240 <= h and h < 300:
        r = z+m  
        g = m 
        b = M
    elif 300 <= h and h < 360:
        r = M 
        g = m 
        b = z+m

    return r,g,b

def BoxMullerNormal():
    u1 = random.random()
    u2 = random.random()
    return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)
    