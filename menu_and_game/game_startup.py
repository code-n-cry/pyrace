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
    road = Road(screen, path + f'{choose_roads()}.jpg')
    main_player = Player(player_sprites)
    main_menu = Menu(screen, background, road, main_player, str(sys.argv[1]))
    garage = Garage(screen, main_menu, main_menu.login)
    shop = Shop(screen, main_menu.login, garage)
    screen.blit(background, (0, 0))
    game = Game(main_player, coin_sprites, nitro_sprites, npc_sprites, player_sprites,
                road, screen, str(sys.argv[1]))
    main_menu.set_game_class(game)
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
            if event.type == pygame.MOUSEMOTION:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage:
                    main_menu.check_mouse_motion(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_motion(event.pos)
                if main_menu.in_garage:
                    garage.check_mouse_motion(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage:
                    main_menu.check_mouse_down(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_down(event.pos)
                if main_menu.in_garage:
                    garage.check_mouse_down(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage:
                    main_menu.check_mouse_up()
                if main_menu.is_shopped:
                    shop.check_mouse_up()
                if main_menu.in_garage:
                    garage.check_mouse_up()
        if not main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage:
            main_menu.render()
        if main_menu.is_shopped and not main_menu.is_started and not main_menu.in_garage:
            screen.fill('#c0c0c0')
            shop.render()
        if not main_menu.is_shopped and not main_menu.is_started and main_menu.in_garage:
            screen.fill('#c0c0c0')
            garage.render()
        if main_menu.is_started and not main_menu.is_shopped and not main_menu.in_garage:
            game.spawn()
            game.render(event)
            game.road.speed = 5
            main_menu.check_game_over(main_player, shop)
        if shop.quit(event):
            main_menu.is_shopped = False
        if garage.quit(event):
            main_menu.in_garage = False
        pygame.display.flip()
        clock.tick(fps)
