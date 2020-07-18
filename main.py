import pygame,sys

class Block(pygame.sprite.Sprite):
	def __init__(self, color, w, h, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([w, h])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = width, height = 600,600
clock = pygame.time.Clock()

obstacles = pygame.sprite.Group([Block(BLACK, 100, 250, 200, 0), Block(BLACK, 100, 250, 200, height - 250), Block(BLACK, 100, 300, 375, 200)])

myfont = pygame.font.SysFont("Courier", 30)

# Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)
screen.fill((100,100,71))
bg = pygame.Color("#e7eaf6")

pygame.display.set_caption("My Game")

algorithms = [RRT(width, height, obstacles, start, goal)]


while True:
	screen.fill(WHITE)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pass

	obstacles.draw(screen)


	
	pygame.display.update()
	clock.tick(60)