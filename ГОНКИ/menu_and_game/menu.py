import sys

import pygame
import os
import sqlite3
from animated_background import Car
from player import Player
from button import Button


class Menu:
    def __init__(self, user_login):
        path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game'
        self.con = sqlite3.connect(path + '\\game_data/users_info.db')
        cur = self.con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS info(login, data)')
        self.con.commit()
        self.coins = 0
        self.cars = 1
        logins = [i[0]
                  for i in cur.execute('SELECT login FROM info').fetchall()]
        if user_login not in logins:
            cur.execute('INSERT INTO info VALUES(?, ?)',
                        (user_login, '#0000_01_001'))
            self.con.commit()
        else:
            data = cur.execute(
                'SELECT data FROM info where login=?', (user_login, )).fetchone()[0]
            self.coins = int(data.split('_')[0][1:])
            self.cars = int(data.split('_')[1])
        self.start_button = Button(10, 10, 132, 50, 'Играть', screen, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 55,
                                   self.start_game)
        self.quit_button = Button(658, 8, 132, 45, 'Выход', screen, (66, 245, 206),
                                  (0, 0, 0), (227, 66, 245), 0, 50, self.quit)
        self.shop_button = Button(10, 70, 132, 45, 'Магазин', screen, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 46,
                                  self.shop)
        self.buttons = [self.start_button, self.quit_button, self.shop_button]
        self.is_started = False
        self.music = pygame.mixer.Sound(path + '\\menu_data\\CB2077.mp3')
        self.car = Car()
        self.sprites = pygame.sprite.Group(self.car)

    def render(self):
        self.music.play()
        self.sprites.clear(screen, background)
        self.sprites.update()
        self.sprites.draw(screen)
        self.quit_button.render()
        self.start_button.render()
        self.shop_button.render()
        '''self.render_text()'''

    def check_mouse_motion(self, pos):
        for i in self.buttons:
            i.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for i in self.buttons:
            i.check_mouse_down(pos)

    def check_mouse_up(self):
        for i in self.buttons:
            i.check_mouse_up()

    def start_game(self):
        self.is_started = True
        self.music.stop()

    def quit(self):
        exit()

    def shop(self):
        pass

    '''def render_text(self):
        font = pygame.font.SysFont('Montserrat', 55)
        text_object_1 = font.render(
            f'Ваши монеты: {self.coins}', True, (255, 255, 255))
        text_object_2 = font.render(
            f'Машин у вас: {self.cars}', True, (255, 255, 255))
        screen.blit(text_object_1, (100, 400))
        screen.blit(text_object_2, (100, 500))'''# в магазине сделаем

    def game_over(self):
        if p.check():
            font = pygame.font.SysFont('Montserrat', 100)
            a = font.render(f'GAME OVER', True, (255, 0, 0))
            screen.blit(a, (200, 300))


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    background = pygame.Surface(screen.get_size())
    screen.blit(background, (0, 0))
    all_sprites = pygame.sprite.Group()
    p = Player(all_sprites)
    main_menu = Menu(str(sys.argv[1]))
    running = True
    fps = 60
    bg_img = pygame.image.load('\\'.join(os.getcwd().split(
        '\\')[:-1]) + '\\menu_and_game\\game_data\\road.jpg')
    bg_img = pygame.transform.scale(bg_img, (800, 800))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if not main_menu.is_started:
                    main_menu.check_mouse_motion(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not main_menu.is_started:
                    main_menu.check_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if not main_menu.is_started:
                    main_menu.check_mouse_up()
        if not main_menu.is_started:
            main_menu.render()
        else:
            screen.blit(bg_img, (0, 0))
            all_sprites.update(event)
            all_sprites.draw(screen)
            main_menu.game_over()

        pygame.display.flip()
        clock.tick(fps)
