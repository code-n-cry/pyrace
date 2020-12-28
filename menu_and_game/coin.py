import pygame
import os
import random


class Coin(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\coin.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Coin.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = 5
        self.y = y
        self.x_place = [94, 281, 500, 700]

    def update(self, event):
        print(self.rect.y)
        if self.rect.y < 750:
            self.rect.y += self.vy
        else:
            self.kill()

