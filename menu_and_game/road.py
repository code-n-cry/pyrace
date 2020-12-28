import pygame
import os

road_default = pygame.image.load(
    '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\road.jpg')
road_default = pygame.transform.scale(road_default, (800, 800))


class Road:
    def __init__(self, screen):
        self.image = road_default
        self.pos = 0
        self.screen = screen
        self.screen.fill((0, 0, 0))
        self.speed = 5

    def move(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (0, 0), (0, 800 - self.pos, 800, 800))
        self.screen.blit(self.image, (0, self.pos))
        self.pos += self.speed
        if self.pos >= 800:
            self.pos = 0
        return self.screen

