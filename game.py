#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

level_number = 1
number_of_levels = 2

font = pygame.font.SysFont("comicsans", 60)
small_font = pygame.font.SysFont("comicsans", 30)
boss_defeated_msg = font.render("Congretulations ! You Won !", False, (0, 0, 0))
treasure_found_msg = font.render("Yeah ! You just found a treasure !", False, (0, 0, 0))
level_number_msg = font.render("Level : {}".format(level_number), False, (255, 255, 255))

finished = False
leaving_button = False
treasure_found = False
boss_fight_started = False

boss_life_points = 20
boss_alive = True

player_position_x = 65
player_position_y = 650

opponent_position_x = 770
opponent_position_y = 600

opponent_moving_right = True
opponent_moving_left = False

treasure_position_x = 450
treasure_position_y = 560

boss_defeated_msg_position_x = 250
boss_defeated_msg_position_y = 500

level_reached_number_msg_position_x =250
level_reached_number_msg_position_y = 600

treasure_found_msg_position_x = 250
treasure_found_msg_position_y = 300

player_profil_img = pygame.image.load("player.png")
player_profil_img = pygame.transform.scale(player_profil_img, (80, 80)) #scale it
player_profil_img = player_profil_img.convert_alpha()

opponent_profil_img = pygame.image.load("opponent.png")
opponent_profil_img = pygame.transform.scale(opponent_profil_img, (80, 80))
opponent_profil_img = opponent_profil_img.convert_alpha()

treasure_img = pygame.image.load("treasure.jpeg")
treasure_img = pygame.transform.scale(treasure_img, (60 ,60))
treasure_img = treasure_img.convert_alpha()

background_img = pygame.image.load("background.jpeg")
background_img = pygame.transform.scale(background_img, (1000, 1000))

screen.blit(background_img, (0, 0))
screen.blit(treasure_img, (treasure_position_x, treasure_position_y))

white = (255, 255, 255)

frame = pygame.time.Clock()

def put_player_back():
	global player_position_x
	global player_position_y

	player_position_x = 65
	player_position_y = 650

def update_screen():
	# Background
	screen.blit(background_img, (0, 0))

	# Level Number Message
	screen.blit(level_number_msg, (0, 0))

while not leaving_button and not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			leaving_button = True

	pressed_keys = pygame.key.get_pressed()

	if pressed_keys[pygame.K_ESCAPE] == 1:
		leaving_button = True
	if pressed_keys[pygame.K_UP] == 1:
		player_position_y -= 5
	if pressed_keys[pygame.K_DOWN] == 1:
		player_position_y += 5
	if pressed_keys[pygame.K_LEFT] == 1:
		player_position_x -= 5
	if pressed_keys[pygame.K_RIGHT] == 1:
		player_position_x += 5

	# Boss move
	if opponent_position_x >= 770:
		opponent_moving_right = True
		opponent_moving_left = False
	if opponent_position_x <= 730:
		opponent_moving_left = True
		opponent_moving_right = False

	if opponent_moving_right:
		if level_number == 1:
			opponent_position_x -= 1
		elif level_number == 2:
			opponent_position_x -= 2
		elif level_number == 3:
			opponent_position_x -= 3

	if opponent_moving_left:
		if level_number == 1:
			opponent_position_x += 1
		elif level_number == 2:
			opponent_position_x += 2
		elif level_number == 3:
			opponent_position_x += 3

	# Treasure
	if abs(player_position_x - treasure_position_x) < 60 and abs(player_position_y - treasure_position_y) < 60 and not treasure_found:
		print("Player found a treasure !")
		screen.blit(treasure_found_msg, (treasure_found_msg_position_x, treasure_found_msg_position_y))
		pygame.display.flip()
		frame.tick(1)
		treasure_found = True
	if abs(player_position_x - treasure_position_x) > 60 or abs(player_position_y - treasure_position_y) > 60: #circular hitbox with a radius of 30
		print("Distance x : {}, Distance y : {}".format(player_position_x - treasure_position_x, player_position_y - treasure_position_y))

	# Boss
	if abs(player_position_x - opponent_position_x) < 81 and abs(player_position_y - opponent_position_y) < 81: #circular hitbox with a radius of 40.5
		print("Player is fighting the Boss !")
		boss_life_points -= 1
		print("Boss life : {}".format(boss_life_points))

		# Make hero takes damages
		player_position_x -= 10
		player_position_y -= 10

		if boss_life_points <= 0:
			boss_alive = False

	update_screen()

	if not treasure_found:
		screen.blit(treasure_img, (treasure_position_x, treasure_position_y))
	if boss_alive:
		screen.blit(opponent_profil_img, (opponent_position_x, opponent_position_y))
		screen.blit(player_profil_img, (player_position_x, player_position_y))
	if not boss_alive:

		put_player_back()

		treasure_found = False
		boss_alive = True
		boss_life_points = 20

		level_number += 1
		level_number_msg = font.render("Level : {}".format(level_number), False, (255, 255, 255))
		level_reached_number_msg = font.render("You've reached the level number {}".format(level_number), False, (0, 0, 0))

		screen.fill(white)
		screen.blit(boss_defeated_msg, (boss_defeated_msg_position_x, boss_defeated_msg_position_y))
		screen.blit(level_reached_number_msg, (level_reached_number_msg_position_x, level_reached_number_msg_position_y))

		pygame.display.flip()
		frame.tick(5)
		time.sleep(3)

	if level_number > number_of_levels:
		finished = True

	# Update the display
	pygame.display.flip()

	# 1/30 of a frame
	frame.tick(30)
