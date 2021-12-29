import pygame

pygame.init()
win = pygame.display.set_mode((800, 500))
win.fill(pygame.Color('white'))

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('calibri', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def redrawWindow():
    win.fill(pygame.Color('white'))
    greenButton.draw(win)
    redButton.draw(win)

run = True
greenButton = Button(pygame.Color('yellow'), 280, 255, 250, 100, "Да")
redButton = Button(pygame.Color('green'), 280, 380, 250, 100, "Нет")
while run:
    redrawWindow()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                print("clicked the button_1")
            if redButton.isOver(pos):
                print("clicked the button_2")
    pygame.display.update()