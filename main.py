import pygame
import random
from settings import *
from gen_map import run
from player import *
from map import Cell


name = ['level', 'level_1', 'level_2']
pygame.init()
screen = pygame.display.set_mode(RES)
run()
player, level_x, level_y = generate_level(load_level(random.choice(name)))
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.player_move(-1, 0)
            if event.key == pygame.K_RIGHT:
                player.player_move(1, 0)
            if event.key == pygame.K_UP:
                player.player_move(0, -1)
            if event.key == pygame.K_DOWN:
                player.player_move(0, 1)

    screen.fill('Grey')
    # board.render(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
