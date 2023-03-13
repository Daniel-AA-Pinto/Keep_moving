import random
import pygame

from objects import Ground, Rabbit, Obstacles, Button, Background

pygame.init()
WIDTH, HEIGHT = (1200, 400)

# create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("KEEP Moving")

clock = pygame.time.Clock()
#velocidade fo jogo
FPS = 60


##    Split screen    ******************************************************

# Camera for the split display
player1_camera = pygame.Rect(0, 0, WIDTH, HEIGHT // 2)
player2_camera = pygame.Rect(0, HEIGHT // 2, WIDTH, HEIGHT//2)

# Split display for each player
display_1 = screen.subsurface(player1_camera)
display_2 = screen.subsurface(player2_camera)


# COLORS ********************************************************************

WHITE = (225,225,225)


# IMAGES *********************************************************************

# intro_background
intro_bg = pygame.image.load("Assets/Background/start_background.png").convert()


# pause_background
pause_bg = pygame.image.load("Assets/Background/bg_transparent_50.png").convert_alpha()

# load Rabbit INTRO images
rabbit_INTRO_list = []
for i in range(1, 36):
	rabbit_INTRO_img = pygame.image.load(f'Assets/bunny/v3geVY-{i} (arrastado).tiff')
	rabbit_INTRO_img = pygame.transform.scale(rabbit_INTRO_img, (423/2,558/2))
	rabbit_INTRO_list.append(rabbit_INTRO_img)

# load game over images
game_over_img = pygame.image.load('Assets/images/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

# Load replay image
replay_img = pygame.image.load('Assets/images/button_play_again.png').convert_alpha()
#replay_img = pygame.transform.scale(replay_img, (40*4, 36*4))

# load score numbers 
numbers_img = pygame.image.load('Assets/images/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

#load menu button images
singlePlayer_img = pygame.image.load("Assets/images/singlePlayer.png").convert_alpha()
twoPlayers_img = pygame.image.load("Assets/images/twoPlayers.png").convert_alpha()
playerVsCPU_img = pygame.image.load("Assets/images/playerVsCPU.png").convert_alpha()

#difficulty level images
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

# difficulty level
easy_button = Button((WIDTH/2 - easy_img.get_width()/2*scale), 90 , easy_img, scale)
medium_button = Button((WIDTH/2 - medium_img.get_width()/2*scale), 165.6, medium_img, scale)
hard_button = Button((WIDTH/2 - hard_img.get_width()/2*scale), 241.2, hard_img, scale)

# replay
replay_button = Button(425.5,118,replay_img, 1)


# SOUNDS *********************************************************************

mouse_collision_fx = pygame.mixer.Sound('Assets/Sounds/jump3.wav')
mouse_click_fx = pygame.mixer.Sound('Assets/Sounds/jump3.wav')
jump_fx = pygame.mixer.Sound('Assets/Sounds/jump3.wav')
die_fx = pygame.mixer.Sound('Assets/Sounds/die.wav')
checkpoint_fx = pygame.mixer.Sound('Assets/Sounds/checkPoint.wav')
pygame.mixer.music.load('Assets/Sounds/music_game.mp3')

# OBJECTS & GROUPS ***********************************************************

background_one_player = Background(3,2)
background_player_1 = Background(2,1)
background_player_2 = Background(2,1)

ground_one_player = Ground(350)
ground_player_1 = Ground(150)
ground_player_2 = Ground(150)

rabbit_one_player = Rabbit(50, 360)
rabbit_1 = Rabbit(50, 160)
rabbit_2 = Rabbit(50, 160)

obstacles_one_player_group = pygame.sprite.Group()
obstacles_1_group = pygame.sprite.Group()
obstacles2_group = pygame.sprite.Group()


# FUNCTIONS ******************************************************************

def reset():

	global counter_player_1,counter_player_2, speed_player_1, speed_player_2, score_player_1, score_player_2, \
		high_score_player_1, high_score_player_2, high_score_geral, scroll_player_1, scroll_player_2, \
		enemy_time_1, enemy_time_2

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
	enemy_time_2 = 100

	speed_player_1 = 5
	speed_player_2 = 5
	
	score_player_1 = 0
	score_player_2 = 0
	
	scroll_player_1 = 0
	scroll_player_2 = 0

	obstacles_1_group.empty()
	obstacles2_group.empty()

	rabbit_one_player.reset()
	rabbit_1.reset()
	rabbit_2.reset()


# AI *************************************************************************

AI = True


# VARIABLES ******************************************************************

#para a iteração de imagens do coelho do ecrã inicial
rabbit_start_value = 0

# variavel criada para abrandar a animação do coelho usa o valor inteiro de incrementos de 0.2 (sobe de 5 em 5 vezes) 
float_to_int = 0

counter_player_1 = 0
counter_player_2 = 0
enemy_time_1 = 100
enemy_time_2 = 100
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
difficulty = 0


# Game Variables  ************************************************************

one_player = False
start_page = True
game_paused = False
menu_state = "main"
run = True
help_score= 0


# Game  ********************************************************************

while run:
	jump1 = False
	jump2 = False
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				game_paused = True
				FPS = 60
				pygame.mixer.music.pause()

			if event.key == pygame.K_w:
				jump1 = True
				

			if event.key == pygame.K_BACKSPACE:
				if start_page == True:
					if menu_state == "options":
						menu_state = "main"
			
			if event.key == pygame.K_l:
				AI = False
			
	
			if event.key == pygame.K_UP:
				if AI == False:
					jump2 = True
			
			if event.key == pygame.K_m:
				pygame.mixer.music.set_volume(0)
			
			if event.key == pygame.K_n:
				pygame.mixer.music.set_volume(0.2)
				

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				jump1 = False

			if event.key == pygame.K_l:
				AI = True

			if event.key == pygame.K_UP:
				jump2 = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)
			mouse_cliked = False

		
	# First screen __________________________________________________________

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
				rabbit_1 = Rabbit(50, 160)
				AI = False
				one_player = False
				menu_state = "options"
				mouse_cliked = True


			# Player VS CPU
			if playerVsCPU_button.draw(screen) and not mouse_cliked:
				rabbit_1 = Rabbit(50, 160)
				one_player = False
				AI = True
				menu_state = "options"
				mouse_cliked = True


		### if state is option (after main)
		if menu_state == "options":
			if easy_button.draw(screen) and not mouse_cliked:
				reset()
				difficulty = 1
				start_page = False
				game_paused = False
				mouse_cliked = True
			if medium_button.draw(screen) and not mouse_cliked:
				reset()
				difficulty = 2
				start_page = False
				game_paused= False
				mouse_cliked = True
			if hard_button.draw(screen) and not mouse_cliked:
				reset()
				difficulty = 3
				start_page = False
				game_paused = False
				mouse_cliked = True
					
	# Menu from PAUSE screen_________________________________________________

	elif game_paused == True:
		screen.blit(pause_bg, (0,0))	

		if resume_button.draw(screen) and not mouse_cliked:
			game_paused = False
			mouse_cliked = True
			pygame.mixer.music.unpause()

		if options_button.draw(screen) and not mouse_cliked:
			menu_state = "main"
			start_page= True
			mouse_cliked = True
		if quit_button.draw(screen) and not mouse_cliked:
			run = False
			mouse_cliked = True
		
	# GAME IS RUNNING ________________________________________________________

	elif one_player == False:
		if score_player_1 == 1 :
			pygame.mixer.music.play(-1, 0.0, 5000)
			pygame.mixer.music.set_volume(0.20)
		
		#####	PLAYER 1	##### 
		if rabbit_1.alive :
			counter_player_1 += 1
			if counter_player_1 % int(enemy_time_1) == 0:
					type = random.randint(0, 4)
					obstacles_1 = Obstacles(type, 165)
					obstacles_1_group.add(obstacles_1)

			if counter_player_1 % 100 == 0:
				match difficulty:
					case 1:
						speed_player_1 += 0.5
						enemy_time_1 -= 0.5
					case 2:
						speed_player_1 += 0.4 * 1.25
						enemy_time_1 -= 0.5 * 1.25
					case 3:
						speed_player_1 += 0.4 * 1.50
						enemy_time_1 -= 0.5 * 1.50


			if counter_player_1 % 5 == 0:
				score_player_1 += 1

			if score_player_1 and score_player_1 % 100 == 0:
				checkpoint_fx.play()
				checkpoint_fx.set_volume(0.20)

			for obstacles1 in obstacles_1_group:
				if pygame.sprite.collide_mask(rabbit_1, obstacles1):
					speed_player_1 = 0
					rabbit_1.alive = False
					die_fx.play()

			

		#####	PLAYER 2	##### 
		if rabbit_2.alive :
			counter_player_2 += 1
			if counter_player_2 % int(enemy_time_2) == 0:
					type = random.randint(0, 4)
					obstacles2 = Obstacles(type, 165)
					obstacles2_group.add(obstacles2)

			if counter_player_2 % 100 == 0:
				match difficulty:	
					case 1:
						speed_player_2 += 0.5
						enemy_time_2 -= 0.5
					case 2:
						speed_player_2 += 0.4 * 1.25
						enemy_time_2 -= 0.5 * 1.25
					case 3:
						speed_player_2 += 0.4 * 1.50
						enemy_time_2 -= 0.5 * 1.50

			if counter_player_2 % 5 == 0:
				score_player_2 += 1

			if score_player_2 and score_player_2 % 100 == 0:
				checkpoint_fx.play()
				checkpoint_fx.set_volume(0.20)

			# INICIO DA AI	___________________________________________________	
			for obstacles2 in obstacles2_group:
				match difficulty:
					
					case 1:    # Difficulty: EASY
						if AI:
							dx = obstacles2.rect.x - rabbit_2.rect.x
							fudge = (int(70+(counter_player_2/80)))
							if score_player_2 >= 415: #415 SCORE
								fudge = int(random.uniform(55, 100))
								if score_player_2 >= 500: #TO LOSE (505 MAX SCORE)
									fudge = 50
							if dx <= (fudge):
								jump2 = True
						
					case 2:    # Difficulty: MEDIUM
						if AI:
							dx = obstacles2.rect.x - rabbit_2.rect.x
							fudge = (int(60+(counter_player_2/10)))
							if score_player_2 >= 670: #670 SCORE
								fudge = int(random.uniform(110, 130))
								if score_player_2 >= 760: #TO LOSE (765 MAX SCORE)
									fudge = 100
							if dx <= (fudge):
								jump2 = True
					
					case 3:    # Difficulty: HARD
						if AI:
							dx = obstacles2.rect.x - rabbit_2.rect.x
							fudge = (int(75+(counter_player_2/20)))
							if score_player_2 >= 820: #820 SCORE
								fudge = int(random.uniform(130, 175)) #1108 MAX SCORE (LUCKY)
							if dx <= (fudge):
								jump2 = True

			

			# FIM DA AI	__________________________________________________________	
				if pygame.sprite.collide_mask(rabbit_2, obstacles2):
					speed_player_2 = 0
					rabbit_2.alive = False
					die_fx.play()
			
		if rabbit_1.alive == False and score_player_1 == score_player_2:
			FPS = 10
		if rabbit_1.alive == False and score_player_1 + 5 == score_player_2:
			FPS = 60
		if rabbit_2.alive == False and score_player_2 == score_player_1:
			FPS = 10
		if rabbit_2.alive == False and score_player_2 + 5 == score_player_1:
			FPS = 60

		# JUMP sound **********************

		if jump1 == True and rabbit_1.isJumping == False and rabbit_1.alive == True:
			jump_fx.play()
			jump_fx.set_volume(0.2)
	
		if jump2 == True and rabbit_2.isJumping == False and rabbit_2.alive == True:
			jump_fx.play()
			jump_fx.set_volume(0.2)


		#####	DRAW GROUND, Rabbits and Obstacles in gameplay	##### 
		
		background_player_1.update(speed_player_1)
		background_player_2.update(speed_player_2)
		background_player_1.draw(display_1)
		background_player_2.draw(display_2)
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
		
		
		# score player 1
		string_score_player_1 = str(score_player_1).zfill(5)
		for i, num in enumerate(string_score_player_1):
			display_1.blit(numbers_img, (625+11*i, 10), (10*int(num), 0, 10, 12))

		#score player 2
		string_score_player_2 = str(score_player_2).zfill(5)
		for i, num in enumerate(string_score_player_2):
			display_2.blit(numbers_img, (625+11*i, 10), (10*int(num), 0, 10, 12))

		# print hi-score player 1
		if high_score_player_1:
			# print "HI"
			display_1.blit(numbers_img, (520, 10), (100, 0, 20, 12))
			string_score_player_1 = f'{high_score_player_1}'.zfill(5)
			for i, num in enumerate(string_score_player_1):
				display_1.blit(numbers_img, (545+11*i, 10), (10*int(num), 0, 10, 12))
		
		# print hi-score player 2
		if high_score_player_2:
			# print "HI"
			display_2.blit(numbers_img, (520, 10), (100, 0, 20, 12))
			string_score_player_2 = f'{high_score_player_2}'.zfill(5)
			for i, num in enumerate(string_score_player_2):
				display_2.blit(numbers_img, (545+11*i, 10), (10*int(num), 0, 10, 12))
		
		# print hi-score geral
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
			pygame.mixer.music.stop()
			if replay_button.draw(screen) and not mouse_cliked:
				reset()
				
				
	elif one_player == True:
		rabbit_1 = rabbit_one_player

		if score_player_1 == 1 :
			pygame.mixer.music.play(-1, 0.0, 5000)
			pygame.mixer.music.set_volume(0.20)

		#####	PLAYER 1	##### 
		if rabbit_1.alive :
			counter_player_1 += 1
			if counter_player_1 % int(enemy_time_1) == 0:
					type = random.randint(0, 4)
					obstacles_1 = Obstacles(type, 365)
					obstacles_1_group.add(obstacles_1)

			if counter_player_1 % 100 == 0:
				match difficulty:
					case 1:
						speed_player_1 += 0.5
						enemy_time_1 -= 0.5
					case 2:
						speed_player_1 += 0.4 * 1.25
						enemy_time_1 -= 0.5 * 1.25
					case 3:
						speed_player_1 += 0.4 * 1.50
						enemy_time_1 -= 0.5 * 1.50

			if counter_player_1 % 5 == 0:
				score_player_1 += 1

			""" if score and score % 100 == 0:
				checkpoint_fx.play() """

			for obstacles1 in obstacles_1_group:
				if pygame.sprite.collide_mask(rabbit_1, obstacles1):
					speed_player_1 = 0
					rabbit_1.alive = False
					die_fx.play()

		if jump1 == True and rabbit_1.isJumping == False and rabbit_1.alive == True:
			jump_fx.play()
			jump_fx.set_volume(0.2)

		#####	DRAW GROUND, Rabbits and Obstacles in gameplay	##### 

		background_one_player.update(speed_player_1)
		background_one_player.draw(screen)
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
		

		if not rabbit_1.alive:
			display_1.blit(game_over_img, (WIDTH//2-100, 50))
			if replay_button.draw(screen) and not mouse_cliked:
				reset()


	pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)

	pygame.display.flip()
	clock.tick(FPS)
	help_score = score_player_2


pygame.quit()