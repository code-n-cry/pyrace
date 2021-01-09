import random
import pygame
import os
import sqlite3
from animated_background import Car
from record import Record
from button import Button
from roads import choose_roads


class Menu:
    def __init__(self, screen, background, road, player, user_login):
        width, height = screen.get_size()
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.con = sqlite3.connect(self.path + 'game_data\\users_info.db')
        cur = self.con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS info(login, data)')
        logins = [i[0] for i in cur.execute('SELECT login FROM info').fetchall()]
        if user_login not in logins:
            cur.execute('INSERT INTO info VALUES(?, ?)',
                        (user_login, '#0000_1_0_0_0_0_0_0_0_0_1'))
        self.con.commit()

        self.cars = 1
        self.header = ''
        self.screen = screen
        self.background = background
        self.road = road
        self.login = user_login
        self.player = player
        self.car = Car(width, height)
        self.record = Record()
        self.start_button = Button(10, 10, 132, 50, 'Играть', screen, (66, 245, 206),
                                   (255, 204, 0), (227, 66, 245), 1, 55, self.start_game)
        self.quit_button = Button(width - 142, 10, 132, 45, 'Выход', screen, (66, 245, 206),
                                  (255, 204, 0), (227, 66, 245), 1, 50, self.quit)
        self.shop_button = Button(10, 70, 132, 45, 'Магазин', screen, (66, 245, 206),
                                  (255, 204, 0), (227, 66, 245), 1, 46, self.shop)
        self.garage_button = Button(10, 130, 173, 45, 'Ваш гараж', screen, (66, 245, 206),
                                    (255, 204, 0), (227, 66, 245), 1, 46, self.garage)
        self.buttons = [self.start_button, self.quit_button, self.shop_button,
                        self.garage_button]
        self.game = None
        self.is_started = False
        self.is_shopped = False
        self.in_garage = False
        self.game_over = False
        melodies = [self.path + 'menu_data\\menu_music.wav']
        self.music = pygame.mixer.Sound(random.choice(melodies))
        self.sprites = pygame.sprite.Group(self.car)
        self.chosen_car = int(
            cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0].split('_')[-1])

    def render(self):
        self.music.play()
        self.sprites.clear(self.screen, self.background)
        self.sprites.update()
        self.sprites.draw(self.screen)
        self.render_record()
        for btn in self.buttons:
            btn.render()

    def render_record(self):
        all_records = self.record.read_records()
        records = []
        for data in all_records:
            if data[2] == self.login:
                records.append(data)
        records.sort(key=lambda x: x[1])
        if len(records) < 5:
            self.header = 'Последние заезды:'
        elif len(records) == 0:
            self.header = 'Начни игру!'
        else:
            self.header = 'Топ-5 заездов:'
            records = records[::-1][:6]
        font = pygame.font.SysFont('Montserrat', 55)
        header = font.render(self.header, True, (255, 204, 0))
        self.screen.blit(header, (10, 400))
        if records:
            y_coord = 710
            font = pygame.font.SysFont('Montserrat', 40)
            for i in records:
                rec = font.render(f'{i[1]} сек.', True, (66, 245, 206))
                self.screen.blit(rec, (80, y_coord))
                y_coord -= 50

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
        image = pygame.image.load(self.path + f'game_data\\{choose_roads()}.jpg')
        self.road.image = pygame.transform.scale(image, (800, 800))
        self.player.update_image(self.chosen_car)
        self.is_started = True
        self.music.stop()
        self.game.restart()
        self.game.unstop()

    def quit(self):
        exit(1)

    def shop(self):
        self.is_shopped = True
        self.music.stop()

    def garage(self):
        self.in_garage = True
        self.music.stop()

    def check_game_over(self, player, shop):
        if player.check() or player.crashed:
            cur = self.con.cursor()
            data_str = \
                cur.execute('SELECT data FROM info WHERE login=?', (self.login,)).fetchone()[0]
            coins = data_str[1:].split('_')[0]
            old_coins = int(coins)
            coins = '0' * len(str(1000 - player.got_coins + old_coins)) + str(
                player.got_coins + old_coins)
            data_str = '#' + coins + '_' + '_'.join(data_str[1:].split('_')[1:])
            cur.execute('UPDATE info SET data=? WHERE login=?', (data_str, self.login))
            self.con.commit()
            cur.close()
            player.got_coins = 0
            self.game_over = True
            self.player.bg_time = 0
            player.crashed = False
            self.game_over_text()
            shop.update_coins()
            return True

    def game_over_text(self):
        font = pygame.font.SysFont('Montserrat', 100)
        text = font.render(f'GAME OVER', True, (255, 0, 0))
        font2 = pygame.font.SysFont('Montserrat', 40)
        text2 = font2.render('Нажмите "ESC" для перехода в главное меню', True,
                             (255, 0, 0))
        self.screen.blit(text, (200, 300))
        self.screen.blit(text2, (83, 500))

    def set_game_class(self, game):
        self.game = game
