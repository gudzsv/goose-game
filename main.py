# Game BANDERO GOOSE
import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

# Screen view property
HEIGHT = 800
WIDTH = 1200
# Score Font
FONT = pygame.font.SysFont('Verdana', 40)
COLOR_BLACK = (0, 0, 0)

ZERO = 0
TIMER_ENEMY_M_SEC = 1500
TIMER_BONUS_M_SEC = 3000
TIMER_GOOSE_M_SEC = 200


# Create Display
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('./image/background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "./image/animation/"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# Player properties
player_size = (20, 20)
player = pygame.image.load("./image/player.png").convert_alpha()
player_rect = pygame.Rect(20, 300, *player_size)
#  4 or -4 - it is player speed
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]


# Create Enemy function
def create_enemy():
		# Enemy properties
		enemy_size = (30, 30)
		enemy = pygame.image.load("./image/enemy.png").convert_alpha()
		enemy_rect = pygame.Rect(WIDTH, random.randint(100, 700), *enemy_size)
		enemy_move = [random.randint(-8, -4), 0]
		return [enemy, enemy_rect, enemy_move]

# Create Bonuses function
def create_bonus():
		# Bonus properties
		bonus_size = (60, 60)
		bonus = pygame.image.load("./image/bonus.png").convert_alpha()
		bonus_rect = pygame.Rect(random.randint(200, 1000), 0, *bonus_size)
		bonus_move = [0, random.randint(4, 8)]
		return [bonus, bonus_rect, bonus_move]


# Create Enemy Event
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, TIMER_ENEMY_M_SEC)

# Create Bonus Event
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, TIMER_BONUS_M_SEC)

# Create Goose animation Event
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, TIMER_GOOSE_M_SEC)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True

while playing:
		FPS.tick(130)
		for event in pygame.event.get():
			if event.type == QUIT:
				playing = False
			if event.type == CREATE_ENEMY:
				enemies.append(create_enemy())
			if event.type == CREATE_BONUS:
				bonuses.append(create_bonus())
			if event.type == CHANGE_IMAGE:
				player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
				image_index += 1
				if image_index >= len(PLAYER_IMAGES):
					image_index = 0


		# Add background to the Screen
		bg_x1 -= bg_move
		bg_x2 -= bg_move

		if bg_x1 < -bg.get_width():
			bg_x1 = bg.get_width()
		if bg_x2 < -bg.get_width():
			bg_x2 = bg.get_width()

		main_display.blit(bg, (bg_x1, 0))
		main_display.blit(bg, (bg_x2, 0))

		# Player control
		keys = pygame.key.get_pressed()

		if keys[K_DOWN] and player_rect.bottom < HEIGHT:
			player_rect = player_rect.move(player_move_down)

		if keys[K_UP] and player_rect.top >= ZERO:
			player_rect = player_rect.move(player_move_up)

		if keys[K_RIGHT] and player_rect.right < WIDTH:
			player_rect = player_rect.move(player_move_right)

		if keys[K_LEFT] and player_rect.left >= ZERO:
			player_rect = player_rect.move(player_move_left)

		for enemy in enemies:
			enemy[1] = enemy[1].move(enemy[2])
			main_display.blit(enemy[0], enemy[1])

			if player_rect.colliderect(enemy[1]):
				playing = False

		for bonus in bonuses:
			bonus[1] = bonus[1].move(bonus[2])
			main_display.blit(bonus[0], bonus[1])

			if player_rect.colliderect(bonus[1]):
				# Add bonus to Score
				score += 1
				# Remove bomnus from Screen
				bonuses.pop(bonuses.index(bonus))

		# Add Score to Screen
		main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
		# Add Player to Screen
		main_display.blit(player, player_rect)

		pygame.display.flip()

		for enemy in enemies:
			if enemy[1].left < 0:
				enemies.pop(enemies.index(enemy))

		for bonus in bonuses:
			if bonus[1].bottom > HEIGHT:
				bonuses.pop(bonuses.index(bonus))
