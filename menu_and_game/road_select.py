import os
import pygame
from button import Button
from clickable_image import ClickableImage


class Road_select:
    def __init__(self, surface, menu, login):
        self.surface = surface
        self.menu = menu
        self.choosen = 4
        self.choosen_road = 0
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.login = login
        self.roads = ['road', 'road_v2', 'road_v3', 'ice_road']
        self.images = self.load_images()
        self.buttons = self.load_buttons()

    def load_images(self):
        images = []
        x, y = 100, 40
        for elem in self.roads:
            image = ClickableImage(x, y, elem, self.surface)
            images.append(image)
            if x < 600:
                x += 250
            else:
                y += 270
                x = 100
        return images

    def load_buttons(self):
        x, y = self.surface.get_width() // 3 - 135, 210
        buttons = []
        for i in range(len(self.roads)):
            if i != self.choosen:
                i = Button(x - 25, y + 5, 80, 30, 'Выбрать', self.surface,
                           (66, 245, 206),
                           (0, 0, 0), (227, 66, 245), 0, 25, self.choose)
            else:
                i = Button(x - 25, y + 5, 80, 30, 'Выбрано', self.surface,
                           (66, 245, 206),
                           (0, 0, 0), (227, 66, 245), 0, 25, self.choose)
            buttons.append(i)
            if x < 600:
                x += 250
            else:
                y += 270
                x = 135
        buttons.append(
            Button(106, 650, 80, 30, 'Выбрать', self.surface, (66, 245, 206),
                   (0, 0, 0), (227, 100, 245), 0, 25, self.choose))
        return buttons

    def change_text(self):
        for i in range(len(self.buttons)):
            if i != self.choosen:
                self.buttons[i].set_text('Выбрать')
            else:
                self.buttons[i].set_text('Выбрано')

    def choose(self):
        if self.choosen == 4:
            self.choosen_road = 0
        else:
            self.choosen_road = pygame.transform.scale(
                self.images[self.choosen].orig_image, (800, 800))

    def check_mouse_motion(self, pos):
        for btn in self.buttons:
            btn.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for btn in self.buttons:
            btn.check_mouse_down(pos)
            if btn.state == 'pressed':
                self.choosen = self.buttons.index(btn)
        for img in self.images:
            img.check_mouse_down(pos)

    def check_mouse_up(self):
        for btn in self.buttons:
            btn.check_mouse_up()

    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.menu.in_roads:
                self.menu.in_roads = False
                return True

    def render(self):
        for i in self.images:
            i.render()
        for btn in self.buttons:
            btn.render()
        font = pygame.font.SysFont('Montserrat', 50)
        text = font.render(f'Случайная дорога', True, (0, 106, 98))
        self.surface.blit(text, (65, 600))
        self.change_text()
