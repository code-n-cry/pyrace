import pygame


class Button:
    def __init__(self, x, y, w, h, text, surface, bcolor, tcolor, hcolor, border, tsize, func, centr_text=False):
        self.font = pygame.font.SysFont('Montserrat', tsize)
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
        text_object = self.font.render(self.text, True, self.text_color)
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
