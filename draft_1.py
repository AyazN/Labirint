import pygame

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


def redrawWindow():
    win.fill([255, 255, 255])
    win.blit(BackGround.image, BackGround.rect)
    green_button.draw(win, (0, 0, 0))
    red_button.draw(win, (0, 0, 0))
    info_button.draw(win, (0,0,0))

run = True
green_button = Button((0, 255, 0), 280, 150, 250, 100, "Start")
red_button = Button((255, 0, 0), 280, 275, 250, 100, "Quit")
info_button = Button(pygame.Color('Yellow'), 280, 395, 250, 100, 'Info')
BackGround = Background('/Users/norbi273cool/PycharmProjects/YanexLyceum/data/main_menu_1.jpg', [0,0])

while run:
    redrawWindow()

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
    pygame.display.update()
