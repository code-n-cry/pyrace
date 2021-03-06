import random
import os
import time
import pygame
import pygame.freetype
from coin import Coin
from nitro import Nitro
from npc import Npc
from record import Record


class Game:
    """Класс, отвечающий за все процессы, происходящие во время игры. Обрабатывает пересечения
    объектов, отвечает за их спавн, а также за рендер на экране"""

    def __init__(self, player, coin_group, nitro_group, enemy_group, player_group, road, surface,
                 login):
        self.ticks = 0
        self.speed = 5
        self.bg_time = time.time()
        self.screen = surface
        self.player = player
        self.player_group = player_group
        self.coin_group = coin_group
        self.nitro_group = nitro_group
        self.enemy_group = enemy_group
        self.player_mask = pygame.mask.from_surface(player.image)
        self.road = road
        self.login = login
        self.record = Record()
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.music_defeat = pygame.mixer.Sound(self.path + '\\game_data\\defeat.ogg')
        self.music_coin = pygame.mixer.Sound(self.path + '\\game_data\\coin.ogg')
        self.music_nitro = pygame.mixer.Sound(self.path + '\\game_data\\nitro.ogg')
        self.x_places = [94, 281, 500, 700]
        self.nitro_time = []
        self.do_timer = True
        self.is_nitro = False
        self.do_spawn = True

    def render(self, event):
        self.ticks = pygame.time.get_ticks()
        self.coin_group.update(event)
        self.nitro_group.update(event)
        self.enemy_group.update(event)
        self.road.move(self.speed)
        self.coin_group.draw(self.screen)
        self.nitro_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        pygame.sprite.groupcollide(self.coin_group, self.enemy_group, True, False)
        pygame.sprite.groupcollide(self.nitro_group, self.enemy_group, True, False)
        if pygame.sprite.spritecollide(self.player, self.coin_group, True,
                                       pygame.sprite.collide_mask):
            self.player.got_coins += 1
            self.music_coin.play()
        if pygame.sprite.spritecollide(self.player, self.nitro_group, True,
                                       pygame.sprite.collide_mask):
            self.nitro()
            self.music_nitro.play()
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False,
                                       pygame.sprite.collide_mask):
            self.player.crashed = True
            self.record.add_record(round(time.time() - self.bg_time, 2), self.login,
                                   self.music_defeat)
            self.stop()  # При столкновении с врагом записываем в БД время поездки, останавливаем
            # игру.
        if self.player.rect.x <= 0 or self.player.rect.x >= 700:
            self.player.crashed = True
            self.record.add_record(round(time.time() - self.bg_time, 2), self.login,
                                   self.music_defeat)
            self.stop()
        self.check_nitro()
        self.timer(self.do_timer)

    def timer(self, do):
        """Функция для отображения времени поездки"""
        if do:
            font = pygame.freetype.SysFont(None, 34)
            font.origin = True
            out = str(round(time.time() - self.bg_time, 2))
            font.render_to(self.screen, (700, 760), out, pygame.Color('dodgerblue'))

    def spawn(self):
        if self.do_spawn:
            preliminarily_group_coins = pygame.sprite.Group()
            preliminarily_group_nitro = pygame.sprite.Group()
            preliminarily_group_npc = pygame.sprite.Group()
            if self.chance(15):
                coin = Coin(preliminarily_group_coins, random.choice(
                    self.x_places), random.randrange(50, 350), self.road)
                if self.check(coin):
                    self.coin_group.add(coin)
            if self.chance(3):
                nitro = Nitro(preliminarily_group_nitro, self.road, random.choice(
                    self.x_places), random.randrange(50, 350))
                if self.check(nitro):
                    self.nitro_group.add(nitro)
            if self.chance(30):
                x = random.choice(self.x_places)
                if self.x_places[0] <= x <= self.x_places[1]:
                    x -= random.randrange(60, 90)
                    y = random.randrange(-150, -110)
                    npc = Npc(preliminarily_group_npc, x, y, True)
                else:
                    x -= random.randrange(60, 90)
                    y = random.randrange(890, 990)
                    npc = Npc(preliminarily_group_npc, x, y, False)
                if self.check(npc):
                    self.enemy_group.add(npc)
            if self.player.bg_time == 0:
                self.bg_time = time.time()
                self.player.bg_time = 1

    def chance(self, need):
        if random.randint(0, 100) == need:
            return True
        return False

    def check(self, sprite):
        if not pygame.sprite.spritecollide(sprite, self.coin_group, False) and not \
                pygame.sprite.spritecollide(sprite, self.nitro_group, False) and not \
                pygame.sprite.spritecollide(sprite, self.enemy_group, False):
            return True
        return False

    def nitro(self):
        """Ускорение(нитро - окись азота, использующаяся для увелечения характеристик двигателя)"""
        for coin in self.coin_group:
            coin.vy += 10
        for nitro in self.nitro_group:
            nitro.speed += 10
        self.speed += 10
        self.road.speed += 10
        self.nitro_time.append(time.time())

    def check_nitro(self):
        if self.nitro_time:
            if time.time() - self.nitro_time[-1] >= 3:
                for coin in self.coin_group:
                    coin.vy -= 10
                for nitro in self.nitro_group:
                    nitro.speed -= 10
                self.speed -= 10
                self.road.speed -= 10
                self.nitro_time.clear()

    def unstop(self):
        for car in self.enemy_group:
            if car.rect.x < 200:
                car.vy = 12
            else:
                car.vy = -7
        for coin in self.coin_group:
            coin.vy = 5
        for nitro in self.nitro_group:
            nitro.speed = 5
        self.speed = 5
        self.do_spawn = True
        self.do_timer = True
        self.player.can_move = True

    def stop(self):
        for car in self.enemy_group:
            car.vy = 0
        for coin in self.coin_group:
            coin.vy = 0
        for nitro in self.nitro_group:
            nitro.speed = 0
        self.speed = 0
        self.do_spawn = False
        self.do_timer = False
        self.player.can_move = False
        self.nitro_time.clear()
        self.bg_time = time.time()

    def restart(self):
        self.record.col = 2
        self.record.col -= 1
        self.do_spawn = True
        self.do_timer = True
        self.player.can_move = True
        self.coin_group.empty()
        self.nitro_group.empty()
        self.enemy_group.empty()
        self.speed = 5
