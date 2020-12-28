import sys
import pygame
import random
from player import Player
from shop import Shop
from road import Road
from menu import Menu
from coin import Coin
from nitro import Nitro

x_place = [94, 281, 500, 700]

def chance(need):
    if random.randint(0,100) == need:
        return True
    return False

def generate_coin():
    if chance(15):
        return random.choice(x_place), random.randrange(50, 400)
    else:
        pass


def generate_nitro():
    if  chance(4):
        return random.choice(x_place), random.randrange(50, 400)
    else:
        pass


def generate_car():
    if random.randint(1, 100) == 1:
        if x_place.index(random.choice(x_place)) == 0 or x_place.index(random.choice(x_place)) == 1:
            print('perevorot')
        if x_place.index(random.choice(x_place)) == 2 or x_place.index(random.choice(x_place)) == 3:
            print('neperevorot')
    else:
        pass


if __name__ == '__main__':
    fps = 60
    running = True
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 800
    coin_sprites = pygame.sprite.Group()
    nitro_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    background = pygame.Surface(screen.get_size())
    all_sprites = pygame.sprite.Group()
    road = Road(screen)
    main_menu = Menu(screen, background, all_sprites, road, str(sys.argv[1]))
    shop = Shop(screen, main_menu.login)
    main_player = Player(all_sprites, coin_sprites)
    screen.blit(background, (0, 0))
    while running:
        coord = generate_coin()
        coord_nitro = generate_nitro()
        if coord:
            c = Coin(coin_sprites, coord[0], coord[1])
            all_sprites.add(coin_sprites)
        if coord_nitro:
            nitro = Nitro(nitro_sprites,road, coord_nitro[0], coord_nitro[1])
            all_sprites.add(nitro_sprites)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if main_menu.game_over:
                    if event.key == pygame.K_ESCAPE:
                        main_menu.is_started = False
                        main_player.respawner = True
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
            road.move()
            all_sprites.update(event)
            all_sprites.draw(screen)
            main_menu.check_game_over(main_player, shop)

        if shop.quit(event):
            main_menu.is_shopped = False
        pygame.display.flip()
        clock.tick(fps)
