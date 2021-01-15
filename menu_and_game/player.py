import pygame
from pygame.locals import *
import os
import json


class Player(pygame.sprite.Sprite):
    """Спрайт игрока. Класс реализует движение игрока, анимации движения, получение
    характеристик выбранной машины из json-файла"""

    def __init__(self, group, chosen_car=1):
        super().__init__(group)
        self.path = '\\'.join(os.getcwd().split('\\')[:-1])
        Player.image = pygame.image.load(
            self.path + f'\\menu_and_game\\game_data\\Car{chosen_car}.png')
        self.image = Player.image
        self.image.set_colorkey((255, 255, 255))
        self.img_name = f'Car{chosen_car}'
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 580
        self.vx = 0
        self.vy = 0
        self.got_coins = 0
        self.crashed = False
        self.can_move = True
        self.bg_time = 0

    def update(self, event):
        if self.can_move:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        self.move_left()
                    elif event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_d:
                        self.move_right()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    else:
                        self.vx = 0
                    if not self.check():
                        self.rect.x += self.vx
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.unmove_left()
                    if event.key == pygame.K_a:
                        self.unmove_left()
                    if event.key == pygame.K_RIGHT:
                        self.unmove_right()
                    if event.key == pygame.K_d:
                        self.unmove_right()
            except AttributeError:
                pass

    def set_speed(self):
        need_data = None
        with open(self.path + '\\menu_and_game\\game_data\\cars.json', encoding='utf-8') as data:
            all_data = json.load(data)
        for i in all_data['cars']:
            if i['id'] == self.img_name:
                need_data = i
        speed = need_data['speed']
        return speed

    def move_left(self):
        if self.rect.x > 0:
            self.vx = -self.set_speed()
            self.image = pygame.transform.rotate(Player.image, 30)
            pygame.draw.lines(self.image, (255, 0, 0), True, [(0, 0), (0, 180), (100, 180), (100, 0)])
            self.image.set_colorkey((255, 255, 255))

    def move_right(self):
        if self.rect.x < 800 - self.rect.width:
            self.vx = self.set_speed()
            self.image = pygame.transform.rotate(Player.image, 330)
            pygame.draw.lines(self.image, (255, 0, 0), True, [(0, 0), (0, 180), (100, 180), (100, 0)])
            self.image.set_colorkey((255, 255, 255))

    def unmove_left(self):
        if self.rect.x > 0:
            self.image = Player.image
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (100, 180))

    def unmove_right(self):
        if self.rect.x < 800 - self.rect.width:
            self.image = Player.image
            self.image = pygame.transform.scale(self.image, (100, 180))
            self.image.set_colorkey((255, 255, 255))

    def check(self):
        if 0 <= self.rect.x <= 690:
            return False
        else:
            self.can_move = False
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
