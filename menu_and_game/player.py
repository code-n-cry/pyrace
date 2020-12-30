import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, group, choosen_car=1):
        super().__init__(group)
        self.path = '\\'.join(os.getcwd().split('\\')[:-1])
        Player.image = pygame.image.load(self.path + f'\\menu_and_game\\game_data\\Car{choosen_car}.png')
        self.image = Player.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580
        self.vx = 0
        self.vy = 0
        self.got_coins = 0

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.rect.x > 0:
                    self.vx = -3
                    self.image = pygame.transform.rotate(Player.image, 30)
                    self.image.set_colorkey((255, 255, 255))
            elif event.key == pygame.K_RIGHT or event.KEY == pygame.K_d:
                if self.rect.x < 800 - self.rect.width:
                    self.vx = 3
                    self.image = pygame.transform.rotate(Player.image, 330)
                    self.image.set_colorkey((255, 255, 255))
            else:
                self.vx = 0
            if not self.check():
                self.rect.x += self.vx
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.rect.x > 0:
                    self.image = Player.image
                    self.image.set_colorkey((255, 255, 255))
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.rect.x < 800 - self.rect.width:
                    self.image = Player.image
                    self.image.set_colorkey((255, 255, 255))

    def check(self):
        if 0 <= self.rect.x <= 700:
            return False
        return True

    def respawn(self):
        self.rect.x = 450

    def update_image(self, choosen):
        Player.image = pygame.image.load(self.path + f'\\menu_and_game\\game_data\\Car{choosen}.png')
        self.image = Player.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580