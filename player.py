# сделал Мухаметзянов Дамир

import random
from settings import *
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
        if color_key == KEY:
            color_key = image.get_at(NULLS_CORDS)
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
    new_player, new_enemy, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'N':
                Tile('empty', x, y)
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == 'F':
                Tile('empty', x, y)
                Tile('frame', x, y)
                fires.append((x, y))
            elif level[y][x] == 'G':
                Tile('nulls', x, y)
                nulls.append([x, y])
            elif level[y][x] == 'T':
                Tile('wall', x, y)
                walls.append((x, y))
            elif level[y][x] == 'X':
                Tile('em', x, y)
                castle.append([x, y])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'N':
                new_enemy = Enemy(x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, new_enemy, x, y


def is_free(position):
    return position not in walls


def find_path_step(start, target):
    INF = ITERATION_TICK
    x, y = start
    distance = [[INF] * COLS for _ in range(ROWS)]
    distance[y][x] = ZERO
    prev = [[None] * COLS for _ in range(ROWS)]
    queue = [(x, y)]
    while queue:
        x, y = queue.pop(ZERO)
        for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
            next_x, next_y = x + dx, y + dy
            if ZERO <= next_x < COLS and ZERO <= next_y < ROWS and \
                    is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                distance[next_y][next_x] = distance[y][x] + ONE_ITERATION
                prev[next_y][next_x] = (x, y)
                queue.append((next_x, next_y))
    x, y = target
    if distance[y][x] == ZERO:
        return start
    while prev[y][x] != start:
        x, y = prev[y][x]
    return x, y


tile_images = {
    'wall': load_image('wall_box.png'),
    'empty': load_image('ground.png'),
    'em': load_image('door.png'),
    'enemy': load_image('enemy.png'),
    'frame': load_image('frame.png'),
    'fire': load_image('fire.png'),
    'nulls': load_image('mini.png')
}
player_image = load_image('king.png')
enemy_image = load_image('enemy.png')

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls, fires, nulls, castle = [], [], [], []

tile_width = tile_height = TILE
cords = ALL_CORDS_MOVE


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
            tile_width * pos_x + RECT_PLAYER_WIDTH, tile_height * pos_y + RECT_PLAYER_HEIGHT)

    def player_move(self, x, y):
        if (self.pos_x + x, self.pos_y + y) not in walls \
                and -ONE < self.pos_x + x < CELL_WIDTH and -ONE < self.pos_y + y < CELL_HEIGHT:
            self.pos_x += x
            self.pos_y += y
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + RECT_PLAYER_WIDTH, tile_height * self.pos_y + RECT_PLAYER_HEIGHT)

    def get_pos(self):
        return [self.pos_x, self.pos_y]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = enemy_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.start_pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + RECT_PLAYER_WIDTH, tile_height * pos_y + RECT_PLAYER_HEIGHT)

    def enemy_move(self, player_pos, flag):
        x, y = find_path_step((self.pos_x, self.pos_y), Player.get_pos(player_pos))
        if not flag:
            self.pos_x = x
            self.pos_y = y
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + RECT_PLAYER_WIDTH, tile_height * self.pos_y + RECT_PLAYER_HEIGHT)

    def collision_check(self, player_pos):
        return Player.get_pos(player_pos) == [self.pos_x, self.pos_y]

    def collision_check_with_fire(self, player_pos):
        x, y = Player.get_pos(player_pos)
        return (x, y) in fires

    def get_pos(self):
        return [[self.pos_x, self.pos_y], [self.pos_x + ONE, self.pos_y], [self.pos_x, self.pos_y + ONE],
                [self.pos_x - ONE, self.pos_y], [self.pos_x, self.pos_y - ONE]]

    def start_pos_rt(self):
        return self.start_pos
