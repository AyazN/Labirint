# Фазульзянов Амир
# 02.01 сделана мини-игра крестики-нолики

import pygame

WIDTH = 1200
HEIGHT = 800
BLACK = 0
BLUE = 1
RED = 2
COLORS = ['Black', 'Blue', 'Red']


class NoughtsCrosses:
    def __init__(self, width, height, left=300, top=100, cell_size=200):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.set_view(left, top, cell_size)
        self.move = BLUE

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        ots = 2
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'White', (self.left + col * self.cell_size,
                                 self.top + row * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board[row][col] == BLUE:
                    pygame.draw.line(screen, COLORS[self.board[row][col]],
                                     (col * self.cell_size + 2 * ots + self.left, row * self.cell_size + ots + self.top),
                                     ((col + 1) * self.cell_size - 2 * ots + self.left,
                                     (row + 1) * self.cell_size - 2 * ots + self.top), width=7)
                    pygame.draw.line(screen, COLORS[self.board[row][col]],
                                     ((col + 1) * self.cell_size - 2 * ots + self.left,
                                     row * self.cell_size + ots + self.top),
                                     (col * self.cell_size + 2 * ots + self.left,
                                     (row + 1) * self.cell_size - 2 * ots + self.top), width=7)
                if self.board[row][col] == RED:
                    pygame.draw.circle(screen, COLORS[self.board[row][col]],
                                       ((col + 0.5) * self.cell_size + self.left,
                                       (row + 0.5) * self.cell_size + self.top),
                                       self.cell_size / 2 - ots, width=7)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        if 0 <= pos[0] - self.left < self.width * self.cell_size and \
                0 <= pos[1] - self.top < self.height * self.cell_size:
            return (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
        return None

    def on_click(self, cell):
        if cell:
            col, row = cell[0], cell[1]
            if self.board[row][col] == BLACK and self.move == BLUE:
                self.board[row][col] = BLUE
                self.move = RED
            elif self.board[row][col] == BLACK and self.move == RED:
                self.board[row][col] = RED
                self.move = BLUE


def main_noughts_crosses():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Крестики-нолики')
    board = NoughtsCrosses(3, 3)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()


main_noughts_crosses()