class Game:
    def __init__(self, player, coin_group, nitro_group, enemy_group, player_group, road, surface):
        self.screen = surface
        self.player = player
        self.player_group = player_group
        self.coin_group = coin_group
        self.nitro_group = nitro_group
        self.enemy_group = enemy_group
        self.road = road

    def render(self, event):
        self.player_group.update(event)
        self.coin_group.update(event)
        self.nitro_group.update(event)
        #self.enemy_group.update()
        self.road.move()
        self.coin_group.draw(self.screen)
        self.nitro_group.draw(self.screen)
        #self.enemy_group.draw(self.screen)
        self.player_group.draw(self.screen)

    def spawn(self):
        field = [[], [], [], []]
