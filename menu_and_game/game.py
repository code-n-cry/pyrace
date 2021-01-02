import random
from coin import Coin
from nitro import Nitro
import time
import pygame
from npc import Npc


class Game:
    def __init__(self, player, coin_group, nitro_group, enemy_group, player_group, road,
                 surface):
        self.screen = surface
        self.player = player
        self.player_group = player_group
        self.coin_group = coin_group
        self.nitro_group = nitro_group
        self.enemy_group = enemy_group
        self.road = road
        self.speed = 5
        self.x_places = [94, 281, 500, 700]
        self.is_nitro = False
        self.do_spawn = True
        self.nitro_time = []

    def render(self, event):
        # self.enemy_group.update()
        # self.enemy_group.draw(self.screen)
        self.player_group.update(event)
        self.coin_group.update(event)
        self.nitro_group.update(event)
        self.enemy_group.update(event)
        self.road.move(self.speed)
        self.coin_group.draw(self.screen)
        self.nitro_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        if pygame.sprite.spritecollide(self.player, self.coin_group, True):
            self.player.got_coins += 1
        if pygame.sprite.spritecollide(self.player, self.nitro_group, True):
            self.nitro()
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            self.player.crashed = True
            self.stop()
        self.check_nitro()

    def spawn(self):
        if self.do_spawn:
            predv_group_coins = pygame.sprite.Group()
            predv_group_nitro = pygame.sprite.Group()
            predv_group_npc = pygame.sprite.Group()
            if self.chance(15):
                coin = Coin(predv_group_coins, random.choice(
                    self.x_places), random.randrange(50, 350), self.road)
                if self.check(coin):
                    self.coin_group.add(coin)
            if self.chance(3):
                nitro = Nitro(predv_group_nitro, self.road, random.choice(
                    self.x_places), random.randrange(50, 350))
                if self.check(nitro):
                    self.nitro_group.add(nitro)
            if self.chance(30):
                x = random.choice(self.x_places)
                if self.x_places[0] <= x <= self.x_places[1]:
                    x -= random.randrange(60, 90)
                    y = random.randrange(-150, -110)
                    npc = Npc(predv_group_npc, x, y, True)
                else:
                    x -= random.randrange(60, 90)
                    y = random.randrange(890, 990)
                    npc = Npc(predv_group_npc, x, y, False)
                if self.check(npc):
                    self.enemy_group.add(npc)

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

    def stop(self):
        for car in self.enemy_group:
            car.vy = 0
        for coin in self.coin_group:
            coin.vy = 0
        for nitro in self.nitro_group:
            nitro.speed = 0
        self.speed = 0
        self.do_spawn = False
        self.nitro_time.clear()

    def restart(self):
        self.do_spawn = True
        self.coin_group.empty()
        self.nitro_group.empty()
        self.enemy_group.empty()
        self.speed = 5