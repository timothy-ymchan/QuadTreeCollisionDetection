import pygame

class Rectangle:
    def __init__(self,x,y,w,h):
        self.x = x 
        self.y = y 
        self.w = w 
        self.h = h 

def in_rect(point, rect):
    """
    Check if point is inside rectangle
    """
    return (0 <= point.x - rect.x) and (point.x - rect.x < rect.w) and (0 <= point.y - rect.y) and (point.y-rect.y < rect.h)

def rect_intersect(rect1,rect2):
    if rect2.x >= rect1.x:
        rect_x1 = rect1
        rect_x2 = rect2
    else:
        rect_x1 = rect2
        rect_x2 = rect1
    
    if rect2.y >= rect1.y:
        rect_y1 = rect1
        rect_y2 = rect2
    else:
        rect_y1 = rect2
        rect_y2 = rect1
    return (rect_x2.x - rect_x1.x <= rect_x1.w) and (rect_y2.y-rect_y1.y <= rect_y1.h)



class Quadtree:
    def __init__(self,box,cap=4,depth=0):
        self.box = box
        self.cap = cap
        self.points = []
        self.point_count = 0
        self.nodes = {}
        self.depth = depth
    
    def __del__(self):
        # Remove everything except the points
        del self.box
        for _, node in self.nodes.items():
            del node
    
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),
                        pygame.Rect(self.box.x,self.box.y,self.box.w,self.box.h),
                        width=1)
        for _, node in self.nodes.items():
            node.draw(screen)    
    
    def insert(self,point):
        self.points.append(point)
        self.point_count += 1 # Count all points under the box

        if self.point_count > self.cap:
            # Create a new layer of recursion and transfer the points to child

            # If no child, create child
            if len(self.nodes.keys()) == 0:
                x,y,w,h = self.box.x, self.box.y, self.box.w, self.box.h
                self.nodes['NW'] = Quadtree(Rectangle(x,y,w/2,h/2),cap=self.cap,depth=self.depth+1)
                self.nodes['NE'] = Quadtree(Rectangle(x+w/2,y,w/2,h/2),cap=self.cap,depth=self.depth+1)
                self.nodes['SW'] = Quadtree(Rectangle(x,y+h/2,w/2,h/2),cap=self.cap,depth=self.depth+1)
                self.nodes['SE'] = Quadtree(Rectangle(x+w/2,y+h/2,w/2,h/2),cap=self.cap,depth=self.depth+1)

            # Recursive insert
            inserted = False
            for pt in self.points:
                for key, node in self.nodes.items():
                    if in_rect(pt,node.box):
                        node.insert(pt)
                        inserted = True
                        break
                assert inserted == True, f'Error: Point {pt} cannot be inserted for some reason'
            
            self.points = []

    def get_particle_in_rect(self,rect):
        queue = [self]
        result = []
        while len(queue) != 0:
            entry = queue.pop(0)
            if rect_intersect(entry.box,rect):
                if len(entry.nodes.keys()) == 0:
                   for pt in entry.points:
                     if in_rect(pt,rect):
                        result.append(pt)
                else:
                    for _,node in entry.nodes.items():
                        queue.append(node)
        return result

    