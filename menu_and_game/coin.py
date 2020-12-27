import pygame
import os


class Coin(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\menu_data\\coin.jpg')

    def __init__(self, group):
        super().__init__(group)
        self.image = Coin.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400

