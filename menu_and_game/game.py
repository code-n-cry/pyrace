import random
from coin import Coin
from nitro import Nitro
import pygame


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

    def render(self, event):
        # self.enemy_group.update()
        # self.enemy_group.draw(self.screen)
        self.player_group.update(event)
        self.coin_group.update(event)
        self.nitro_group.update(event)
        self.road.move()
        self.coin_group.draw(self.screen)
        self.nitro_group.draw(self.screen)
        self.player_group.draw(self.screen)
        if pygame.sprite.spritecollide(self.player, self.coin_group, True):
            self.player.got_coins += 1
        if pygame.sprite.spritecollide(self.player, self.nitro_group, True):
            pass

    def spawn(self):
        if self.chance(15):
            return Coin(self.coin_group, random.choice(self.x_places), random.randrange(50, 350), self.road)
        if self.chance(10):
            return Nitro(self.nitro_group, self.road, random.choice(self.x_places), random.randrange(50, 350))

    def chance(self, need):
        if random.randint(0, 100) == need:
            return True
        return False

