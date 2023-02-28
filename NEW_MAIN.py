#Teste de edição

import random
import pygame
import math

from NEW_OBJECTS import Ground, Rabbit, Obstacles, Button

pygame.init()
WIDTH, HEIGHT = (1200, 400)

# create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("KEEP Moving")

clock = pygame.time.Clock()
FPS = 60


##    SpLit screen    ********************************************************

# Camera for the split display
player1_camera = pygame.Rect(0, 0, WIDTH, HEIGHT // 2)
player2_camera = pygame.Rect(0, HEIGHT // 2, WIDTH, HEIGHT//2)

# Split display for each player
display_1 = screen.subsurface(player1_camera)
display_2 = screen.subsurface(player2_camera)


# COLORS *********************************************************************

WHITE = (225,225,225)


# IMAGES *********************************************************************

# intro_background
intro_bg = pygame.image.load("Assets/Background/start_background.png").convert()

# main background
bg = pygame.image.load("Assets/Background/background.png").convert()
bg_width = bg.get_width()
bg_single = pygame.transform.scale(bg, (3600,400))

# load Rabbit INTRO images
rabbit_INTRO_list = []
for i in range(1, 36):
    rabbit_INTRO_img = pygame.image.load(f'Assets/bunny/v3geVY-{i} (arrastado).tiff')
    rabbit_INTRO_img = pygame.transform.scale(rabbit_INTRO_img, (423/2,558/2))
    rabbit_INTRO_list.append(rabbit_INTRO_img)

# load game over images
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

# Load replay image
replay_img = pygame.image.load('Assets/replay.png').convert_alpha()
replay_img = pygame.transform.scale(replay_img, (40*4, 36*4))

# load score numbers 
numbers_img = pygame.image.load('Assets/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

#load menu button images
singlePlayer_img = pygame.image.load("Assets/images/singlePlayer.png").convert_alpha()
twoPlayers_img = pygame.image.load("Assets/images/twoPlayers.png").convert_alpha()
playerVsCPU_img = pygame.image.load("Assets/images/playerVsCPU.png").convert_alpha()

#dificulty level images
easy_img = pygame.image.load("Assets/images/easy.png").convert_alpha()
medium_img = pygame.image.load("Assets/images/medium.png").convert_alpha()
hard_img = pygame.image.load("Assets/images/hard.png").convert_alpha()

#pause images
resume_img = pygame.image.load("Assets/images/button_resume.png").convert_alpha()
options_img = pygame.image.load("Assets/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("Assets/images/button_quit.png").convert_alpha()


# Create button instances *************************************************************************

### Define scale of all buttons
scale = 0.8

# 1st screen  
singlePlayer_button = Button((WIDTH/2 - singlePlayer_img.get_width()/2*scale), 90 , singlePlayer_img, scale)
twoPlayers_button = Button((WIDTH/2 - twoPlayers_img.get_width()/2*scale), 165.6, twoPlayers_img, scale)
playerVsCPU_button = Button((WIDTH/2 - playerVsCPU_img.get_width()/2*scale), 241.2, playerVsCPU_img, scale)

# pause 1st screen
resume_button = Button((WIDTH/2 - resume_img.get_width()/2*scale), 90 , resume_img, scale)
options_button = Button((WIDTH/2 - options_img.get_width()/2*scale), 165.6, options_img, scale)
quit_button = Button((WIDTH/2 - quit_img.get_width()/2*scale), 241.2, quit_img, scale)

# dificulty level
easy_button = Button((WIDTH/2 - easy_img.get_width()/2*scale), 90 , easy_img, scale)
medium_button = Button((WIDTH/2 - medium_img.get_width()/2*scale), 165.6, medium_img, scale)
hard_button = Button((WIDTH/2 - hard_img.get_width()/2*scale), 241.2, hard_img, scale)

# replay
replay_button = Button((WIDTH // 2 - 100),100,replay_img, 1)


# SOUNDS *********************************************************************

jump_fx = pygame.mixer.Sound('Assets/Sounds/jump.wav')
die_fx = pygame.mixer.Sound('Assets/Sounds/die.wav')
checkpoint_fx = pygame.mixer.Sound('Assets/Sounds/checkPoint.wav')


# OBJECTS & GROUPS ***********************************************************

ground_one_player = Ground(350)
ground_player_1 = Ground(150)
ground_player_2 = Ground(150)

rabbit_one_player = Rabbit(50, 350)
rabbit_1 = Rabbit(50, 160)
rabbit_2 = Rabbit(50, 160)

obstacles_one_player_group = pygame.sprite.Group()
obstacles_1_group = pygame.sprite.Group()
obstacles2_group = pygame.sprite.Group()


# FUNCTIONS ******************************************************************

def reset():

	global counter_player_1,counter_player_2, speed_player_1, speed_player_2, score_player_1, score_player_2, \
		high_score_player_1, high_score_player_2, high_score_geral, scroll_player_1, scroll_player_2, \
		enemy_time_1, enemy_time2

	if score_player_1 and score_player_1 >= high_score_player_1 :
		high_score_player_1 = score_player_1

	if score_player_2 and score_player_2 >= high_score_player_2:
		high_score_player_2 = score_player_2
	
	if high_score_player_1 >= high_score_player_2:
		high_score_geral = high_score_player_1
	else:
		high_score_geral = high_score_player_2
	

	counter_player_1 = 0
	counter_player_2 = 0
	
	enemy_time_1 = 100
	enemy_time2 = 100

	speed_player_1 = 5
	speed_player_2 = 5
	
	score_player_1 = 0
	score_player_2 = 0
	
	scroll_player_1
	scroll_player_2

	obstacles_1_group.empty()
	obstacles2_group.empty()

	rabbit_1.reset()
	rabbit_2.reset()


# AI *************************************************************************

AI = True


# VARIABLES ******************************************************************

#para a iteração de imagens do coelho do ecrã inicial
rabbit_start_value = 0

#variavel criada para abrandar a animação do coelho usa o valor inteiro de incrementos de 0.2 (sobe de 5 em 5 vezes) 
float_to_int=0

counter_player_1 = 0
counter_player_2 = 0
enemy_time_1 = 100
enemy_time2 = 100
speed_player_1 = 5
speed_player_2 = 5
jump1 = False
jump2 = False
score_player_1 = 0
score_player_2 = 0
high_score_player_1 = 0
high_score_player_2 = 0
high_score_geral = 0
mouse_pos = (-1, -1)
mouse_cliked = False
scroll_player_1 = 0
scroll_player_2 = 0
bg_tiles = math.ceil(WIDTH  / bg_width) + 1


# Game Variables  ************************************************************

one_player = False

start_page = True
game_paused = False
menu_state = "main"
run = True


# Game  ****************************************************************** 

while run:
	jump1 = False
	jump2 = False
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				game_paused = True

			if event.key == pygame.K_w:
				jump1 = True

			if event.key == pygame.K_BACKSPACE:
				if start_page == True:
					if menu_state == "options":
						menu_state = "main"
	
			if event.key == pygame.K_UP:
				if AI == False:
					jump2 = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				jump1 = False

			if event.key == pygame.K_UP:
				jump2 = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)
			mouse_cliked = False

		
	# First screen _________________________________________________________
	if start_page:
		screen.blit(intro_bg, (0,0))

		# DRAW Rabbit intro animation
		if rabbit_start_value >= len(rabbit_INTRO_list):
			rabbit_start_value = 0
			float_to_int = 0
		
		rabbit_INTRO_img = rabbit_INTRO_list[rabbit_start_value]
		screen.blit(rabbit_INTRO_img, (150,100))
		float_to_int+= 0.2
		rabbit_start_value= int(float_to_int)
	
		
		# MENU ______________________________________________________________
		
		### if state is main
		if menu_state == "main":

			#Single Player Button
			if singlePlayer_button.draw(screen) and not mouse_cliked:
				AI = False
				one_player = True 
				menu_state = "options"
				mouse_cliked = True
			
			# 2 Players Button
			if twoPlayers_button.draw(screen) and not mouse_cliked:
				AI = False
				one_player = False
				menu_state = "options"
				mouse_cliked = True

			# Player VS CPU
			if playerVsCPU_button.draw(screen) and not mouse_cliked:
				one_player = False
				AI = True
				menu_state = "options"
				mouse_cliked = True

		### if state is option (after main)
		if menu_state == "options":
			if easy_button.draw(screen) and not mouse_cliked:
				reset()
				start_page = False
				game_paused = False
				mouse_cliked = True
			if medium_button.draw(screen) and not mouse_cliked:
				reset()
				start_page = False
				game_paused= False
				mouse_cliked = True
			if hard_button.draw(screen) and not mouse_cliked:
				reset()
				start_page = False
				game_paused = False
				mouse_cliked = True
			
		
	# Menu from PAUSE screen_________________________________________________

	elif game_paused == True:
		#screen.fill(WHITE)

		if resume_button.draw(screen) and not mouse_cliked:
			game_paused = False
			mouse_cliked = True
		if options_button.draw(screen) and not mouse_cliked:
			menu_state = "main"
			start_page= True
			mouse_cliked = True
		if quit_button.draw(screen) and not mouse_cliked:
			run = False
			mouse_cliked = True
		

	# GAME IS RUNNING __________________________________________________

	elif one_player == False:

		#####	PLAYER 1	##### 
		if rabbit_1.alive :
			counter_player_1 += 1
			if counter_player_1 % int(enemy_time_1) == 0:
					type = random.randint(0, 4)
					obstacles_1 = Obstacles(type)
					obstacles_1_group.add(obstacles_1)

			if counter_player_1 % 100 == 0:
				speed_player_1 += 0.4
				enemy_time_1 -= 0.5

			if counter_player_1 % 5 == 0:
				score_player_1 += 1

			""" if score and score % 100 == 0:
				checkpoint_fx.play() """

			for obstacles1 in obstacles_1_group:
				if pygame.sprite.collide_mask(rabbit_1, obstacles1):
					speed_player_1 = 0
					rabbit_1.alive = False
					die_fx.play()

		#####	PLAYER 2	##### 
		if rabbit_2.alive :
			counter_player_2 += 1
			if counter_player_2 % int(enemy_time2) == 0:
					type = random.randint(0, 4)
					obstacles2 = Obstacles(type)
					obstacles2_group.add(obstacles2)

			if counter_player_2 % 100 == 0:
				speed_player_2 += 0.4
				enemy_time2 -= 0.5

			if counter_player_2 % 5 == 0:
				score_player_2 += 1

			""" if score and score % 100 == 0:
				checkpoint_fx.play() """

			# INICIO DA AI	___________________________________________________	
			for obstacles2 in obstacles2_group:
				if AI:
					dx = obstacles2.rect.x - rabbit_2.rect.x
					fudge = (int(60+(counter_player_1/30)))
					if fudge >= 230:
						fudge = (int(65+(counter_player_1/25)))
					if fudge >= 330:
						fudge = (int(70+(counter_player_1/20)))
					if fudge >= 420:		
						fudge = (int((counter_player_1/30)))
					if counter_player_1 >= 11000 and counter_player_1 <= 13499:
						fudge = (int((counter_player_1/25)))
					if counter_player_1 >= 13500: #and counter1 <= 13999:
						fudge = (1200)
					if dx <= (fudge):
						jump2 = True
			# FIM DA AI	__________________________________________________________		

				if pygame.sprite.collide_mask(rabbit_2, obstacles2):
					speed_player_2 = 0
					rabbit_2.alive = False
					die_fx.play()


		#####	DRAW BACKGROUND IMAGE	##### 
		for i in range(0, bg_tiles):
			display_1.blit(bg, (i * bg_width + scroll_player_1,0))
			display_2.blit(bg, (i * bg_width + scroll_player_2,0))
		scroll_player_1 -= speed_player_1/10
		scroll_player_2 -= speed_player_2/20

		# update scroll
		if abs(scroll_player_1) > (bg_width):
			scroll_player_1 = 0
		if abs(scroll_player_2) > (bg_width):
			scroll_player_2 = 0
		

		#####	DRAW GROUND, Rabbits and Obstacles in gameplay	##### 
		ground_player_1.update(speed_player_1)
		ground_player_2.update(speed_player_2)
		ground_player_1.draw(display_1)
		ground_player_2.draw(display_2)
		obstacles_1_group.update(speed_player_1, rabbit_1)
		obstacles2_group.update(speed_player_2, rabbit_2)
		obstacles_1_group.draw(display_1)
		obstacles2_group.draw(display_2)
		rabbit_1.update(jump1)
		rabbit_2.update(jump2)
		rabbit_1.draw(display_1)
		rabbit_2.draw(display_2)


		string_score_player_1 = str(score_player_1).zfill(5)
		for i, num in enumerate(string_score_player_1):
			display_1.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		string_score_player_2 = str(score_player_2).zfill(5)
		for i, num in enumerate(string_score_player_2):
			display_2.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		if high_score_player_1:
			display_1.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score_player_1 = f'{high_score_player_1}'.zfill(5)
			for i, num in enumerate(string_score_player_1):
				display_1.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))
		
		if high_score_player_2:
			display_2.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score_player_2 = f'{high_score_player_2}'.zfill(5)
			for i, num in enumerate(string_score_player_2):
				display_2.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))
		
		if high_score_geral:
			screen.blit(numbers_img, (1105, 10), (100, 0, 20, 12))
			string_score_player_2 = f'{high_score_player_2}'.zfill(5)
			for i, num in enumerate(string_score_player_2):
				screen.blit(numbers_img, (1135+11*i, 10), (10*int(num), 0, 10, 12))

		if not rabbit_1.alive:
			display_1.blit(game_over_img, (WIDTH//2-100, 50))
		if not rabbit_2.alive:
			display_2.blit(game_over_img, (WIDTH//2-100, 50))
		if not rabbit_1.alive and not rabbit_2.alive:
			if replay_button.draw(screen) and not mouse_cliked:
				reset()

	elif one_player == True:

		#####	PLAYER 1	##### 
		if rabbit_1.alive :
			counter_player_1 += 1
			if counter_player_1 % int(enemy_time_1) == 0:
					type = random.randint(0, 4)
					obstacles_1 = Obstacles(type)
					obstacles_1_group.add(obstacles_1)

			if counter_player_1 % 100 == 0:
				speed_player_1 += 0.4
				enemy_time_1 -= 0.5

			if counter_player_1 % 5 == 0:
				score_player_1 += 1

			""" if score and score % 100 == 0:
				checkpoint_fx.play() """

			for obstacles1 in obstacles_1_group:
				if pygame.sprite.collide_mask(rabbit_1, obstacles1):
					speed_player_1 = 0
					rabbit_1.alive = False
					die_fx.play()


		#####	DRAW BACKGROUND IMAGE	##### 
		for i in range(0, bg_tiles):
			screen.blit(bg_single, (i * bg_width + scroll_player_1,0))
		scroll_player_1 -= speed_player_1/6

		# update scroll
		if abs(scroll_player_1) > (bg_width):
			scroll_player_1 = 0


		#####	DRAW GROUND, Rabbits and Obstacles in gameplay	##### 
		ground_one_player.update(speed_player_1)
		ground_one_player.draw(screen)
		obstacles_1_group.update(speed_player_1, rabbit_1)
		obstacles_1_group.draw(screen)
		rabbit_one_player.update(jump1)
		rabbit_one_player.draw(screen)


		string_score_player_1 = str(score_player_1).zfill(5)
		for i, num in enumerate(string_score_player_1):
			display_1.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		if high_score_player_1:
			display_1.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score_player_1 = f'{high_score_player_1}'.zfill(5)
			for i, num in enumerate(string_score_player_1):
				display_1.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))
		
		if high_score_geral:
			screen.blit(numbers_img, (1105, 10), (100, 0, 20, 12))
			string_score_player_2 = f'{high_score_player_2}'.zfill(5)
			for i, num in enumerate(string_score_player_2):
				screen.blit(numbers_img, (1135+11*i, 10), (10*int(num), 0, 10, 12))

		if not rabbit_1.alive:
			display_1.blit(game_over_img, (WIDTH//2-100, 50))
			if replay_button.draw(screen) and not mouse_cliked:
				reset()


	pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()