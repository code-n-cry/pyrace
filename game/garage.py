import os
import sqlite3
import pygame
from button import Button


class Garage:
    def __init__(self, surface, menu, login):
        self.surface = surface
        self.menu = menu
        self.images = []
        self.buttons = []
        self.choosen = 0
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.login = login
        self.connect = sqlite3.connect(self.path + '\\game_data\\users_info.db')
        self.cars = []
        self.update_cars()

    def load_images(self):
        path = self.path + '\\game_data\\'
        images = []
        for i in self.cars:
            image = pygame.image.load(path + f'Car{i}.png')
            image = pygame.transform.flip(image, True, False)
            image = pygame.transform.scale(image, (100, 170))
            images.append(image)
        return images

    def load_buttons(self):
        x, y = self.surface.get_width() // 3 - 135, 210
        buttons = []
        for i in range(len(self.cars)):
            if i != self.choosen:
                i = Button(x - 25, y, 80, 30, 'Выбрать', self.surface, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 25,
                           self.choose)
            else:
                i = Button(x - 25, y, 80, 30, 'Выбрано', self.surface, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 25,
                           self.choose)
            buttons.append(i)
            if x < 600:
                x += 250
            else:
                y += 270
                x = 135
        return buttons

    def change_text(self):
        for i in range(len(self.buttons)):
            if i != self.choosen:
                self.buttons[i].set_text('Выбрать')
            else:
                self.buttons[i].set_text('Выбрано')

    def check_mouse_motion(self, pos):
        for btn in self.buttons:
            btn.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for btn in self.buttons:
            btn.check_mouse_down(pos)
            if btn.state == 'pressed':
                self.choosen = self.buttons.index(btn)

    def check_mouse_up(self):
        for btn in self.buttons:
            btn.check_mouse_up()

    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu.choosen_car = self.choosen + 1
                return True

    def render(self):
        x, y = self.surface.get_width() // 3 - 170, 20
        for i in self.images:
            self.surface.blit(i, (x, y))
            self.buttons[self.images.index(i)].render()
            if x < 500:
                x += 250
            else:
                y += 270
                x = 100
        for btn in self.buttons:
            btn.render()
        self.change_text()

    def choose(self):
        cur = self.connect.cursor()
        last_data = cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0]
        new_data = '_'.join(last_data.split('_')[:-1] + [str(self.choosen + 1)])
        cur.execute('UPDATE info SET data=? WHERE login=?', (new_data, self.login))
        self.connect.commit()
        cur.close()

    def update_cars(self):
        cur = self.connect.cursor()
        raw_data = cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0]
        all_cars = raw_data.split('_')[1:]
        self.cars.clear()
        if len(all_cars) > 9:
            while len(all_cars) != 9:
                del all_cars[-1]
        for i in range(len(all_cars)):
            if all_cars[i] == '1':
                self.cars.append(i + 1)
        self.buttons = self.load_buttons()
        self.images = self.load_images()
        self.choosen = int(raw_data.split('_')[-1]) - 1
