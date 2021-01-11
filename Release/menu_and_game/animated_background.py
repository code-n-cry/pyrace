import pygame
import os


class Car(pygame.sprite.Sprite):
    """Аниммированый фон для меню"""

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.car_images = []
        self.path = '/'.join(os.getcwd().replace('\\', '/').split('/')[:-1]) + '/menu_and_game/menu_data/'
        self.not_gif_img = pygame.image.load(self.path + 'car1.gif')
        self.not_gif_img = pygame.transform.scale(self.not_gif_img, (width, height))
        self.image = self.not_gif_img
        self.rect = self.image.get_rect()
        self.frame = 0
        self.delay = 4
        self.pause = 0
        self.width = width
        self.height = height
        self.load_images()

    def update(self):
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
        if self.frame >= len(self.car_images):
            self.frame = 0
        self.image = self.car_images[self.frame]

    def load_images(self):
        """Загружаем картинки для гифки"""

        for i in range(1, 13):
            image_name = self.path + 'car%d.gif' % i
            image = pygame.image.load(image_name)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.car_images.append(image)
