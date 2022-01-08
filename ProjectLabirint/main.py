# сделал Мухаметзянов Дамир

from function_sql import *
import pygame
from settings import *
from mini_game import main_noughts_crosses
from final import *
from player import *

num_exit = ZERO
time_seconds = ZERO


def save_game(enemy, player, img_kill, user_id):
    if enemy.collision_check(player) and not img_kill:
        add_new_save(user_id, player.get_pos()[ZERO], player.get_pos()[ONE], enemy.start_pos_rt()[ZERO],
                     enemy.start_pos_rt()[ONE],
                     select_map_id(open_map()))
    else:
        add_new_save(user_id, player.get_pos()[ZERO], player.get_pos()[ONE], enemy.get_pos()[ZERO][ZERO],
                     enemy.get_pos()[ZERO][ONE],
                     select_map_id(open_map()))


def redraw_new_window(screen, dead, win, enemy, player, img_kill, user_id):
    global num_exit
    my_font = pygame.font.SysFont('arial', FONT_RES)
    text_surface = my_font.render('YOU WIN', False, GOLD)
    text_surface_died = my_font.render('YOU DIED', False, RED_COLOR)
    if dead:
        save_game(enemy, player, img_kill, user_id)
        screen.fill('Black')
        screen.blit(text_surface_died, (WIDTH // OME_OF_FOUR + TILE, HEIGHT // ONE_OF_THREE))
        num_exit += ONE_ITERATION
    elif win:
        screen.fill('Black')
        screen.blit(text_surface, (WIDTH // ONE_OF_THREE, HEIGHT // ONE_OF_THREE))
        create_particles((random.randint(ONE_COORD, WIDTH), random.randint(ONE_COORD, HEIGHT)))
        all_sprites_new.draw(screen)
        all_sprites_new.update()
        num_exit += ONE_ITERATION
    else:
        all_sprites.draw(screen)
        all_sprites.update()


def check_all_nulls():
    if not main_noughts_crosses():
        return True
    return False


def main_play(running, user_id, player_pos=SPAWN_PLAYER, enemy_pos=SPAWN_ENEMY, play_nulls=True, total=ZERO, num=ZERO,
              dead=False,
              img_kill=False, img_fire=False, win=False, killing=False):
    global num_exit, time_seconds
    pygame.init()
    screen = pygame.display.set_mode(RES)
    player, enemy, level_x, level_y = generate_level(load_level('map'))
    player.pos_x, player.pos_y = player_pos
    enemy.pos_x, enemy.pos_y = enemy_pos
    player.player_move(ZERO, ZERO)
    clock = pygame.time.Clock()
    if img_kill:
        enemy.image = load_image('kill.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(enemy, player, img_kill, user_id)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.player_move(MOVE_LEFT_X, MOVE_LEFT_Y)
                if event.key == pygame.K_RIGHT:
                    player.player_move(MOVE_RIGHT_X, MOVE_RIGHT_Y)
                if event.key == pygame.K_UP:
                    player.player_move(MOVE_UP_X, MOVE_UP_Y)
                if event.key == pygame.K_DOWN:
                    player.player_move(MOVE_DOWN_X, MOVE_DOWN_Y)
                if event.key == pygame.K_SPACE and player.get_pos() in enemy.get_pos():
                    enemy.image = load_image('kill.png')
                    img_kill = True
                    killing = True
        screen.fill('Grey')
        if num_exit % BIG_ITERATION == ZERO and num_exit > BIG_ITERATION:
            pygame.display.flip()
            print(time_seconds)
            running = False
            continue
        if bool(nulls) and player.get_pos() == nulls[ZERO] and play_nulls:
            dead = check_all_nulls()
            main_play(running, user_id, player.get_pos(), enemy.get_pos()[ZERO], play_nulls=False,
                      img_kill=img_kill, img_fire=img_fire, killing=killing, total=total, num=num, dead=dead)
            running = False
            continue
        save_game(enemy, player, img_kill, user_id)
        if ((enemy.collision_check(player) and not img_kill) or
            (enemy.collision_check_with_fire(player) and img_fire)) and not dead:
            dead = True
            save_game(enemy, player, img_kill, user_id)
        if player.get_pos() == castle[ZERO]:
            win = True
        if total % SMALL_ITERATION == ZERO and total > SMALL_ITERATION and not win and not dead:
            enemy.enemy_move(player, killing)
        if total % BIG_ITERATION == ZERO and total > BIG_ITERATION and not win and not dead:
            tile_images['frame'] = load_image('fire.png') if num % NUM_FIRE_FACE == ZERO else load_image('frame.png')
            img_fire = True if not img_fire else False
            [Tile('frame', fires[i][ZERO], fires[i][ONE]) for i in range(len(fires))]
            num += ONE_ITERATION
        redraw_new_window(screen, dead, win, enemy, player, img_kill, user_id)
        total += ONE_ITERATION
        pygame.display.flip()
        time_millis = clock.tick(FPS)
        time_seconds += time_millis / ITERATION_TICK
    save_game(enemy, player, img_kill, user_id)
    pygame.quit()

