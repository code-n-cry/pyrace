import random
from coin import Coin
from nitro import Nitro
import time
import pygame
from npc import Npc


class Game:
    def __init__(self, player, coin_group, nitro_group, enemy_group, player_group, road, surface):
        self.screen = surface
        self.player = player
        self.player_group = player_group
        self.coin_group = coin_group
        self.nitro_group = nitro_group
        self.enemy_group = enemy_group
        self.road = road
        self.x_places = [94, 281, 500, 700]
        self.is_nitro = False

    def render(self, event):
        # self.enemy_group.update()
        # self.enemy_group.draw(self.screen)
        self.player_group.update(event)
        self.coin_group.update(event)
        self.nitro_group.update(event)
        self.enemy_group.update(event)
        self.road.move()
        self.coin_group.draw(self.screen)
        self.nitro_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        if pygame.sprite.spritecollide(self.player, self.coin_group, True):
            self.player.got_coins += 1
        if pygame.sprite.spritecollide(self.player, self.nitro_group, True):
            self.nitro()

    def spawn(self):
        predv_group_coins = pygame.sprite.Group()
        predv_group_nitro = pygame.sprite.Group()
        predv_group_npc = pygame.sprite.Group()
        if self.chance(15):
            coin = Coin(predv_group_coins, random.choice(
                self.x_places), random.randrange(50, 350), self.road)
            if self.check(coin):
                self.coin_group.add(coin)
        if self.chance(10):
            nitro = Nitro(predv_group_nitro, self.road, random.choice(
                self.x_places), random.randrange(50, 350))
            if self.check(nitro):
                self.nitro_group.add(nitro)
        if self.chance(10):
            x = random.choice(self.x_places)
            y = random.randrange(50, 350)
            npc = ''
            if self.x_places[0] <= x <= self.x_places[1]:
                x -= 90
                npc = Npc(predv_group_npc, x, y, True)
            else:
                x -= 90
                npc = Npc(predv_group_npc, x, y, False)
            if self.check(npc):
                self.enemy_group.add(npc)

    def chance(self, need):
        if random.randint(0, 100) == need:
            return True
        return False

    def check(self, sprite):
        if not pygame.sprite.spritecollide(sprite, self.coin_group, False) and not\
                pygame.sprite.spritecollide(sprite, self.nitro_group, False) and not\
                pygame.sprite.spritecollide(sprite, self.enemy_group, False):
            return True
        return False

    def nitro(self):
        self.is_nitro = True
