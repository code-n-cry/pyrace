import random


def choose_roads():
    """Функция для случайного выбора дороги. Некоторые дороги выпадают с определённым шансом"""
    roads = ['road_v2', 'road_v3', 'ice_road', 'road']
    chosen_road = random.choice(roads)
    if random.randrange(0, 100) == 15:
        return 'psychodelic_road'
    if random.randrange(0, 100) == 1:
        return 'snow_road'
    return chosen_road
