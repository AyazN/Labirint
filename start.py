import pygame
from settings import *
from function_sql import *
from main import main_play
from gen_map import run


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, False, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redraw_window(screen):
    screen.blit(BackGround.image, BackGround.rect)
    green_button.draw(screen, (0, 0, 0))
    red_button.draw(screen, (0, 0, 0))
    info_button.draw(screen, (0, 0, 0))


green_button = Button((0, 255, 0), WIDTH // 2 - 225, 225, 450, 100, "Начать игру")
red_button = Button((255, 0, 0), WIDTH // 2 - 125, 345, 250, 100, "Выход")
info_button = Button(pygame.Color('Yellow'), WIDTH // 2 - 325, 465, 650, 100, 'Загрузить игру')
BackGround = Background('data/labirint_mini.png', [0, 0])


def start_menu_game(running, user_id):
    pygame.init()
    screen = pygame.display.set_mode(RES)
    flag = False
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.is_over(pos):
                    run()
                    running = False
                    flag = True
                if red_button.is_over(pos):
                    print("clicked the 2Button")
                    running = False
                if info_button.is_over(pos):
                    reconstruct_map(user_id)
                    running = False
                    flag = True
                    print('clicked info_button')
            if event.type == pygame.MOUSEMOTION:
                if green_button.is_over(pos):
                    green_button.color = (105, 105, 105)
                else:
                    green_button.color = (0, 255, 0)
                if red_button.is_over(pos):
                    red_button.color = (105, 105, 105)
                else:
                    red_button.color = (255, 0, 0)
                if info_button.is_over(pos):
                    info_button.color = pygame.Color('grey')
                else:
                    info_button.color = pygame.Color('Yellow')
        screen.fill((255, 255, 255))
        redraw_window(screen)
        pygame.display.flip()
    main_play(flag, user_id)
    pygame.quit()


start_menu_game(True, 2)
