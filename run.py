import sys, pygame
from math import copysign
from pygame import *
from pygame.locals import *
from pygame.sprite import *
from PIL import Image
from numpy import full
from random import randint


class Vader(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.item = False
        self.key = False
        self.lightsaber = True
        self.direction = RIGHT
        self.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
        self.rect = self.image.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))

        self.pos = [0, 0]
        self.movePos = [0, 0]


class Block(Sprite):
    def __init__(self, type):
        Sprite.__init__(self)


class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.rect = None
        self.image = None
        self.pos = [0, 0]
        self.movePos = [0, 0]
        self.canMove = False

    def on_tick(self, board):
        print(board[0][0])


class Kenobi(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.lightsaber = True
        self.direction = RIGHT
        self.image = pygame.transform.scale(image.load('benkenobi.png'), (BOXSIZE, BOXSIZE))
        self.rect = self.image.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
        self.canMove = False

    def on_tick(self, board):
        self.movePos = [0, 0]
        if abs(VADER.pos[0] - self.pos[0]) >= abs(VADER.pos[1] - self.pos[1]):
            # self.movePos = [int(VADER.pos[0] - self.pos[0] / abs(VADER.pos[0] - self.pos[0])), 0]
            self.movePos = [int(copysign(1, VADER.pos[0] - self.pos[0])), 0]
        else:
            # self.movePos = [0, int(VADER.pos[1] - self.pos[1] / abs(VADER.pos[1] - self.pos[1]))]
            self.movePos = [0, int(copysign(1, VADER.pos[1] - self.pos[1]))]
            # print(int(VADER.pos[1] - self.pos[1] / abs(VADER.pos[1] - self.pos[1])))
        if checkForMove(board, self.pos, self.movePos, KENOBI):
            print(self.movePos)
            move(board, self.pos, self.movePos, self.image, self.pos[0], self.pos[1], KENOBI)


class Rebel(Mob):
    def __init__(self, pos):
        Mob.__init__(self)
        self.image = pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE))
        self.rect = self.image.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
        self.pos = pos
        self.canMove = False

    def on_tick(self, board):
        if randint(0, 1) == 0:
            self.movePos = [randint(-1, 1), 0]
        else:
            self.movePos = [0, randint(-1, 1)]
        if checkForMove(board, self.pos, self.movePos, Rebel):
            move(board, self.pos, self.movePos, self.image, self.pos[0], self.pos[1], Rebel)


WHITE = (255, 255, 255)
LGRAY = (200, 200, 200)
DGRAY = (100, 100, 100)
BLACK = (0, 0, 0)
TEAL = (0, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (250, 150, 0)
YELLOW = (250, 250, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
DGREEN = (50, 150, 0)

BLANK = 0
WALL = 1
DOOR = 2
VOID = 3
SHIELD = 4
DROID = 5
PLANS = 6
HANGAR = 7
BOSS = 8
START = 9
KEY = 10
HINT = 11

BLOCKS = {
    BLANK: LGRAY,
    WALL: DGRAY,
    DOOR: GREEN,
    VOID: BLACK,
    SHIELD: TEAL,
    DROID: ORANGE,
    PLANS: YELLOW,
    HANGAR: WHITE,
    BOSS: BLUE,
    START: RED,
    KEY: MAGENTA,
    HINT: DGREEN

}

BOXSIZE = 100
WINDOWWIDTH = 1500
WINDOWHEIGHT = 700
BOARDWIDTH = int(WINDOWWIDTH / BOXSIZE)
BOARDHEIGHT = int(WINDOWHEIGHT / BOXSIZE)

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


def main():
    global DISPLAYSURF, GLOBALSURF, FPSCLOCK, VADER, KENOBI, REBELS
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GLOBALSURF = Surface((1, 1))
    pygame.display.set_caption("Anakin's Adventure")
    pygame.display.update()
    VADER = Vader()
    KENOBI = Kenobi()
    REBELS = []
    board = readPic('deathstar.png')
    # drawInventory()
    startx, starty = VADER.pos
    updateHint(startx, starty)
    pygame.display.update()

    time = pygame.time.get_ticks()
    cooldown = 0
    while True:
        # updateClock()

        cooldown -= pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE:
                VADER.lightsaber = not VADER.lightsaber
                if VADER.lightsaber:
                    if VADER.direction == LEFT:
                        VADER.image = pygame.transform.scale(image.load('darthvaderr.png'), (BOXSIZE, BOXSIZE))
                    else:
                        VADER.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
                else:
                    if VADER.direction == LEFT:
                        VADER.image = pygame.transform.scale(image.load('darthvadernlr.png'), (BOXSIZE, BOXSIZE))
                    else:
                        VADER.image = pygame.transform.scale(image.load('darthvadernl.png'), (BOXSIZE, BOXSIZE))
                left, top = leftTopCoordsOfBox(VADER.pos[0], VADER.pos[1])
                GLOBALSURF.blit(VADER.image, (left, top))
                pygame.display.update()

        keys = pygame.key.get_pressed()
        if cooldown <= 0:
            if VADER.lightsaber:
                cooldown = 200
            else:
                cooldown = 100

            if keys[K_LEFT] or keys[K_a]:
                VADER.direction = LEFT
                if VADER.lightsaber:
                    VADER.image = pygame.transform.scale(image.load('darthvaderr.png'), (BOXSIZE, BOXSIZE))
                else:
                    VADER.image = pygame.transform.scale(image.load('darthvadernlr.png'), (BOXSIZE, BOXSIZE))
                VADER.movePos[0] -= 1
            elif keys[K_RIGHT] or keys[K_d]:
                VADER.direction = RIGHT
                if VADER.lightsaber:
                    VADER.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
                else:
                    VADER.image = pygame.transform.scale(image.load('darthvadernl.png'), (BOXSIZE, BOXSIZE))
                VADER.movePos[0] += 1
            elif keys[K_UP] or keys[K_w]:
                VADER.movePos[1] -= 1
            elif keys[K_DOWN] or keys[K_s]:
                VADER.movePos[1] += 1
            else:
                cooldown = 0
            vaderMove = VADER.movePos[0] != 0 or VADER.movePos[1] != 0
            if vaderMove and checkForMove(board, VADER.pos, VADER.movePos, VADER):
                move(board, VADER.pos, VADER.movePos, VADER.image, startx, starty, VADER)

            if KENOBI.canMove and vaderMove:
                KENOBI.on_tick(board)
            if REBELS[0].canMove and vaderMove:
                for i in range(len(REBELS)):
                    REBELS[i].on_tick(board)

            left, top = leftTopCoordsOfBox(VADER.pos[0], VADER.pos[1])
            GLOBALSURF.blit(VADER.image, (left, top))
            DISPLAYSURF.blit(GLOBALSURF, (
            int(WINDOWWIDTH / 2 / BOXSIZE) * BOXSIZE - left, int(WINDOWHEIGHT / 2 / BOXSIZE) * BOXSIZE - top))
            drawInventory(board)
            updateHint(VADER.pos[0], VADER.pos[1])

            VADER.movePos = [0, 0]
        pygame.display.update()


def readPic(filename):
    blocks = {
        LGRAY: BLANK,
        DGRAY: WALL,
        GREEN: DOOR,
        BLACK: VOID,
        TEAL: SHIELD,
        ORANGE: DROID,
        YELLOW: PLANS,
        WHITE: HANGAR,
        BLUE: BOSS,
        RED: START,
        MAGENTA: KEY,
        DGREEN: HINT
    }
    file = Image.open(filename)
    pix = file.load()
    size = file.size
    boxx, boxy = file.size
    board = full(size, BLANK, dtype=Block)
    global GLOBALSURF
    GLOBALSURF = Surface((boxx * BOXSIZE, boxy * BOXSIZE))
    GLOBALSURF.fill(BLACK)
    startx, starty = 0, 0
    for y in range(boxx):
        for x in range(boxy):
            color = pix[y, x][:3]
            board[y][x] = blocks[color]
            if color == RED:
                pygame.draw.rect(GLOBALSURF, DGREEN, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(VADER.image, (y * BOXSIZE, x * BOXSIZE))
                startx, starty = y, x
                board[y][x] = blocks[DGREEN]
            elif color == BLUE:
                pygame.draw.rect(GLOBALSURF, LGRAY, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(KENOBI.image, (y * BOXSIZE, x * BOXSIZE))
                board[y][x] = blocks[LGRAY]
                KENOBI.pos = [y, x]
            elif color == ORANGE:
                pygame.draw.rect(GLOBALSURF, LGRAY, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)),
                                (y * BOXSIZE, x * BOXSIZE))
                board[y][x] = blocks[LGRAY]
                REBELS.append(Rebel([y, x]))
            else:
                pygame.draw.rect(GLOBALSURF, color, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
    left, top = leftTopCoordsOfBox(startx, starty)
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(GLOBALSURF,
                     (int(WINDOWWIDTH / 2 / BOXSIZE) * BOXSIZE - left, int(WINDOWHEIGHT / 2 / BOXSIZE) * BOXSIZE - top))
    drawInventory(board)
    VADER.pos = [startx, starty]

    return board


def move(board, pos, movePos, image, startx, starty, player):
    left, top = leftTopCoordsOfBox(pos[0], pos[1])
    pygame.draw.rect(GLOBALSURF, BLOCKS[board[pos[0]][pos[1]]], (left, top, BOXSIZE, BOXSIZE))

    pos[0] += movePos[0]
    pos[1] += movePos[1]
    left, top = leftTopCoordsOfBox(pos[0], pos[1])

    checkForItem(board, pos)
    checkForKey(board, pos)

    GLOBALSURF.blit(image, (left, top))
    pygame.display.update()
    while checkForShield(board, pos):
        # wait = 1000
        # while wait > 0:
        # wait -= pygame.time.get_ticks()
        if checkForMove(board, pos, movePos, player):
            move(board, pos, movePos, image, startx, starty, player)
    if checkForVoid(board, pos):
        pos[0] = startx
        pos[1] = starty
    pygame.display.update()

    # drawInventory()
    # updateClock()

    if board[VADER.pos[0]][VADER.pos[1]] == 11:
        updateHint(VADER.pos[0], VADER.pos[1])

    movePos[0] = 0
    movePos[1] = 0


def checkForMove(board, pos, movePos, player):
    canMove = False
    playx = int(pos[0] + movePos[0])
    playy = int(pos[1] + movePos[1])
    if player is not Rebel:
        if board[playx][playy] == 1:
            canMove = False
        elif board[playx][playy] in [0, 4, 11]:
            canMove = True
        elif board[playx][playy] == 3:
            shieldPos = [playx, playy]
            if checkForMove(board, shieldPos, movePos, player):
                canMove = True
            else:
                canMove = False
        elif board[playx][playy] in [6, 10]:
            if player is VADER:
                canMove = True
            else:
                canMove = False
        elif board[playx][playy] == 7 and VADER.item:
            canMove = True
        elif board[playx][playy] == 2 and VADER.key:
            canMove = True
            openDoor(board, playx, playy)
        if player is VADER:
            if KENOBI.pos == [playx, playy]:
                if VADER.lightsaber is KENOBI.lightsaber:
                    canMove = False
                elif VADER.lightsaber:
                    canMove = True
                    KENOBI.pos = [0, 0]
                    KENOBI.canMove = False
                elif KENOBI.lightsaber:
                    canMove = True
                    VADER.pos = [89, 52]
            elif len(REBELS) > 0:
                for r in REBELS:
                    if r.pos == [playx, playy]:
                        if VADER.lightsaber:
                            canMove = True
                            REBELS.remove(r)
                        else:
                            canMove = True
                            VADER.pos = [89, 52]
        elif player is KENOBI:
            if VADER.pos == [playx, playy]:
                if VADER.lightsaber is KENOBI.lightsaber:
                    canMove = False
                elif VADER.lightsaber:
                    canMove = True
                    KENOBI.pos = [0, 0]
                    KENOBI.canMove = False
                elif KENOBI.lightsaber:
                    canMove = True
                    VADER.pos = [89, 52]
            elif len(REBELS) > 0:
                for r in REBELS:
                    if r.pos == [playx, playy]:
                        if VADER.lightsaber:
                            canMove = True
                            REBELS.remove(r)
                        else:
                            canMove = True
                            VADER.pos = [89, 52]
    else:
        if board[playx][playy] == 1:
            canMove = False
        elif board[playx][playy] in [0, 3, 4, 11]:
            canMove = True
        elif board[playx][playy] in [6, 10]:
            if player is VADER:
                canMove = True
            else:
                canMove = False
        elif board[playx][playy] == 7 and VADER.item:
            canMove = True
        elif board[playx][playy] == 2 and VADER.key:
            canMove = True
            openDoor(board, playx, playy)
        if VADER.pos == [playx, playy]:
            if VADER.lightsaber:
                canMove = False
            else:
                canMove = True
                VADER.pos = [89, 52]

    return canMove


def checkForVoid(board, pos):
    playx = pos[0]
    playy = pos[1]
    if board[playx][playy] == 3:
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx + 1][playy]], (left + BOXSIZE, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx - 1][playy]], (left - BOXSIZE, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy + 1]], (left, top + BOXSIZE, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy - 1]], (left, top - BOXSIZE, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))
        return True
    return False


def checkForShield(board, pos):
    playx = pos[0]
    playy = pos[1]
    if board[playx][playy] == 4:
        return True
    return False


def checkForItem(board, pos):
    playx = pos[0]
    playy = pos[1]
    if board[playx][playy] == 6:
        VADER.item = True
        board[playx][playy] = 0
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def checkForKey(board, pos):
    playx = pos[0]
    playy = pos[1]
    if board[playx][playy] == 10:
        VADER.key = True
        board[playx][playy] = 0
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def openDoor(board, playx, playy):
    board[playx][playy] = 0
    left, top = leftTopCoordsOfBox(playx, playy)
    pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def drawInventory(board):
    pygame.draw.rect(DISPLAYSURF, DGRAY, (0, 0, WINDOWWIDTH, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, DGRAY, (WINDOWWIDTH - BOXSIZE * 3, 0, BOXSIZE * 3, WINDOWHEIGHT))
    pygame.draw.rect(DISPLAYSURF, LGRAY,
                     (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE * 2))
    if VADER.item:
        pygame.draw.rect(DISPLAYSURF, YELLOW,
                         (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE))
    if VADER.key:
        pygame.draw.rect(DISPLAYSURF, MAGENTA,
                         (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 3 / 2, BOXSIZE, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 3 / 2, BOXSIZE, BOXSIZE), 5)
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE), 5)

    titleFont = getScaledFont(200, 100, 'A New Hope', 'Comic Sans')
    titleText = titleFont.render('A New Hope', 1, BLACK)
    titleText_rect = titleText.get_rect(center=(100, 75))
    DISPLAYSURF.blit(titleText, titleText_rect)

    updateClock(board)


def updateClock(board):
    pygame.draw.rect(DISPLAYSURF, DGRAY, (WINDOWWIDTH - BOXSIZE * 5, 0, BOXSIZE * 2, BOXSIZE))
    numSeconds = int(pygame.time.get_ticks() / 1000)
    secFont = getScaledFont(100, 100, str(000), 'Comic Sans')
    text = secFont.render(str(numSeconds), 1, BLACK)
    text_rect = text.get_rect(center=(WINDOWWIDTH - BOXSIZE * 4, BOXSIZE / 2))
    DISPLAYSURF.blit(text, text_rect)

    if numSeconds % 10 == 0:
        KENOBI.lightsaber = False
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[KENOBI.pos[0]][KENOBI.pos[1]]], (KENOBI.pos[0] * BOXSIZE, KENOBI.pos[1] * BOXSIZE, BOXSIZE, BOXSIZE))
    else:
        KENOBI.lightsaber = True
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[KENOBI.pos[0]][KENOBI.pos[1]]],
                         (KENOBI.pos[0] * BOXSIZE, KENOBI.pos[1] * BOXSIZE, BOXSIZE, BOXSIZE))

    if KENOBI.lightsaber:
        if KENOBI.direction == LEFT:
            KENOBI.image = pygame.transform.scale(image.load('benkenobir.png'), (BOXSIZE, BOXSIZE))
        else:
            KENOBI.image = pygame.transform.scale(image.load('benkenobi.png'), (BOXSIZE, BOXSIZE))
    else:
        if KENOBI.direction == LEFT:
            KENOBI.image = pygame.transform.scale(image.load('benkenobinlr.png'), (BOXSIZE, BOXSIZE))
        else:
            KENOBI.image = pygame.transform.scale(image.load('benkenobinl.png'), (BOXSIZE, BOXSIZE))
    left, top = leftTopCoordsOfBox(KENOBI.pos[0], KENOBI.pos[1])
    GLOBALSURF.blit(KENOBI.image, (left, top))


def updateHint(playx, playy):
    hintText1 = ''
    hintText2 = ''
    hintText3 = ''
    hintText4 = ''
    hintText5 = ''
    if playx == 19:
        if playy == 62:
            hintText1 = 'The force is strong in this block.'
            hintText2 = 'It will push you ahead.'
    elif playx == 28:
        if playy == 26:
            hintText1 = "I've been waiting for you, Obi-Wan."
            hintText2 = "We meet again at last."
            hintText3 = "The circle is now complete."
            hintText4 = "When I left you, I was but a learner."
            hintText5 = "Now I am the Master."
            KENOBI.canMove = True
            print('confrontation')
    elif playx == 59:
        if playy == 93:
            hintText1 = "The plans are behind these rebels."
            hintText2 = "Beware to not get killed."
            hintText3 = "They move in random directions"
            for i in range(len(REBELS)):
                REBELS[i].canMove = True
    elif playx == 89:
        if playy == 47:
            hintText1 = "I sense something,"
            hintText2 = "A presence I've not felt since..."
        elif playy == 51:
            hintText1 = 'You must acquire the'
            hintText2 = 'Death Star Plans'
            hintText3 = 'to finish Level One and'
            hintText4 = 'proceed to this area.'
        elif playy == 52:
            hintText1 = 'Controls:'
            hintText2 = 'Use arrow keys or WASD to move'
            hintText3 = 'Space bar will adjust lightsaber'
            hintText4 = 'which changes movement speed.'
        elif playy == 53:
            hintText1 = 'If the rebels have obtained'
            hintText2 = 'a complete technical reading of'
            hintText3 = 'this station, it is possible,'
            hintText4 = 'however unlikely, they might find'
            hintText5 = 'a weakness and exploit it.'
    font1 = pygame.font.SysFont('Comic Sans', 25)
    text1 = font1.render(hintText1, 1, WHITE)
    text_rect1 = text1.get_rect(center=(WINDOWWIDTH - BOXSIZE * 3 / 2, BOXSIZE / 2))
    DISPLAYSURF.blit(text1, text_rect1)

    font2 = pygame.font.SysFont('Comic Sans', 25)
    text2 = font2.render(hintText2, 1, WHITE)
    text_rect2 = text2.get_rect(center=(WINDOWWIDTH - BOXSIZE * 3 / 2, BOXSIZE))
    DISPLAYSURF.blit(text2, text_rect2)

    font3 = pygame.font.SysFont('Comic Sans', 25)
    text3 = font3.render(hintText3, 1, WHITE)
    text_rect3 = text3.get_rect(center=(WINDOWWIDTH - BOXSIZE * 3 / 2, BOXSIZE * 3 / 2))
    DISPLAYSURF.blit(text3, text_rect3)

    font4 = pygame.font.SysFont('Comic Sans', 25)
    text4 = font4.render(hintText4, 1, WHITE)
    text_rect4 = text4.get_rect(center=(WINDOWWIDTH - BOXSIZE * 3 / 2, BOXSIZE * 2))
    DISPLAYSURF.blit(text4, text_rect4)

    font5 = pygame.font.SysFont('Comic Sans', 25)
    text5 = font5.render(hintText5, 1, WHITE)
    text_rect5 = text5.get_rect(center=(WINDOWWIDTH - BOXSIZE * 3 / 2, BOXSIZE * 5 / 2))
    DISPLAYSURF.blit(text5, text_rect5)


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE
    top = boxy * BOXSIZE
    return left, top


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def getScaledFont(max_w, max_h, text, font_name):
    font_size = 0
    font = pygame.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    while w < max_w and h < max_h:
        font_size += 1
        font = pygame.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    return pygame.font.SysFont(font_name, font_size - 1)


if __name__ == '__main__':
    main()
