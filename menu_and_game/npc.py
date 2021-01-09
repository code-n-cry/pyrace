import pygame
import os
from random import choice


class Npc(pygame.sprite.Sprite):
    """Вражеская машина, класс загружает для неё случайную картинку и отвечает за движение"""

    def __init__(self, group, x, y, flipped=False):
        super().__init__(group)
        self.naklad = False
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + f'\\menu_and_game\\game_data\\'
        self.image = self.load_images()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check = False
        if self.rect.x < 200:
            self.vy = 12
        else:
            self.vy = -7
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, event):
        if self.rect.x < 200:
            if self.rect.y < 920:
                self.rect.y += self.vy
            else:
                self.kill()
        else:
            if self.rect.y > -110:
                self.rect.y += self.vy
            else:
                self.kill()

    def load_images(self):
        images = []
        for i in range(1, 10):
            img = pygame.image.load(self.path + f'Car{i}.png')
            img = pygame.transform.scale(img, (100, 180))
            images.append(img)
        return choice(images)
