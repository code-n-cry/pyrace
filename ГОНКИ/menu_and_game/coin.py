import pygame
import os


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\coin.jpg')
    image.set_colorkey((255, 255, 255))

