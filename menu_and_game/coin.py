import pygame
import os


class Coin(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\coin.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Coin.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y

    def update(self):
        if self.rect.y < 750:
            self.rect.y += 2
        else:
            self.rect.y = self.y

