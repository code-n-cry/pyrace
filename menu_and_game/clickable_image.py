import pygame
import os
import subprocess


class ClickableImage:
    """Кликабельная картинка. Позволяет выполнить какую-либо функцию при нажатии на неё"""

    def __init__(self, x, y, image, surface):
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.image = pygame.transform.scale(
            pygame.image.load(self.path + f'game_data\\{image}.png'), (100, 170))
        self.orig_image = pygame.image.load(self.path + f'game_data\\{image}.png')
        self.image = pygame.transform.flip(self.image, True, False)
        self.str_img = image
        self.bound = pygame.Rect(x, y, 100, 170)
        self.screen = surface

    def check_mouse_down(self, pos):
        if self.bound.collidepoint(pos[0], pos[1]):
            subprocess.call(f'python {self.path}info_window.py {self.str_img}')

    def render(self):
        self.screen.blit(self.image, (self.bound.x, self.bound.y))

    def get_name(self):
        return self.str_img
