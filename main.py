import pygame,sys,random
import numpy as np
from shapely.geometry import LineString

class Block(pygame.sprite.Sprite):
    def __init__(self, color, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([w, h])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.w = w
        self.h = h

##### ALGORITHMS #####

### COLLISION ###

# does the line through a1 a2 collide with any obstacles
def collision(a1, a2, obstacles):
    line1 = LineString([a1, a2])
    for obst in obstacles:
        BB = [np.array([(obst.x, obst.y), (obst.x + obst.w, obst.y)]),
                np.array([(obst.x, obst.y), (obst.x, obst.y + obst.h)]),
                np.array([(obst.x, obst.y + obst.h), (obst.x + obst.w, obst.y + obst.h)]),
                np.array([(obst.x + obst.w, obst.y), (obst.x + obst.w, obst.y + obst.h)])]
        for B in BB:
            line2 = LineString([B[0], B[1]])
            if line1.intersection(line2):
                return True
            else:
                continue
    return False

def distance(a, b):
    return np.linalg.norm(a-b)


### NODE ###
class Node:
    def __init__(self, point, parent=None, cost=None):
        self.point = point
        self.parent = parent
        self.cost = cost

### RRT ###
class RRT:
    def __init__(self, screen, width, height, obstacles, start, goal):
        self.image = screen
        self.width = width
        self.height = height
        self.obstacles = obstacles
        self.start = Node(start)
        self.goal = Node(goal)
        self.nodes = [self.start]
        self.growth = 25

    def draw_edge(self, a, b):
        pygame.draw.line(self.image, (9, 0, 0), (int(a.point[0]), int(a.point[1])),
                         (int(b.point[0]), int(b.point[1])), 1)
        pygame.display.update()

    def draw_done(self):
        pass

    def run(self):

        if self.valid_edge(self.start, self.goal):
            self.draw_edge(self.start, self.goal)
            self.draw_done()
            return


        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            qrand = self.rand()
            qnear = self.nearest(qrand)
            qnew = self.new_scaled(qnear, qrand)

            if qnew.point[0] < 0 or qnew.point[0] >= self.width or qnew.point[1] < 0 or qnew.point[1] >= self.height:
                    continue

            if not self.valid_edge(qnear, qnew):
                continue
            self.nodes.append(qnew)
            self.draw_edge(qnear, qnew)

            if self.valid_edge(qnew, self.goal):
                self.draw_edge(qnew, self.goal)
                self.draw_done()
                return

    def valid_edge(self, a, b):
        return not collision(a.point, b.point, self.obstacles)


    def new_scaled(self, qnear, qrand):
        if distance(qnear.point, qrand.point) < self.growth * self.growth:
            return qrand
        temp = qrand.point - qnear.point
        temp = temp / np.sqrt(np.sum(temp**2))
        return Node(qnear.point + (temp * self.growth))

    def rand(self):
        return Node(np.array([random.randint(0, self.width),random.randint(0, self.height)]))

    def nearest(self, p1):
        return min(self.nodes, key=lambda p2: distance(p2.point, p1.point))

class RRTSTAR(RRT):
    def __init__(self, screen, width, height, obstacles, start, goal):
        super().__init__(screen, width, height, obstacles, start, goal)
        self.r = 50

    def run(self):
        if self.valid_edge(self.start, self.goal):
            self.draw_edge(self.start, self.goal)
            self.draw_done()
            return

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            qrand = self.rand()
            qnear = self.nearest(qrand)
            qnew = self.new_scaled(qnear, qrand)

            if qnew.point[0] < 0 or qnew.point[0] >= self.width or qnew.point[1] < 0 or qnew.point[1] >= self.height:
                    continue

            qnew.cost = distance(qnew.point, qnear.point)

            neighbours = self.neighbours(qnew)

            for n in neighbours:
                if qnew.cost + distance(qnew.point, n.point) < n.cost:
                    if valid_edge(qnew, n):
                        n.cost =  qnew.cost + distance(qnew.point, n.point)
                        n.parent = qnew

                    




# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = width, height = 600,600
clock = pygame.time.Clock()

obstacles = pygame.sprite.Group([Block(BLACK, 100, 250, 200, 0), Block(BLACK, 100, 250, 200, height - 250), Block(BLACK, 100, 425, 325, 50)])

start = np.array([10,300])
goal = np.array([590,300])


myfont = pygame.font.SysFont("Courier", 30)

# Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)
screen.fill((100,100,71))
bg = pygame.Color("#e7eaf6")

pygame.display.set_caption("My Game")

algorithms = [RRT(screen, width, height, obstacles, start, goal)]


while True:
    screen.fill(WHITE)
    pause = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
               pause = False
    if pause:
        continue

    obstacles.draw(screen)

    RRT(screen, width, height, obstacles, start, goal).run()
    
    pygame.display.update()
    clock.tick(60)