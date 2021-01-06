import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, group, choosen_car=1):
        super().__init__(group)
        self.path = '\\'.join(os.getcwd().split('\\')[:-1])
        Player.image = pygame.image.load(self.path + f'\\menu_and_game\\game_data\\Car{choosen_car}.png')
        self.image = Player.image
        self.image.set_colorkey((255, 255, 255))
        self.img_name = f'Car{choosen_car}'
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580
        self.vx = 0
        self.vy = 0
        self.got_coins = 0
        self.crashed = False
        self.can_move = True

    def update(self, event):
        if self.can_move:
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.rect.x > 0:
                            self.vx = -self.set_speed()
                            self.image = pygame.transform.rotate(Player.image, 30)
                            self.image = pygame.transform.scale(self.image, (140, 200))
                            self.image.set_colorkey((255, 255, 255))
                    elif event.key == pygame.K_RIGHT or event.KEY == pygame.K_d:
                        if self.rect.x < 800 - self.rect.width:
                            self.vx = self.set_speed()
                            self.image = pygame.transform.rotate(Player.image, 330)
                            self.image = pygame.transform.scale(self.image, (140, 200))
                            self.image.set_colorkey((255, 255, 255))
                    else:
                        self.vx = 0
                    if not self.check():
                        self.rect.x += self.vx
                except AttributeError:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.rect.x > 0:
                        self.image = Player.image
                        self.image.set_colorkey((255, 255, 255))
                        self.image = pygame.transform.scale(self.image, (100, 180))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.rect.x < 800 - self.rect.width:
                        self.image = Player.image
                        self.image = pygame.transform.scale(self.image, (100, 180))
                        self.image.set_colorkey((255, 255, 255))

    def set_speed(self):
        need_data = None
        with open(self.path + '\\menu_and_game\\menu_data\\data.txt', encoding='utf-8') as data:
            all_data = data.read().split('\n')
        for i in all_data:
            if i.split(':')[0] == self.img_name:
                need_data = i
        speed = int(need_data.split(':')[1].split(',')[1])
        return speed

    def check(self):
        if 0 <= self.rect.x <= 690:
            return False
        return True

    def respawn(self):
        self.rect.x = 450

    def update_image(self, choosen):
        Player.image = pygame.image.load(self.path + f'\\menu_and_game\\game_data\\Car{choosen}.png')
        self.image = Player.image
        self.image = pygame.transform.scale(self.image, (100, 180))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580
        self.img_name = f'Car{choosen}'
