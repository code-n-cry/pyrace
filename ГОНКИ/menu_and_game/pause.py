import pygame
import os


class Pause:
    def __init__(self, screen):
        self.menu = False
        self.game = False
        self.screen = screen

    def render_pause(self):

        font = pygame.font.SysFont('Montserrat', 100)
        a = font.render(f'Нажмите Esc для выхода', True, (255, 0, 0))
        self.screen.blit(a, (200, 300))

    def quit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game = True


