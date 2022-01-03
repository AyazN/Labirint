# сделал Мухаметзянов Дамир

from settings import *
from random import *
from function_sql import *
from enum import Enum

level_map = []


class MapEntryType(Enum):
    MAP_EMPTY = 0,
    MAP_BLOCK = 1,


class WallDirection(Enum):
    WALL_LEFT = 0,
    WALL_UP = 1,
    WALL_RIGHT = 2,
    WALL_DOWN = 3,


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def set_map(self, x, y, value):
        if value == MapEntryType.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MapEntryType.MAP_BLOCK:
            self.map[y][x] = 1

    def is_movable(self, x, y):
        return self.map[y][x] != 1

    def is_valid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def show_map(self):
        total = 0
        for row in self.map:
            s = ''
            for entry in row:
                if total == 26:
                    s += '@'
                elif total == 398:
                    s += 'X'
                elif total == 373:
                    s += 'F'
                elif total == 397:
                    s += 'G'
                elif total == 29:
                    s += 'F'
                elif total == 77:
                    s += 'F'
                elif total == 48:
                    s += 'N'
                elif entry == 0:
                    s += '.'
                elif entry == 1:
                    s += 'T'
                else:
                    s += '.'
                total += 1
            level_map.append(s)


def recursive_division(map, x, y, width, height, wall_value):
    def get_wall_index(start, length):
        assert length >= 3
        wall_index = randint(start + 1, start + length - 2)
        if wall_index % 2 == 1:
            wall_index -= 1
        return wall_index

    def generate_holes(map, x, y, width, height, wall_x, wall_y):
        holes = []

        hole_entrys = [(randint(x, wall_x - 1), wall_y), (randint(wall_x + 1, x + width - 1), wall_y),
                       (wall_x, randint(y, wall_y - 1)), (wall_x, randint(wall_y + 1, y + height - 1))]
        margin_entrys = [(x, wall_y), (x + width - 1, wall_y), (wall_x, y), (wall_x, y + height - 1)]
        adjacent_entrys = [(x - 1, wall_y), (x + width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
        for i in range(4):
            adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
            if map.is_valid(adj_x, adj_y) and map.is_movable(adj_x, adj_y):
                map.set_map(margin_entrys[i][0], margin_entrys[i][1], MapEntryType.MAP_EMPTY)
            else:
                holes.append(hole_entrys[i])

        ignore_hole = randint(0, len(holes) - 1)
        for i in range(0, len(holes)):
            if i != ignore_hole:
                map.set_map(holes[i][0], holes[i][1], MapEntryType.MAP_EMPTY)

    if width <= 1 or height <= 1:
        return

    wall_x, wall_y = (get_wall_index(x, width), get_wall_index(y, height))

    for i in range(x, x + width):
        map.set_map(i, wall_y, wall_value)
    for i in range(y, y + height):
        map.set_map(wall_x, i, wall_value)

    generate_holes(map, x, y, width, height, wall_x, wall_y)

    recursive_division(map, x, y, wall_x - x, wall_y - y, wall_value)
    recursive_division(map, x, wall_y + 1, wall_x - x, y + height - wall_y - 1, wall_value)
    recursive_division(map, wall_x + 1, y, x + width - wall_x - 1, wall_y - y, wall_value)
    recursive_division(map, wall_x + 1, wall_y + 1, x + width - wall_x - 1, y + height - wall_y - 1, wall_value)


def do_recursive_division(map):
    for x in range(0, map.width):
        map.set_map(x, 0, MapEntryType.MAP_BLOCK)
        map.set_map(x, map.height - 1, MapEntryType.MAP_BLOCK)

    for y in range(0, map.height):
        map.set_map(0, y, MapEntryType.MAP_BLOCK)
        map.set_map(map.width - 1, y, MapEntryType.MAP_BLOCK)

    recursive_division(map, 1, 1, map.width - 2, map.height - 2, MapEntryType.MAP_BLOCK)


def run():
    width = WIDTH // TILE if (WIDTH // TILE) % 2 != 0 else WIDTH // TILE + 1
    height = HEIGHT // TILE if (HEIGHT // TILE) % 2 != 0 else HEIGHT // TILE + 1
    map = Map(width, height)
    do_recursive_division(map)
    map.show_map()
    with open('data/map.txt', "a") as file:
        file.truncate(0)
        for message in level_map:
            file.write(message)
            file.write('\n')
    add_file_name(open_map())
    return level_map
