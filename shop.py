import pygame
import os
import sqlite3
from button import Button


class Shop:
    def __init__(self, surface, login):
        self.return_menu = False
        path_to_db = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\users_info.db'
        self.con = sqlite3.connect(path_to_db)
        cur = self.con.cursor()
        data_str = cur.execute('SELECT data FROM info WHERE login=?', (login,)).fetchone()[0]
        cur.close()
        self.coins = int(data_str.split('_')[0][1:])
        self.cars = [int(i) for i in data_str.split('_')[1:]]
        self.bought_item = None
        self.surface = surface
        self.login = login
        self.images = []
        self.buttons = []
        self.load_buttons()
        self.load_images()

    def load_images(self):
        path_to_img = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\'
        for i in range(1, 10):
            image = pygame.image.load(path_to_img + f'Car{i}.png')
            image = pygame.transform.flip(image, True, False)
            image = pygame.transform.scale(image, (100, 170))
            self.images.append(image)

    def load_buttons(self):
        x, y = 135, 220
        first_price = 10
        for i in range(9):
            if self.cars[i] == 1:
                b = Button(x - 25, y, 75, 30, 'Куплено', self.surface, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 25,
                           self.buy, False)
            else:
                b = Button(x, y, 32, 30, first_price, self.surface, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 35,
                           self.buy, False)
            self.buttons.append(b)
            first_price += 5
            if x < 600:
                x += 250
            else:
                y += 270
                x = 135

    def render(self):
        x, y = 100, 40
        for i in self.images:
            self.surface.blit(i, (x, y))
            self.buttons[self.images.index(i)].render()
            if x < 600:
                x += 250
            else:
                y += 270
                x = 100
        self.render_text()

    def buy(self):
        price = self.buttons[self.bought_item].get_text()
        if price.isdigit():
            if self.coins >= int(price):
                self.buttons[self.bought_item].set_text('Куплено')
                x, y, w, h = self.buttons[self.bought_item].get_coords()
                self.buttons[self.bought_item].set_coords((x - 25, y, w + 45, h), 25)
                self.coins -= int(price)
                self.cars[self.bought_item] = 1
                if self.coins > 0:
                    coins = '0' * len(str(1000 - self.coins)) + str(self.coins)
                else:
                    coins = '0' * 4
                cars_for_db = '_'.join([str(i) for i in self.cars])
                str_for_db = f'#{coins}_{cars_for_db}'
                cur = self.con.cursor()
                cur.execute('UPDATE info SET data=? WHERE login=?', (str_for_db, self.login))
                self.con.commit()
                cur.close()
            else:
                print('Недостаточно средств!')
        else:
            print('Вы уже купили эту машину!')

    def check_mouse_motion(self, pos):
        for i in self.buttons:
            i.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for i in self.buttons:
            i.check_mouse_down(pos)
            if i.state == 'pressed':
                self.bought_item = self.buttons.index(i)

    def check_mouse_up(self):
        for i in self.buttons:
            i.check_mouse_up()

    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True

    def render_text(self):
        font = pygame.font.SysFont('Montserrat', 30)
        text = font.render(f'Ваши монеты: {self.coins}', True, (255, 255, 255))
        self.surface.blit(text, (0, 15))
    def update_coins(self):
        cur = self.con.cursor()
        self.coins = int(
            cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0][1:].split('_')[0])