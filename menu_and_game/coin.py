import pygame
import os


class Coin(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\coin.png')

    def __init__(self, group, x, y, road):
        super().__init__(group)
        self.image = Coin.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = road.speed

    def update(self, event):
        if self.rect.y < 850:
            self.rect.y += self.vy
        else:
            self.kill()
