import pygame
import os
import random


class Mob(pygame.sprite.Sprite):
    image_1 = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_1, False, True)
    image_1.set_colorkey((255, 255, 255))

    image_2 = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_2, False, True)
    image_2.set_colorkey((255, 255, 255))

    image_3 = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_3, False, True)
    image_3.set_colorkey((255, 255, 255))

    image_4 = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_4, False, True)
    image_4.set_colorkey((255, 255, 255))

    image_5 = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_5, False, True)
    image_5.set_colorkey((255, 255, 255))

    image_1_nf = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_1_nf, False, True)
    image_1_nf.set_colorkey((255, 255, 255))

    image_2_nf = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_2_nf, False, True)
    image_2_nf.set_colorkey((255, 255, 255))

    image_3_nf = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_3_nf, False, True)
    image_3_nf.set_colorkey((255, 255, 255))

    image_4_nf = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_4_nf, False, True)
    image_4_nf.set_colorkey((255, 255, 255))

    image_5_nf = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\Car1.png')
    pygame.transform.flip(image_5_nf, False, True)
    image_5_nf.set_colorkey((255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Mob.image
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 500
        self.vx = 0
        self.vy = 0
        self.place_in_place = []
        self.place = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.car = [image_1, image_2,
                    image_3, image_4, image_5]
        self.car_nf = [image_1_nf, image_2_nf,
                       image_3_nf, image_4_nf, image_5_nf]

    def mob_generate(self):
        for i in range(5):
            self.place_in_place.append(random.randint(0, 3))
        for i in self.place_in_place:
            if i != 0:
                continue
            self.place[i] = 1

    def coin_generate(self):
        for i in range(5):
            self.place_in_place.append(random.randint(0, 3))
        for i in self.place_in_place:
            if i != 0:
                continue
            self.place[i] = 2

    def nitro_generate(self):
        for i in range(5):
            self.place_in_place.append(random.randint(0, 3))
        for i in self.place_in_place:
            if i != 0:
                continue
            self.place[i] = 3

    def reset(self):
        self.place = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

    def render(self):
        for place in self.place:
            for item in i:
                if item == 1:
                    if item.index(item) == 0:
                        return ((100, 0), 'Left', random.choice(self.car))
                    if place.index(item) == 1:
                        return (300, 0), 'Left', random.choice(self.car)
                    if place.index(item) == 2:
                        return ((500, 0), 'Right', random.choice(self.car_nf))
                    if place.index(item) == 3:
                        return ((700, 0), 'Right', random.choice(self.car_nf))
                if item == 2:
                    if place.index(item) == 0:
                        return (100, 0)
                    if place.index(item) == 1:
                        return (300, 0)
                    if place.index(item) == 2:
                        return (500, 0)
                    if place.index(item) == 3:
                        return (700, 0)
                if item == 3:
                    if place.index(item) == 0:
                        return (100, 0)
                    if place.index(item) == 1:
                        return (300, 0)
                    if place.index(item) == 2:
                        return (500, 0)
                    if place.index(item) == 3:
                        return (700, 0)
