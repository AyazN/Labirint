# сделал Мухаметзянов Дамир

from function_sql import *
import pygame
from settings import *
from mini_game import main_noughts_crosses
from function import save_game
from final import *
from player import *

num_exit = 0


def redraw_new_window(screen, dead, win, enemy, player, img_kill, user_id):
    global num_exit
    my_font = pygame.font.SysFont('arial', 130)
    text_surface = my_font.render('YOU WIN', False, (255, 204, 0))
    text_surface_died = my_font.render('YOU DIED', False, (255, 0, 0))
    if dead:
        save_game(enemy, player, img_kill, user_id)
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


def check_all_nulls():
    if not main_noughts_crosses():
        return True
    return False


def main_play(running, user_id, player_pos=(1, 1), enemy_pos=(23, 1), play_nulls=True, total=0, num=0, dead=False,
              img_kill=False, img_fire=False, win=False, killing=False):
    global num_exit
    pygame.init()
    screen = pygame.display.set_mode(RES)
    player, enemy, level_x, level_y = generate_level(load_level('map'))
    player.pos_x, player.pos_y = player_pos
    enemy.pos_x, enemy.pos_y = enemy_pos
    player.player_move(0, 0)
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
        if bool(nulls) and player.get_pos() == nulls[0] and play_nulls:
            dead = check_all_nulls()
            main_play(running, user_id, player.get_pos(), enemy.get_pos()[0], play_nulls=False,
                      img_kill=img_kill, img_fire=img_fire, killing=killing, total=total, num=num)
            running = False
            continue
        save_game(enemy, player, img_kill, user_id)
        if ((enemy.collision_check(player) and not img_kill) or
           (enemy.collision_check_with_fire(player) and img_fire)) and not dead:
            dead = True
            save_game(enemy, player, img_kill, user_id)
        if player.get_pos() == castle[0]:
            win = True
        if total % 25 == 0 and total > 25 and not win and not dead:
            enemy.enemy_move(player, killing)
        if total % 100 == 0 and total > 100 and not win and not dead:
            tile_images['frame'] = load_image('fire.png') if num % 2 == 0 else load_image('frame.png')
            img_fire = True if not img_fire else False
            [Tile('frame', fires[i][0], fires[i][1]) for i in range(len(fires))]
            num += 1
        redraw_new_window(screen, dead, win, enemy, player, img_kill, user_id)
        total += 1
        pygame.display.flip()
        clock.tick(FPS)
    save_game(enemy, player, img_kill, user_id)
    pygame.quit()


