import pygame
import sys
import os
import random
from scripts.robot import Robot
from scripts.parts import Part
from scripts.particle import Particle

import pygame.font
import pygame.mixer

pygame.font.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 800

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("iJackson")
ROBOT_WIDTH = 60
ROBOT_HEIGHT = 80

BG_COLOR = (111, 66, 138)
BLUE_COLOR = (0, 120, 215)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


SCORE_FONT = pygame.font.SysFont("comicsans", 100)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
ERROR_FONT = pygame.font.SysFont("comicsans", 30)

PARTS_TYPE_LIST = ["screw", "cable0", "cable1", "cable2", "skull", "hacker"]
ERROR_CAUSES = ["hacker"]
DEATH_CAUSES = ["skull"]
#PARTS_TYPE_LIST = ERROR_CAUSES

QR_CODE = pygame.transform.scale(
					pygame.image.load(os.path.join("assets", "error", "qr code2.png")), (150, 150))
GAME_BG = pygame.transform.scale(
					pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))

ERROR_SOUND = pygame.mixer.Sound(os.path.join("sfxs", "error.mp3"))
SCORE_SOUND = pygame.mixer.Sound(os.path.join("sfxs", "score.wav"))
BG_MUSIC = pygame.mixer.music.load(os.path.join("sfxs", "enivicivokke.mp3"))
pygame.mixer.music.set_volume(0.2)

SCORE_SOUND.set_volume(0.1)



def main():
	
	run = True
	gameover = False
	clock = pygame.time.Clock()

	part_list = []
	robot = Robot(WIDTH//2, HEIGHT-2*ROBOT_HEIGHT,
				  ROBOT_WIDTH, ROBOT_HEIGHT, SCREEN)
	part_list.append(Part(random.randint(0, WIDTH-50), 0, 3,
					 SCREEN, random.choice(PARTS_TYPE_LIST)))
	particle_list = []

	score = 0
	time_to_drop = 0
	
	time_limit = 8
	while run:
		clock.tick(75)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit(); sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# pygame.quit(); sys.exit()
					run = False
					pygame.mixer.music.stop()

				if not gameover:
					if event.key == pygame.K_LEFT:
						robot.vel = -abs(robot.vel)

					if event.key == pygame.K_RIGHT:
						robot.vel = abs(robot.vel)

					if event.key == pygame.K_UP:
						robot.vel = abs(robot.vel) + \
										1 if robot.vel > 0 else -abs(robot.vel)-1
						robot.update_sprite_incrementation()

					if event.key == pygame.K_DOWN:
						robot.vel = abs(robot.vel) - \
										1 if robot.vel > 0 else -abs(robot.vel)+1

				if event.key == pygame.K_r:
					main()
					run = False

				robot.update_sprite_incrementation()

		SCREEN.fill(BLACK)
		SCREEN.blit(GAME_BG, (0,0))

		# updating parts
		for part in part_list:
			part.update()
			if part.y >= HEIGHT:
				part_list.remove(part)
			#   part_list.append(Part(random.randint(0,WIDTH-50),0, 3, SCREEN, random.choice(PARTS_TYPE_LIST)))

			particle_list.append(
				Particle(part.x+part.image.get_width()/2, part.y-5,
				random.randint(0, 30)/10-1, -1*random.randint(0, 2*part.vel), 8, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), SCREEN)
				)

		# updating robot
		robot.update()

		particle_list.append(
			Particle(robot.x+robot.width/2, robot.y+robot.height/2+60,
					random.randint(0, 30)/10-1, random.randint(0, 30)/10-2, 8, 
					(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), SCREEN))

		# updating particles
		if len(particle_list) > 0:
			for i in range(len(particle_list)-1, -1, -1):
				particle = particle_list[i]
				particle.update()
				if particle.timer < 0:
					particle_list.remove(particle)

		# print("particle", len(particle_list))
		# print("parts", len(part_list))

		# checking for collisions, and updating part_list, and error
		if not gameover:
			for i in range(len(part_list)-1, -1, -1):
				part = part_list[i]
				p_type = part.type
				if part.rect.colliderect(robot.rect):
					SCORE_SOUND.play()
					part_list.pop(i)
					score += 1
					# error
					error = True
					password = random.randint(0,9)
					if p_type in ERROR_CAUSES:
						ERROR_SOUND.play(0)
						escape = False
						pygame.mixer.music.stop()
						while error:
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit(); sys.exit()

								if event.type == pygame.KEYDOWN:
									if event.key == pygame.K_ESCAPE:
										#pygame.quit(); sys.exit()
										error = False
										run = False
										return

									if (event.key in [pygame.K_0, pygame.K_KP0] and password == 0) \
										or (event.key in [pygame.K_1, pygame.K_KP1] and password == 1) \
										or (event.key in [pygame.K_2, pygame.K_KP2] and password == 2) \
										or (event.key in [pygame.K_3, pygame.K_KP3] and password == 3) \
										or (event.key in [pygame.K_4, pygame.K_KP4] and password == 4) \
										or (event.key in [pygame.K_5, pygame.K_KP5] and password == 5) \
										or (event.key in [pygame.K_6, pygame.K_KP6] and password == 6) \
										or (event.key in [pygame.K_7, pygame.K_KP7] and password == 7) \
										or (event.key in [pygame.K_8, pygame.K_KP8] and password == 8) \
										or (event.key in [pygame.K_9, pygame.K_KP9] and password == 9):
										error = False

							SCREEN.fill(BLUE_COLOR)
							draw_error_message()
							pygame.display.update()

						pygame.mixer.music.play()
					if p_type in DEATH_CAUSES:
						robot.health -= 1

		time_to_drop += 0.1+score/500
		if time_to_drop > time_limit:
			part_list.append(Part(random.randint(0, WIDTH-50), 0, 3, SCREEN, random.choice(PARTS_TYPE_LIST)))
			time_to_drop = 0
			time_limit -= 0.01
		

		draw_score(score)
		# draw_robot_health(robot.health)

		if robot.health == 0:
			draw_gameover_screen()
			gameover = True
			robot.vel = 0
				
		pygame.display.update()


def draw_score(score):
	text = str(score)
	text_img = SCORE_FONT.render(text, True, BLACK)
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2, 50+5))
	text_img = SCORE_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (WIDTH//2-text_img.get_width()//2, 50))

def draw_error_message():
	x = 200
	y = 200

	text = ":("
	text_img = SCORE_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 100

	text = "Your PC ran into a problem and needs to restart as soon as "
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 75

	text = "we´re finished collecting some error info"
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 75

	text = "XX% complete"
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 75

	SCREEN.blit(QR_CODE, (x, y))
	x += 160
	text = "JUST KIDDING. YOU HAVE TO ENTER THE CORRECT INTEGER [0,9] TO HANDLE IT"
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 50

	text = "FEEL FREE TO PUNCH YOUR KEYBORD"
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))
	y += 50

	text = "WE ARE NOT RESPONSIBLE FOR ANY DAMAGE THOUGH"
	text_img = ERROR_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (x, y))

def draw_robot_health(health):
	text = "HEALTH:" + str(health)
	text_img = HEALTH_FONT.render(text, True, BLACK)
	x, y = 0, 0
	SCREEN.blit(text_img, (x, y))
	text_img = HEALTH_FONT.render(text, True, WHITE)
	x += 2
	y += 2
	SCREEN.blit(text_img, (x, y))

def draw_gameover_screen():
	text = "GAMEOVER!!"
	text_img = SCORE_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2, HEIGHT//2+text_img.get_height()//2-200))

	text = "press R to restart"
	text_img = SCORE_FONT.render(text, True, WHITE)
	SCREEN.blit(text_img, (WIDTH//2+5-text_img.get_width()//2, HEIGHT//2+text_img.get_height()//2))

	pygame.display.update()



if __name__ == '__main__':
	main()
