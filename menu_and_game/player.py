import pygame
import os


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\car.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 315
        self.rect.y = 645
        self.vx = 0
        self.vy = 0

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.rect.x > 0:
                    self.vx = -1
            if event.key == pygame.K_a:
                if self.rect.x > 0:
                    self.vx = -1
            if event.key == pygame.K_RIGHT:
                if self.rect.x < 800 - self.rect.width:
                    self.vx = 1
            if event.key == pygame.K_d:
                if self.rect.x < 800:
                    self.vx = 1
            self.rect.x += self.vx
