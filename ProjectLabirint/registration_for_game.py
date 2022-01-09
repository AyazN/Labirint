import pygame
import pygame as pg
from registration import *
from start import start_menu_game

pygame.init()
win = pygame.display.set_mode((800, 600))
win.fill(pygame.Color('red'))

con = sqlite3.connect('SQL/labirint_db.db')
cur = con.cursor()
COLOR_INACTIVE = pg.Color('yellow')
COLOR_ACTIVE = pg.Color('blue')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    pass
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


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
            font = pygame.font.SysFont('calibri', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


run = True
green_button = Button(pygame.Color('red'), 180, 175, 450, 100, 'Регистрация')
red_button = Button(pygame.Color('red'), 270, 285, 250, 100, "Вход")
reg = 0
vchod = 0
while run:
    win.fill(pygame.Color('red'))
    if reg == 0 and vchod == 0:
        green_button.draw(win, (0, 0, 0))
        red_button.draw(win, (0, 0, 0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.isOver(pos):
                    reg += 1
                if red_button.isOver(pos):
                    vchod += 1

            if event.type == pygame.MOUSEMOTION:
                if green_button.isOver(pos):
                    green_button.color = pygame.Color('grey')
                else:
                    green_button.color = pygame.Color('green')
                if red_button.isOver(pos):
                    red_button.color = pygame.Color('grey')
                else:
                    red_button.color = pygame.Color('green')
    elif reg != 0:
        clock = pg.time.Clock()
        input_box1 = InputBox(300, 200, 140, 32)
        input_box2 = InputBox(300, 300, 140, 32)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        myfont_1 = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Логин', False, pygame.Color('white'))
        textsurface_1 = myfont_1.render('Пароль', False, pygame.Color('white'))
        go_but = Button(pygame.Color('red'), 170, 350, 450, 90, "Регистрация")
        input_boxes = [input_box1, input_box2]
        done = False
        login = input_box1.text
        passw = input_box2.text
        prov_user = []
        flag = 0
        flag_1 = 0
        flag_2 = 0
        check_username = '''SELECT login from accounts'''
        cur.execute(check_username)
        records = cur.fetchall()
        while not done:
            for event in pg.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_but.isOver(pos):
                        prov_user = []
                        check_username = '''SELECT login from accounts'''
                        cur.execute(check_username)
                        records = cur.fetchall()
                        for row in records:
                            prov_user.append(str(row[0]))
                        login = input_box1.text
                        passw = input_box2.text
                        if len(passw) == 0 or len(login) == 0:
                            flag = True
                            print('empty str')
                        elif login in prov_user:
                            print('have user with this login')
                            flag_1 = True
                        else:
                            random_id = random.randint(1000, 9999)
                            sqlite_insert = '''INSERT INTO accounts
                                                (id, login, password)
                                                VALUES (?, ?, ?);'''
                            data_tuple = (random_id, login, passw)
                            cur.execute(sqlite_insert, data_tuple)
                            con.commit()
                            flag_2 = True
                            num = select_account_id(login, passw)
                            start_menu_game(True, num)
                            print('OK')

                if event.type == pg.QUIT:
                    done = True
                if event.type == pygame.MOUSEMOTION:
                    if go_but.isOver(pos):
                        go_but.color = pygame.Color('grey')
                    else:
                        go_but.color = pygame.Color('red')
                for box in input_boxes:
                    box.handle_event(event)
                pygame.display.update()
            for box in input_boxes:
                box.update()
            win.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(win)
                go_but.draw(win, (0, 0, 0))
                win.blit(textsurface, (355, 150))
                win.blit(textsurface_1, (355, 250))
                text_quk = ''
                x, y = 0, 0
                text_quk_23 = 'пустая строка'
                text_quk_1 = 'такой пользователь существует'
                text_quk_2 = 'УСПЕШНО'
                if flag_1:
                    text_quk = text_quk_1
                if flag:
                    text_quk = text_quk_23
                if flag_2:
                    text_quk = text_quk_2
                    run = False
                myfont_2 = pygame.font.SysFont('Comic Sans MS', 30)
                textsurface_2 = myfont_2.render(text_quk, False, pygame.Color('red'))
                win.blit(textsurface_2, (x, y))

            pg.display.flip()
            clock.tick(30)
            run = False

            pygame.display.update()
    elif vchod != 0:
        clock = pg.time.Clock()
        input_box1 = InputBox(300, 200, 140, 32)
        input_box2 = InputBox(300, 300, 140, 32)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        myfont_1 = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Логин', False, pygame.Color('white'))
        textsurface_1 = myfont_1.render('Пароль', False, pygame.Color('white'))
        go_but = Button(pygame.Color('red'), 170, 350, 450, 90, "Вход")
        input_boxes = [input_box1, input_box2]
        done = False
        flag = 0
        flag_1 = 0
        flag_2 = 0
        flag_0 = 0
        flag_10 = 0
        x = 0
        y = 0
        while not done:
            for event in pg.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_but.isOver(pos):
                        login = input_box1.text
                        passw = input_box2.text
                        check_username = '''SELECT login from accounts'''
                        check_pass = '''SELECT password from accounts'''
                        cur.execute(check_username)
                        records = cur.fetchall()
                        cur.execute(check_pass)
                        records_1 = cur.fetchall()
                        prov_user = []
                        prov_pass = []
                        for row in records:
                            prov_user.append(str(row[0]))
                        for row_1 in records_1:
                            prov_pass.append(str(row_1[0]))
                        if len(login) == 0 or len(passw) == 0:
                            flag_0 = True
                        else:
                            if login in prov_user:
                                if passw in prov_pass:
                                    flag = True
                                    num = select_account_id(login, passw)
                                    start_menu_game(True, num)
                                    quit()
                                    print('correct')
                                else:
                                    flag_1 = True
                                    print('not correct pass')
                            else:
                                flag_2 = True
                                print('user not found')
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)

                if event.type == pygame.MOUSEMOTION:
                    if go_but.isOver(pos):
                        go_but.color = pygame.Color('grey')
                    else:
                        go_but.color = pygame.Color('red')

            for box in input_boxes:
                box.update()
            win.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(win)
                go_but.draw(win, (0, 0, 0))
                win.blit(textsurface, (355, 150))
                win.blit(textsurface_1, (355, 250))
                text_quk = ''
                text_quk_23 = 'успешно'
                text_quk_1 = 'неправильный пароль'
                text_quk_2 = 'игрок не найден'
                text_quk_3 = 'пустая строка'
                if flag_0:
                    text_quk = text_quk_3
                if flag_1:
                    text_quk = text_quk_1
                if flag_2:
                    text_quk = text_quk_2
                if flag:
                    text_quk = text_quk_23
                    run = False
                myfont_2 = pygame.font.SysFont('Comic Sans MS', 30)
                textsurface_2 = myfont_2.render(text_quk, False, pygame.Color('red'))
                win.blit(textsurface_2, (x, y))
            pg.display.flip()
            clock.tick()
            run = False
    pygame.display.update()
