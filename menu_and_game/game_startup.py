import sys
import pygame
from player import Player
from shop import Shop
from road import Road
from menu import Menu

if __name__ == '__main__':
    fps = 60
    running = True
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    background = pygame.Surface(screen.get_size())
    all_sprites = pygame.sprite.Group()
    main_menu = Menu(screen, background, str(sys.argv[1]))
    shop = Shop(screen, main_menu.login)
    road = Road(screen)
    main_player = Player(all_sprites)
    screen.blit(background, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            if not main_menu.game_over(main_player):
                road.move(5)
                all_sprites.update(event)
                all_sprites.draw(screen)
            else:
                road.move(0)
                all_sprites.draw(screen)
                main_menu.game_over(main_player)
        if shop.quit(event):
            main_menu.is_shopped = False
        pygame.display.flip()
        clock.tick(fps)
