import pygame
import math

SCREEN = WIDTH, HEIGHT = (1200, 400)

class Background():
	
	def __init__(self, x, y):

		# GROUND	
		self.x = x
		self.y = y
		self.image = pygame.image.load("Assets/Background/background.png").convert()
		self.image = pygame.transform.scale(self.image, (WIDTH*self.x,(HEIGHT/2)*self.y))
		self.scroll = 0
		self.width_ground = self.image.get_width()
		self.g_tiles = math.ceil(WIDTH  / self.width_ground) + 1
 
	def update(self, speed):
		self.scroll -= speed/10	
	
	def draw(self, screen):
		for i in range(0, self.g_tiles):
			screen.blit(self.image, (i * self.width_ground + self.scroll,0))
		if abs(self.scroll) > self.width_ground:
			self.scroll = 0

class Ground():
	
	def __init__(self, y):

		# GROUND
		self.image = pygame.image.load('Assets/Background/block-big.png')
		self.y = y
		self.scroll = 0
		self.width_ground = self.image.get_width()
		self.g_tiles = math.ceil(WIDTH  / self.width_ground) + 1
 
	def update(self, speed):
		self.scroll -= speed	
	
	def draw(self, screen):
		for i in range(0, self.g_tiles):
			screen.blit(self.image, (i * self.width_ground + self.scroll,self.y))
		if abs(self.scroll) > self.width_ground:
			self.scroll = 0
	
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
		

	
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Rabbit():
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.duck_list = []

		for i in range(1, 4):
			img = pygame.image.load(f'Assets/Rabbit/{i}.png')
			img = pygame.transform.scale(img, (52, 58))
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'Assets/Rabbit/{i}.png')
			img = pygame.transform.scale(img, (70, 38))
			self.duck_list.append(img)

		self.dead_image = pygame.image.load(f'Assets/Rabbit/6.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (52,58))

		self.reset()

		self.vel = 0
		self.gravity = 1
		self.jumpHeight = 15
		self.isJumping = False

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.bottom = self.base

		self.alive = True
		self.counter = 0

	def update(self, jump):
		if self.alive:
			if not self.isJumping and jump:
				self.vel = -self.jumpHeight
				self.isJumping = True

			self.vel += self.gravity
			if self.vel >= self.jumpHeight:
				self.vel = self.jumpHeight

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.isJumping = False


			if self.isJumping:
				self.index = 0
				self.counter = 0
				self.image = self.run_list[self.index]
			else:
				self.counter += 1
				if self.counter >= 4:
					self.index = (self.index + 1) % len(self.run_list)
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

		else:
			self.image = self.dead_image


	def draw(self, player2_display):
		player2_display.blit(self.image, self.rect)
 
class Obstacles(pygame.sprite.Sprite):


	def __init__(self, type, bottom):
		super(Obstacles, self).__init__()

		self.image_list = []
		for i in range(5):
			scale = 0.55
			img = pygame.image.load(f'Assets/Obstacles/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = bottom

	def update(self, speed, rabbit):
		if rabbit.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		 screen.blit(self.image, self.rect)
 