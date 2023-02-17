import random
import pygame

from objects import Background, Rabbit, Obstacles

pygame.init()
WIDTH, HEIGHT = (1200, 400)

# create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KEEP Moving")

clock = pygame.time.Clock()
FPS = 60

##    SpLit screen    ****************************************

# Camera for the split display
player1_camera = pygame.Rect(0, 0, WIDTH, HEIGHT // 2)
player2_camera = pygame.Rect(0, HEIGHT // 2, WIDTH, HEIGHT//2)

# Split display for each player
display_1 = screen.subsurface(player1_camera)
display_2 = screen.subsurface(player2_camera)

# Drawing a line on each split "screen" 
pygame.draw.line(display_1, (0,255,255),(0,HEIGHT/2), (WIDTH, HEIGHT/2),10)


# COLORS *********************************************************************

WHITE = (225,225,225)


# IMAGES *********************************************************************

start_img = pygame.image.load('Assets/Rabbit/start_img.png')
start_img = pygame.transform.scale(start_img, (25*2, 65*2))

game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('Assets/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('Assets/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

# SOUNDS *********************************************************************

jump_fx = pygame.mixer.Sound('Sounds/jump.wav')
die_fx = pygame.mixer.Sound('Sounds/die.wav')
checkpoint_fx = pygame.mixer.Sound('Sounds/checkPoint.wav')

# OBJECTS & GROUPS ***********************************************************

background = Background()
rabbit_1 = Rabbit(50, 160)
rabbit_2 = Rabbit(50, 160)

obstacles1_group = pygame.sprite.Group()
obstacles2_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def reset():
	global counter1,counter2, SPEED, score, high_score

	if score and score >= high_score:
		high_score = score

	counter1 = 0
	counter2 = 0
	SPEED = 5
	score = 0

	obstacles1_group.empty()
	obstacles2_group.empty()

	rabbit_1.reset()
	rabbit_2.reset()

# CHEATCODES *****************************************************************

# LYAGAMI -> automatic jump and duck

AI = False

# VARIABLES ******************************************************************

counter1 = 0
counter2 = 0
enemy_time = 100

SPEED = 5
scroll = 0
jump1 = False
jump2 = False

score = 0

high_score = 0

start_page = True
mouse_pos = (-1, -1)

running = True
while running:
	jump1 = False
	jump2 = False
	scroll+=3
	screen.fill(WHITE)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_w:
				if start_page:
					start_page = False
				elif rabbit_1.alive:
					jump1 = True
					jump_fx.play()
				else:
					reset()
			
			if event.key == pygame.K_UP:
				if start_page:
					start_page = False
				elif rabbit_2.alive:
					jump2 = True
					jump_fx.play()
				else:
					reset()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				jump1 = False
			if event.key == pygame.K_UP:
				jump2 = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)

	if start_page:
		screen.blit(start_img, (50,150))
	else:

		#player 1
		if rabbit_1.alive :
			counter1 += 1
			if counter1 % int(enemy_time) == 0:
					type = random.randint(1, 4)
					obstacles1 = Obstacles(type)
					obstacles1_group.add(obstacles1)

			if counter1 % 100 == 0:
				SPEED += 0.1
				enemy_time -= 0.5

			if counter1 % 5 == 0:
				score += 1

			if score and score % 100 == 0:
				checkpoint_fx.play()

			for obstacles1 in obstacles1_group:
				if pygame.sprite.collide_mask(rabbit_1, obstacles1):
					SPEED = 0
					rabbit_1.alive = False
					rabbit_2.alive = False
					die_fx.play()

		#player2
		if rabbit_2.alive :
			counter2 += 1
			if counter2 % int(enemy_time) == 0:
					type = random.randint(1, 4)
					obstacles2 = Obstacles(type)
					obstacles2_group.add(obstacles2)

			if counter2 % 100 == 0:
				SPEED += 0.1
				enemy_time -= 0.5

			if counter2 % 5 == 0:
				score += 1

			""" if score and score % 100 == 0:
				checkpoint_fx.play() """

			for obstacles2 in obstacles2_group:
				if AI:
					dx = obstacles2.rect.x - rabbit_2.rect.x
					if 0 <= dx <= (75):
						jump2 = True

				if pygame.sprite.collide_mask(rabbit_2, obstacles2):
					SPEED = 0
					rabbit_1.alive = False
					rabbit_2.alive = False
					die_fx.play()
	
		background.update(SPEED)
		background.draw(display_2,scroll)
		background.draw(display_1,scroll)
		obstacles1_group.update(SPEED, rabbit_1)
		obstacles2_group.update(SPEED, rabbit_2)
		obstacles1_group.draw(display_1)
		obstacles2_group.draw(display_2)
		rabbit_1.update(jump1, duck= False)
		rabbit_2.update(jump2, duck= False)
		rabbit_1.draw(display_1)
		rabbit_2.draw(display_2)


		string_score = str(score).zfill(5)
		for i, num in enumerate(string_score):
			screen.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		if high_score:
			screen.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score = f'{high_score}'.zfill(5)
			for i, num in enumerate(string_score):
				screen.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

		if not rabbit_1.alive or not rabbit_2.alive:
			screen.blit(game_over_img, (WIDTH//2-100, 55))
			screen.blit(replay_img, replay_rect)

			if replay_rect.collidepoint(mouse_pos):
				reset()

	pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.update()

	

pygame.quit()