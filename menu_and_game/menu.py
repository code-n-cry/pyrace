import random
import pygame
import os
import sqlite3
from animated_background import Car
from button import Button


class Menu:
    def __init__(self, screen, background, road, player, user_login):
        width, height = screen.get_size()
        path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game'
        self.con = sqlite3.connect(path + '\\game_data/users_info.db')
        cur = self.con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS info(login, data)')
        self.con.commit()
        self.cars = 1
        self.login = user_login
        self.game = None
        self.player = player
        logins = [i[0] for i in cur.execute('SELECT login FROM info').fetchall()]
        if user_login not in logins:
            cur.execute('INSERT INTO info VALUES(?, ?)', (user_login, '#0000_1_0_0_0_0_0_0_0_0_1'))
            self.con.commit()
        self.start_button = Button(10, 10, 132, 50, 'Играть', screen, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 55,
                                   self.start_game)
        self.quit_button = Button(width - 142, 10, 132, 45, 'Выход', screen, (66, 245, 206),
                                  (0, 0, 0), (227, 66, 245), 0, 50, self.quit)
        self.shop_button = Button(10, 70, 132, 45, 'Магазин', screen, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0, 46,
                                  self.shop)
        self.garage_button = Button(10, 130, 173, 45, 'Ваш гараж', screen, (66, 245, 206), (0, 0, 0), (227, 66, 245), 0,
                                    46, self.garage)
        # self.garage_buttom = Button()
        self.buttons = [self.start_button, self.quit_button, self.shop_button, self.garage_button]
        self.is_started = False
        self.is_shopped = False
        self.in_garage = False
        self.game_over = False
        self.choosen_car = int(
            cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0].split('_')[-1])
        melodies = [path + '\\menu_data\\CB2077.mp3', path + '\\menu_data\\menu_music.wav']
        self.music = pygame.mixer.Sound(random.choice(melodies))
        self.car = Car(width, height)
        self.sprites = pygame.sprite.Group(self.car)
        self.screen = screen
        self.background = background
        self.road = road

    def render(self):
        # self.music.play()
        self.sprites.clear(self.screen, self.background)
        self.sprites.update()
        self.sprites.draw(self.screen)
        for btn in self.buttons:
            btn.render()

    def check_mouse_motion(self, pos):
        for btn in self.buttons:
            btn.check_mouse_motion(pos)

    def check_mouse_down(self, pos):
        for btn in self.buttons:
            btn.check_mouse_down(pos)

    def check_mouse_up(self):
        for btn in self.buttons:
            btn.check_mouse_up()

    def start_game(self):
        self.player.update_image(self.choosen_car)
        self.is_started = True
        self.music.stop()
        self.game.restart()
        self.game.unstop()

    def quit(self):
        exit()

    def shop(self):
        self.is_shopped = True
        self.music.stop()

    def garage(self):
        self.in_garage = True
        self.music.stop()

    def check_game_over(self, player, shop):
        if player.check() or player.crashed:
            cur = self.con.cursor()
            data_str = cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0]
            coins = data_str[1:].split('_')[0]
            old_coins = int(coins)
            coins = '0' * len(str(1000 - player.got_coins + old_coins)) + str(player.got_coins + old_coins)
            data_str = '#' + coins + '_' + '_'.join(data_str[1:].split('_')[1:])
            cur.execute('UPDATE info SET data=? WHERE login=?', (data_str, self.login))
            self.con.commit()
            cur.close()
            player.got_coins = 0
            self.player.bg_time = 0
            self.game_over = True
            player.crashed = False
            self.game_over_text()
            shop.update_coins()
            return True

    def game_over_text(self):
        font = pygame.font.SysFont('Montserrat', 100)
        text = font.render(f'GAME OVER', True, (255, 0, 0))
        font2 = pygame.font.SysFont('Montserrat', 40)
        text2 = font2.render('Нажмите "ESC" для перехода в главное меню', True, (255, 0, 0))
        self.screen.blit(text, (200, 300))
        self.screen.blit(text2, (83, 500))

    def set_game_class(self, game):
        self.game = game
