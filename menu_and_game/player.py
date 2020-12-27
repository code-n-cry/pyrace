import pygame
import os


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    image.set_colorkey((255, 255, 255))

    def __init__(self, group, coin_group, enemy_group=False, nitro_group=False):
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580
        self.vx = 0
        self.vy = 0
        self.got_coins = 0

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.rect.x > 0:
                    self.vx = -3
            if event.key == pygame.K_RIGHT:
                if self.rect.x < 800 - self.rect.width:
                    self.vx = 3
            if not self.check():
                self.rect.x += self.vx
        if pygame.sprite.groupcollide(self.g)

    def check(self):
        if 0 <= self.rect.x <= 700:
            return False
        return True
