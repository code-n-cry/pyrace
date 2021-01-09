import pygame


class Road:
    def __init__(self, screen, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (800, 800))
        self.pos = 0
        self.screen = screen
        self.screen.fill((0, 0, 0))

    def move(self, speed):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (0, 0), (0, 800 - self.pos, 800, 800))
        self.screen.blit(self.image, (0, self.pos))
        self.pos += speed
        if self.pos >= 800:
            self.pos = 0
        return self.screen
