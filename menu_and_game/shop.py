import pygame
import os
import sqlite3
from button import Button


class Shop:
    def __init__(self, surface):
        path_to_db = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\users_info.db'
        self.con = sqlite3.connect(path_to_db)
        self.images = []
        self.buttons = []
        self.load_images()
        self.surface = surface
        self.load_buttons()

    def load_images(self):
        path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\'
        for i in range(1, 10):
            image = pygame.image.load(path + f'Car{i}.png')
            image = pygame.transform.flip(image, True, False)
            image = pygame.transform.scale(image, (100, 170))
            self.images.append(image)

    def load_buttons(self):
        x, y = 125, 220
        first_price = 10
        for i in range(9):
            b = Button(x, y, 40, 30, str(first_price), self.surface, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 30,
                       self.buy, False)
            first_price += 10
            self.buttons.append(b)
            if x < 600:
                print(x)
                x += 250
            else:
                y += 270
                x = 125

    def render(self):
        x, y = 100, 40
        for i in self.images:
            self.surface.blit(i, (x, y))
            if x < 600:
                x += 250
            else:
                y += 270
                x = 100
        for i in self.buttons:
            i.render()

    def buy(self):
        pass

    def check_mouse_motion(self, pos):
        for i in self.buttons:
            i.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for i in self.buttons:
            i.check_mouse_down(pos)

    def check_mouse_up(self):
        for i in self.buttons:
            i.check_mouse_up()


if __name__ == '__main__':
    pygame.init()
    path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\menu_data\\'
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    shop = Shop(screen)
    bg = pygame.image.load(path + 'shop_bg.png')
    bg = pygame.transform.scale(bg, (800, 800))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                shop.check_mouse_motion(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                shop.check_mouse_down(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                shop.check_mouse_up()
        screen.blit(bg, (0, 0))
        shop.render()
        pygame.display.flip()
