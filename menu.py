import pygame
from connect_db import *
pygame.init()
win = pygame.display.set_mode((800, 600))
win.fill((0, 180, 210))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button():
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
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


run = True
green_button = Button((0, 255, 0), 180, 175, 450, 100, "Начать игру")
red_button = Button((255, 0, 0), 270, 285, 250, 100, "Выход")
info_button = Button(pygame.Color('Yellow'), 75, 395, 650, 100, 'Информация об игре')
registr_button = Button(pygame.Color('red'), 100, 500, 650, 100, 'Регистрация')
BackGround = Background('data/main_menu_1.jpg', [0, 0])

while run:
    win.fill([255, 255, 255])
    win.blit(BackGround.image, BackGround.rect)
    green_button.draw(win, (0, 0, 0))
    red_button.draw(win, (0, 0, 0))
    info_button.draw(win, (0, 0, 0))
    registr_button.draw(win, (0,0,0))
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if green_button.isOver(pos):
                print("clicked the Button")
            if red_button.isOver(pos):
                print("clicked the 2Button")
                run = False
                pygame.quit()
                quit()
            if info_button.isOver(pos):
                print('clicked info_button')
            if registr_button.isOver(pos):
                main_account_screen()

        if event.type == pygame.MOUSEMOTION:
            if green_button.isOver(pos):
                green_button.color = (105, 105, 105)
            else:
                green_button.color = (0, 255, 0)
            if red_button.isOver(pos):
                red_button.color = (105, 105, 105)
            else:
                red_button.color = (255, 0, 0)
            if info_button.isOver(pos):
                info_button.color = pygame.Color('grey')
            else:
                info_button.color = pygame.Color('violet')
            if registr_button.isOver(pos):
                registr_button.color = pygame.Color('grey')
            else:
                registr_button.color = pygame.Color('yellow')
    pygame.display.update()