import sys
import pygame
import random
from player import Player
from shop import Shop
from road import Road
from menu import Menu
from coin import Coin
from game import Game
from nitro import Nitro

if __name__ == '__main__':
    fps = 60
    running = True
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 800
    coin_sprites = pygame.sprite.Group()
    for i in range(5):
        c = Coin(coin_sprites, random.randrange(50, 750), random.randrange(50, 530))

    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    background = pygame.Surface(screen.get_size())
    all_sprites = pygame.sprite.Group()
    nitro_sprites = pygame.sprite.Group()
    road = Road(screen)
    main_menu = Menu(screen, background, all_sprites, road, str(sys.argv[1]))
    shop = Shop(screen, main_menu.login)
    main_player = Player(all_sprites, coin_sprites)
    for i in range(5):
        n = Nitro(nitro_sprites, road, random.randrange(50, 750), random.randrange(50, 530))
    screen.blit(background, (0, 0))
    game = Game(main_player, coin_sprites, nitro_sprites, False, all_sprites, road, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and main_menu.game_over:
                    main_menu.is_started = False
                    main_player.respawn()
            if event.type == pygame.MOUSEMOTION:
                if not main_menu.is_started and not main_menu.is_shopped:
                    main_menu.check_mouse_motion(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_motion(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not main_menu.is_started and not main_menu.is_shopped:
                    main_menu.check_mouse_down(event.pos)
                if main_menu.is_shopped:
                    shop.check_mouse_down(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if not main_menu.is_started and not main_menu.is_shopped:
                    main_menu.check_mouse_up()
                if main_menu.is_shopped:
                    shop.check_mouse_up()
        if not main_menu.is_started and not main_menu.is_shopped:
            main_menu.render()
        if main_menu.is_shopped and not main_menu.is_started:
            screen.fill('#c0c0c0')
            shop.render()
        if main_menu.is_started and not main_menu.is_shopped:
            game.render(event)
            main_menu.check_game_over(main_player, shop)
        if shop.quit(event):
            main_menu.is_shopped = False
        pygame.display.flip()
        clock.tick(fps)
