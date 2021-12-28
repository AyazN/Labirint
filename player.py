import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
    return image


def load_level(filename):
    try:
        filename = "data/" + filename + '.txt'
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        print('This file does not exist.')
        sys.exit()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'N':
                continue
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                walls.append((x, y))
            elif level[y][x] == 'X':
                Tile('empty', x, y)
                Tile('em', x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'em': load_image('castle.jpg')
}
player_image = load_image('mario.png')

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls = []

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def player_move(self, x, y):
        if (self.pos_x + x, self.pos_y + y) not in walls \
                and -1 < self.pos_x + x < 24 and -1 < self.pos_y + y < 16:
            self.pos_x += x
            self.pos_y += y
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

