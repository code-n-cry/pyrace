import sys
import os
import pygame
from player import Player
from shop import Shop
from road import Road
from menu import Menu
from game import Game
from garage import Garage
from roads import choose_roads
from road_select import Road_select
from setting import Settings

if __name__ == '__main__':
    """Файл для запуска всей игры(меню, короче все файлы)"""

    fps = 60
    path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\game_data\\'
    running = True
    pygame.init()
    event = 0
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    background = pygame.Surface(screen.get_size())
    player_sprites = pygame.sprite.Group()
    nitro_sprites = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()
    npc_sprites = pygame.sprite.Group()
    road = Road(screen, path + f'{choose_roads()}.png')
    main_player = Player(player_sprites)
    main_menu = Menu(screen, background, road, main_player, str(sys.argv[1]))
    settings = Settings(screen, main_menu, main_menu.login)
    garage = Garage(screen, main_menu, main_menu.login)
    road_select = Road_select(screen, main_menu, main_menu.login)
    change_road = False
    shop = Shop(screen, main_menu.login, garage)
    screen.blit(background, (0, 0))
    game = Game(main_player, coin_sprites, nitro_sprites, npc_sprites, player_sprites,
                road, screen, str(sys.argv[1]))
    main_menu.set_game_class(game)
    moving_event = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and main_menu.game_over:
                    main_menu.is_started = False
                    main_menu.game_over = False
                    main_player.respawn()
                if event.key != pygame.K_ESCAPE and main_menu.game_over:
                    main_menu.game_over_text()
                if main_menu.is_started:
                    moving_event = event
            if event.type == pygame.KEYUP:
                moving_event = event
            if event.type == pygame.MOUSEMOTION:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage and not main_menu.in_settings:
                    main_menu.check_mouse_motion(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_motion(event.pos)
                if main_menu.in_garage:
                    garage.check_mouse_motion(event.pos)
                if main_menu.in_roads:
                    road_select.check_mouse_motion(event.pos)
                if main_menu.in_settings:
                    settings.check_mouse_motion(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage and not main_menu.in_settings:
                    main_menu.check_mouse_down(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_down(event.pos)
                if main_menu.in_garage:
                    garage.check_mouse_down(event.pos)
                if main_menu.in_roads:
                    road_select.check_mouse_down(event.pos)
                if main_menu.in_settings:
                    settings.check_mouse_down(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage and not main_menu.in_settings:
                    main_menu.check_mouse_up()
                if main_menu.is_shopped:
                    shop.check_mouse_up()
                if main_menu.in_garage:
                    garage.check_mouse_up()
                if main_menu.in_roads:
                    road_select.check_mouse_up()
                if main_menu.in_settings:
                    settings.check_mouse_up()
        if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage and not main_menu.in_roads:
            main_menu.render()
            if change_road:
                game.road.image = pygame.transform.scale(
                    pygame.image.load(path + f'{choose_roads()}.png'), (800, 800))
                change_road = False
        if main_menu.is_shopped and not main_menu.is_started and not main_menu.in_garage and not main_menu.in_roads and not main_menu.in_settings:
            screen.fill('#c0c0c0')
            shop.render()
        if not main_menu.is_shopped and not main_menu.is_started and main_menu.in_garage and not main_menu.in_roads and not main_menu.in_settings:
            screen.fill('#c0c0c0')
            garage.render()
        if not main_menu.is_shopped and not main_menu.is_started and not main_menu.in_garage and main_menu.in_roads and not main_menu.in_settings:
            screen.fill('#c0c0c0')
            road_select.render()
            if road_select.choosen_road != 0:
                road.image = road_select.choosen_road
                change_road = False
        if not main_menu.is_shopped and not main_menu.is_started and not main_menu.in_garage and not main_menu.in_roads and main_menu.in_settings:
            screen.fill('#c0c0c0')
            settings.render()
            main_menu.music.set_volume(settings.choosen_m_volume / 100)
            game.music_defeat.set_volume(settings.choosen_s_volume / 100)
            game.music_coin.set_volume(settings.choosen_s_volume / 100)
            game.music_nitro.set_volume(settings.choosen_s_volume / 100)
        if main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage and not main_menu.in_settings:
            game.spawn()
            game.render(event)
            game.road.speed = 5
            if moving_event:
                player_sprites.update(moving_event)
            if main_menu.check_game_over(main_player, shop):
                if road_select.choosen_road == 0:
                    change_road = True
        if shop.quit(event):
            main_menu.is_shopped = False
        if garage.quit(event):
            main_menu.in_garage = False
        if road_select.quit(event):
            main_menu.in_roads = False
        if settings.quit(event):
            main_menu.in_settings = False
        pygame.display.flip()
        clock.tick(fps)
