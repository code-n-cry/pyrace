import os
import pygame
from button import Button


class Settings:
    def __init__(self, surface, menu, login):
        self.surface = surface
        self.menu = menu
        self.choosen_m_volume = 5
        self.choosen_s_volume = 5
        self.login = login
        self.buttons = self.load_buttons()
        self.buttons_m = self.buttons[:12]
        self.buttons_s = self.buttons[12:]

    def load_buttons(self):
        buttons = []
        x = 50
        y = 300
        for i in range(23):
            x += 60
            if i < 11:
                a = Button(x, y, 40, 40, f'{i}', self.surface,
                           (66, 245, 206),
                           (0, 0, 0), (227, 66, 245), 0, 25, self.choose, True)
            if i == 11:
                x = 50
                y = 450
            if i > 11:
                a = Button(x, y, 40, 40, f'{i - 12}', self.surface,
                           (66, 245, 206),
                           (0, 0, 0), (227, 66, 245), 0, 25, self.choose, True)
            buttons.append(a)
        return buttons

    def choose(self):
        if self.choosen < 11:
            self.choosen_m_volume = self.choosen
        else:
            self.choosen_s_volume = self.choosen - 12

    def change_value(self):
        for btn in self.buttons:
            btn.button_color = (66, 245, 206)
        for btn in self.buttons_m:
            if int(btn.text) == self.choosen_m_volume:
                btn.button_color = (255, 255, 255)
        for btn in self.buttons_s:
            if int(btn.text) == self.choosen_s_volume:
                btn.button_color = (255, 255, 255)

    def check_mouse_motion(self, pos):
        for btn in self.buttons:
            btn.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for btn in self.buttons:
            btn.check_mouse_down(pos)
            if btn.state == 'pressed':
                self.choosen = self.buttons.index(btn)
                print(self.choosen)

    def check_mouse_up(self):
        for btn in self.buttons:
            btn.check_mouse_up()

    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.menu.in_settings:
                self.menu.in_settings = False
                return True

    def render(self):
        self.change_value()
        for btn in self.buttons:
            btn.render()
        font = pygame.font.SysFont('Montserrat', 35)
        text = font.render(f'Музыка', True, (0, 106, 98))
        self.surface.blit(text, (10, 315))
        font2 = pygame.font.SysFont('Montserrat', 35)
        text2 = font2.render(f'Звуки', True, (0, 106, 98))
        self.surface.blit(text2, (15, 465))
        font3 = pygame.font.SysFont('Montserrat', 50)
        text3 = font3.render(f'НАСТРОЙКИ', True, (0, 106, 98))
        self.surface.blit(text3, (300, 80))
