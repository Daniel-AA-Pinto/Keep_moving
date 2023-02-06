import sys
import random
import pygame
import math
from pygame.locals import *


pygame.init()                           # INICIO do PROGRAMA *********    

clock = pygame.time.Clock()             # Variavel clock de forma a bloquear o FPS posteriormente
FPS = 60                            

SCREEN_WIDTH = 1500                     # Largura da janela
SCREEN_HEIGHT = 600                     # Altura da janela

#create game window                     
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # definir a variavel screen
pygame.display.set_caption("KEEP RUNNING")                        # Nome do jogo

#load image
bg = pygame.image.load("bg.png").convert()  # Criação da imagem do background
bg_width = bg.get_width()                   # 
bg_rect = bg.get_rect()						#
bg_heigth = bg.get_height()                 #

# Set player 1 starting position
player1_x = SCREEN_WIDTH*0.05
player1_y = (SCREEN_HEIGHT/2)*0.7
player1_width = 50
player1_height = 50


# Set player 2 starting position
player2_x = SCREEN_WIDTH*0.05
player2_y = (SCREEN_HEIGHT/2)*0.7
player2_width = 50
player2_height = 50


# Set obstacle starting position and speed for player 1
obstacle1_x = SCREEN_WIDTH
obstacle1_y = (SCREEN_HEIGHT/2)*0.7+50
obstacle1_speed = 7

# Set obstacle starting position and speed for player 2
obstacle2_x = SCREEN_WIDTH
obstacle2_y = (SCREEN_HEIGHT/2)*0.7+50
obstacle2_speed = 7

# Set game score
score1 = 0
score2 = 0



#define game variables
scroll1 = 0											   # inicialização da variavel scroll
scroll2 = 0                                          # inicialização da variavel scroll
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1      # contagem de quantas imagens serap necessárias. ceil, arredonda para cima o valor. e adicionamos 1 para corrigir algum GAP existente

## SpLit screen ****************************************
	
	# Camera for the split display (isto podia estar contido no split display abaixo)
player1_camera = pygame.Rect(0,0,SCREEN_WIDTH, SCREEN_HEIGHT // 2)
player2_camera = pygame.Rect(0,SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT//2)

	# Split display for each player
player1_display = screen.subsurface(player1_camera)
player2_display = screen.subsurface(player2_camera)

# Drawing a line on each split "screen" 
pygame.draw.line(player1_display, (0,255,255),(0,SCREEN_HEIGHT/2), (SCREEN_WIDTH,SCREEN_HEIGHT/2),10)

## DEFINIR CLASSES *****************************************************

bg1_x = 0
bg2_x = 0
class Player1():

	def __init__(self, x, y):
		self.x = x 
		self.y = y
		# isJump and jumpCount should be attributes of Mario.
		self.isJump = False
		self.jumpCount = 10

	def draw(self):
		global p1_for_collision
		p1_for_collision = pygame.draw.rect(player1_display, (0, 0, 255), [self.x, self.y, player1_width, player1_height])

	def move(self):
		global bg1_x
		if pressed_keys[K_d] and bg1_x > -920:
			if self.x > 490:
				bg1_x -= 5
			else:
				self.x += 5
		if pressed_keys[K_a] and self.x > 5:
			self.x -= 5

	def jump(self):
		# Check if mario is jumping and then execute the
		# jumping code.
		if self.isJump:
			if self.jumpCount >= -10:
				neg = 1
				if self.jumpCount < 0:
					neg = -1
				self.y -= self.jumpCount**2 * 0.3 * neg
				self.jumpCount -= 1
			else:
				self.isJump = False
				self.jumpCount = 10

class Player2():
	def __init__(self, x, y):
		self.x = x 
		self.y = y
		# isJump and jumpCount should be attributes of Mario.
		self.isJump = False
		self.jumpCount = 10

	def draw(self):
		global p2_for_collision
		p2_for_collision = pygame.draw.rect(player2_display, (255, 255, 0), [self.x, self.y, player1_width, player1_height])

	def move(self):
		global bg2_x
		if pressed_keys[K_RIGHT] and bg2_x > -920:
			if self.x > 490:
				bg2_x -= 5
			else:
				self.x += 5
		if pressed_keys[K_LEFT] and self.x > 5:
			self.x -= 5

	def jump(self):
		# Check if mario is jumping and then execute the
		# jumping code.
		if self.isJump:
			if self.jumpCount >= -10:
				neg = 1
				if self.jumpCount < 0:
					neg = -1
				self.y -= self.jumpCount**2 * 0.1 * neg
				self.jumpCount -= 1
			else:
				self.isJump = False
				self.jumpCount = 10


player1 = Player1(SCREEN_WIDTH*0.05,(SCREEN_HEIGHT/2)*0.7)
player2 = Player2(SCREEN_WIDTH*0.05,(SCREEN_HEIGHT/2)*0.7)



######################    LOOOP START   ####################################################

#game loop
run = True
alive = True                              # INICIO DO JOGO - sempre
while run:                                # While de INICIO, vai até ao fim
	clock.tick(FPS)				 #impoe a limitação de FPS do programa usando o clock. já definido acima

	#event handler                            #  faz com que, de para ternimar o jogo
	for event in pygame.event.get():          # Codifo quase "obrigatório"
		if event.type == pygame.QUIT:           # 
			run = False                           # aqui termina o while
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				# Start to jump by setting isJump to True.
				player1.isJump = True
			if event.key == pygame.K_UP:
				player2.isJump = True
			if event.key == pygame.K_SPACE:
				alive = True

	pressed_keys = pygame.key.get_pressed()



### WINING screen

	#screen.fill((91,154,236))
	font = pygame.font.Font(None, 30)

	if score1> score2:
		text = font.render("Player 1 WINs: " + str(score1),True, (0, 0, 0))
		screen.blit(text,((SCREEN_WIDTH)/2, SCREEN_HEIGHT/2))
	elif score2> score1:
		text = font.render("Player 2 WINs: " + str(score2),True, (0, 0, 0))
		screen.blit(text,((SCREEN_WIDTH)/2, SCREEN_HEIGHT/2))
	else:
		text = font.render("SHIT, lets do this again ok?",True, (0, 0, 0))
		screen.blit(text,(((SCREEN_WIDTH-(28*30/2))/2), SCREEN_HEIGHT/2))


### Jogo em si	

	if alive:
		#draw scrolling background
		for i in range(0,tiles):                         
			player1_display.blit(bg,(i * bg_width + scroll1,300-bg_heigth))     # 1 - blit desenha / carrega a imagem para o screen.
			player2_display.blit(bg, (i * bg_width + scroll2,300-bg_heigth))
		
		#scroll background
		scroll1 -= 5   
		scroll2 -= 5                                   #scroll te image of background
		#reset scroll
		if abs(scroll1) > bg_width:
			scroll1 = 0
		if abs(scroll2) > bg_width:
			scroll2 = 0

		#screen.blit(pygame.Surface((640, 400)), (bg_x,0))
		player1.move()
		player1.draw()
		player1.jump()
		player2.move()
		player2.draw()
		player2.jump()

		# obstacle1 Draw
		obstacle1 = pygame.draw.polygon(player1_display,(255, 0, 0), [[obstacle1_x, obstacle1_y], [obstacle1_x + 50, obstacle1_y], [obstacle1_x + 25, obstacle1_y - 50]])
		obstacle2 = pygame.draw.polygon(player2_display, (255, 0, 0), [[obstacle2_x, obstacle2_y], [obstacle2_x + 50, obstacle2_y], [obstacle2_x + 25, obstacle2_y - 50]])

		# Update score for player 1
		if obstacle1_x + 50 < 0:
			score1 += 1

		# Update score for player 2
		if obstacle2_x + 50 < 0:
			score2 += 1

		# Reset obstacle position and speed fro player 1
		if obstacle1_x + 50 < 0:
			obstacle1_x = SCREEN_WIDTH
			obstacle1_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle1_speed += 1

		# Reset obstacle position and speed for player 2
		if obstacle2_x + 50 < 0:
			obstacle2_x = SCREEN_WIDTH
			obstacle2_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle2_speed += 1

		# Move obstacle
		obstacle1_x -= obstacle1_speed

		# Move obstacle
		obstacle2_x -= obstacle1_speed

		# Display player 1 score
		font = pygame.font.Font(None, 30)

		text = font.render("Player 1 Score: " + str(score1), True, (0, 0, 0))
		player1_display.blit(text, (10, 10))

		# Display player 2 score
		text = font.render("Player 2 Score: " + str(score2), True, (0, 0, 0))
		player2_display.blit(text, (10, 10))

		# Check for collisions

		if obstacle1.colliderect(p1_for_collision) == True:
			obstacle1_speed = 0
			scroll1 = 0
			alive = False
		
		# Reset de posições player 1
			player1_x = SCREEN_WIDTH*0.05
			player1_y = (SCREEN_HEIGHT/2)*0.7
			player1_width = 50
			player1_height = 50
			obstacle1_x = SCREEN_WIDTH
			obstacle1_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle1_speed = 7
			score1 = 0
			player2_x = SCREEN_WIDTH*0.05
			player2_y = (SCREEN_HEIGHT/2)*0.7
			player2_width = 50
			player2_height = 50
			obstacle2_x = SCREEN_WIDTH
			obstacle2_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle2_speed = 7
			score1 = 0


			



		if obstacle2.colliderect(p2_for_collision) == True:
			obstacle2_speed = 0
			scroll2 = 0
			alive = False

			
		# Reset de posições player 1
			player1_x = SCREEN_WIDTH*0.05
			player1_y = (SCREEN_HEIGHT/2)*0.7
			player1_width = 50
			player1_height = 50
			obstacle1_x = SCREEN_WIDTH
			obstacle1_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle1_speed = 7
			score1 = 0
			player2_x = SCREEN_WIDTH*0.05
			player2_y = (SCREEN_HEIGHT/2)*0.7
			player2_width = 50
			player2_height = 50
			obstacle2_x = SCREEN_WIDTH
			obstacle2_y = (SCREEN_HEIGHT/2)*0.7+50
			obstacle2_speed = 7
			score2 = 0


		
			


		pygame.display.update()
		#pygame.display.flip()                   # display update, de forma a fazer update a todo o ecrã
	pygame.display.update()
pygame.quit()                   # FIM DO JOGO - Obrigatório