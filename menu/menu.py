import pygame
import os


def run_out():
    global running
    running = False


class Button:
    def __init__(self, x, y, w, h, text, surface, bcolor, tcolor, hcolor, border, tsize, func, centr_text=False):
        self.font = pygame.font.SysFont('Roboto', tsize)
        self.bound = pygame.Rect(x, y, w, h)
        self.text = text
        self.surface = surface
        self.button_color = bcolor
        self.text_color = tcolor
        self.hover_color = hcolor
        self.border = border
        self.state = 'normal'
        self.on_click_func = func
        self.centralize_text = centr_text

    def render(self):
        if self.state == 'normal':
            pygame.draw.rect(self.surface, self.button_color, self.bound, self.border)
            self.render_text(self.bound.x + 2, self.bound.y + 5)
        else:
            pygame.draw.rect(self.surface, self.hover_color, self.bound, self.border)
            self.render_text(self.bound.x + 2, self.bound.y + 5)

    def render_text(self, x, y):
        text_object = self.font.render(self.text, False, self.text_color)
        if not self.centralize_text:
            self.surface.blit(text_object, (x, y))
        else:
            pos = (x - self.bound.width // 2, y)
            self.surface.blit(text_object, pos)

    def check_mouse_motion(self, pos):
        if self.bound.collidepoint(pos[0], pos[1]):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def check_mouse_down(self, pos):
        if self.bound.collidepoint(pos[0], pos[1]):
            self.state = 'pressed'

    def check_mouse_up(self):
        if self.state == 'pressed':
            self.on_click()
            self.state = 'hover'

    def on_click(self):
        self.on_click_func()


path_to_file = '/'.join(os.getcwd().replace('\\', '/').split('/')[:-1]) + '/menu/data/bg.png'
background_image = pygame.transform.scale(pygame.image.load(path_to_file), (800, 800))
pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True
quit_button = Button(250, 350, 132, 50, 'Выход', screen, (153, 153, 153),
                     (0, 0, 0), (204, 204, 204), 0, 55, run_out)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            quit_button.check_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            quit_button.check_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            quit_button.check_mouse_up()
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    quit_button.render()
    pygame.display.flip()
