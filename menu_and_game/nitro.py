import pygame
import os
import random


class Nitro(pygame.sprite.Sprite):
    def __init__(self, group, road, x, y):
        super().__init__(group)
        self.speed = road.speed
        self.image = pygame.image.load(random.choice(self.load_images()))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        images = []
        path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\'
        for i in range(1, 5):
            images.append(path + f'nitro{i}.png')
        return images

    def update(self, event):
        if self.rect.y < 750:
            self.rect.y += self.speed
        else:
            self.kill()