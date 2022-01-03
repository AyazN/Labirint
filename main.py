import random
from function_sql import *
import pygame
from settings import *
from mini_game import main_noughts_crosses
from alternate_final import play_alt
from final import *
from player import *


def main_play(running, user_id):
    pygame.init()
    screen = pygame.display.set_mode(RES)
    player, enemy, level_x, level_y = generate_level(load_level('map'))
    my_font = pygame.font.SysFont('arial', 130)
    text_surface = my_font.render('YOU WIN', False, (255, 204, 0))
    text_surface_died = my_font.render('YOU DIED', False, (255, 0, 0))
    clock = pygame.time.Clock()
    num_exit = 0
    total = 0
    num = 0
    dead = False
    img_kill = False
    img_fire = False
    win = False
    killing = False

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
                if event.key == pygame.K_SPACE and player.get_pos() in enemy.get_pos():
                    enemy.image = load_image('kill.png')
                    img_kill = True
                    killing = True
        screen.fill('Grey')
        if num_exit % 100 == 0 and num_exit > 100:
            pygame.display.flip()
            running = False
            continue
        if player.get_pos() == nulls[0]:
            if not main_noughts_crosses():
                dead = True
                play_alt(True, user_id, num_exit, total, num, dead, img_kill, img_fire, win, killing, player.get_pos(),
                         enemy.get_pos()[0])
            else:
                play_alt(True, user_id, num_exit, total, num, dead, img_kill, img_fire, win, killing, player.get_pos(),
                         enemy.get_pos()[0])
            running = False
            continue
        if ((enemy.collision_check(player) and not img_kill) or
            (enemy.collision_check_with_fire(player) and img_fire)) and not dead:
            dead = True
            if enemy.collision_check(player) and not img_kill:
                add_new_save(user_id, player.get_pos()[0], player.get_pos()[1], enemy.start_pos_rt()[0],
                             enemy.start_pos_rt()[1],
                             select_map_id(open_map()))
            else:
                add_new_save(user_id, player.get_pos()[0], player.get_pos()[1], enemy.get_pos()[0][0],
                             enemy.get_pos()[0][1],
                             select_map_id(open_map()))
        if player.get_pos() == castle[0]:
            win = True
        if total % 25 == 0 and total > 25 and not win and not dead:
            enemy.enemy_move(player, killing)
        if total % 100 == 0 and total > 100 and not win and not dead:
            tile_images['frame'] = load_image('fire.png') if num % 2 == 0 else load_image('frame.png')
            img_fire = True if not img_fire else False
            for i in range(len(fires)):
                Tile('frame', fires[i][0], fires[i][1])
            num += 1
        if dead:
            screen.fill('Black')
            screen.blit(text_surface_died, (WIDTH // 4 + 50, HEIGHT // 3))
            num_exit += 1
        elif win:
            screen.fill('Black')
            screen.blit(text_surface, (WIDTH // 3, HEIGHT // 3))
            create_particles((random.randint(1, WIDTH), random.randint(1, HEIGHT)))
            all_sprites_new.draw(screen)
            all_sprites_new.update()
            num_exit += 1
        else:
            all_sprites.draw(screen)
            all_sprites.update()
        total += 1
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
