import pygame
import math

SCREEN = WIDTH, HEIGHT = (1200, 200)

class Background():
	
	def __init__(self):
		
		# GROUND
		self.image = pygame.image.load('Assets/Background/ground.png')
		self.rect = self.image.get_rect()

		self.width_ground = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width_ground
		self.y = 150

 
	def update(self, speed):
		# GROUND
		self.x1 -= speed
		self.x2 -= speed
		

		if self.x1 <= -self.width_ground:
			self.x1 = self.width_ground

		if self.x2 <= -self.width_ground:
			self.x2 = self.width_ground
		

	def draw(self, screen, scroll):
		# GROUND
		screen.blit(self.image, (self.x1, self.y))
		screen.blit(self.image, (self.x2, self.y))


class Rabbit():
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.duck_list = []

		for i in range(1, 6):
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

	def update(self, jump1, duck):
		if self.alive:
			if not self.isJumping and jump1:
				self.vel = -self.jumpHeight
				self.isJumping = True

			self.vel += self.gravity
			if self.vel >= self.jumpHeight:
				self.vel = self.jumpHeight

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.isJumping = False

			if duck:
				self.counter += 1
				if self.counter >= 6:
					self.index = (self.index + 1) % len(self.duck_list)
					self.image = self.duck_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			elif self.isJumping:
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

	def update(self, jump2, duck):
		if self.alive:
			if not self.isJumping and jump2:
				self.vel = -self.jumpHeight
				self.isJumping = True

			self.vel += self.gravity
			if self.vel >= self.jumpHeight:
				self.vel = self.jumpHeight

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.isJumping = False

			if duck:
				self.counter += 1
				if self.counter >= 6:
					self.index = (self.index + 1) % len(self.duck_list)
					self.image = self.duck_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			elif self.isJumping:
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
	def __init__(self, type):
		super(Obstacles, self).__init__()

		self.image_list = []
		for i in range(6):
			scale = 0.55
			img = pygame.image.load(f'Assets/Obstacles/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 165

	def update(self, speed, rabbit):
		if rabbit.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		 screen.blit(self.image, self.rect)