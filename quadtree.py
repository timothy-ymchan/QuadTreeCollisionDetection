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


class Quadtree:
    def __init__(self,box,cap=4,depth=0):
        self.box = box
        self.cap = cap
        self.points = []
        self.point_count = 0
        self.nodes = {}
        self.depth = depth
    
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),
                        pygame.Rect(self.box.x,self.box.y,self.box.w,self.box.h),
                        width=1)
        for _, node in self.nodes.items():
            node.draw(screen)    
    
    def insert(self,point):
        lv_sep = '--'*self.depth
        self.points.append(point)
        self.point_count += 1 # Count all points under the box

        print(f'{lv_sep}Points list: ',self.points)
        if self.point_count > self.cap:
            # Create a new layer of recursion and transfer the points to child
            print(f'{lv_sep}Recursion!!')
            # If no child, create child
            if len(self.nodes.keys()) == 0:
                x,y,w,h = self.box.x, self.box.y, self.box.w, self.box.h
                self.nodes['NW'] = Quadtree(Rectangle(x,y,w/2,h/2),depth=self.depth+1)
                self.nodes['NE'] = Quadtree(Rectangle(x+w/2,y,w/2,h/2),depth=self.depth+1)
                self.nodes['SW'] = Quadtree(Rectangle(x,y+h/2,w/2,h/2),depth=self.depth+1)
                self.nodes['SE'] = Quadtree(Rectangle(x+w/2,y+h/2,w/2,h/2),depth=self.depth+1)
                print(f'{lv_sep}Created new subtrees')

            # Recursive insert
            inserted = False
            print(f'{lv_sep}Recursive insert: ')
            for pt in self.points:
                print(f'{lv_sep}Point: ',pt)
                for key, node in self.nodes.items():
                    print(f'{lv_sep}\tkey: ',key,'in box ',in_rect(pt,node.box))
                    if in_rect(pt,node.box):
                        node.insert(pt)
                        inserted = True
                        break
                assert inserted == True, f'Error: Point {pt} cannot be inserted for some reason'
            
            self.points = []

        
    