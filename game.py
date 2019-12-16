import sys, pygame
from pygame import *
from pygame.locals import *
from pygame.sprite import *
from PIL import Image
from numpy import full
from random import randint


class ForceWielder(Sprite):
    def __init__(self, name):
        Sprite.__init__(self)
        self.item = False
        self.key = False
        self.lightsaber = True
        self.direction = RIGHT
        if name == 'kenobi':
            self.saberTick = 10
            self.image = pygame.transform.scale(image.load('benkenobir.png'), (BOXSIZE, BOXSIZE))
            self.rect = self.image.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
        elif name == 'vader':
            self.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
            self.rect = self.image.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 2))


class Block(Sprite):
    def __init__(self, type):
        Sprite.__init__(self)


class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)



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
MINIBOSS = 6
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
    MINIBOSS: YELLOW,
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
    global DISPLAYSURF, GLOBALSURF, FPSCLOCK, ANAKIN, ENEMY
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GLOBALSURF = Surface((1, 1))
    pygame.display.set_caption("Anakin's Adventure")
    pygame.display.update()
    ANAKIN = ForceWielder('vader')
    ENEMY = ForceWielder('kenobi')
    mobmove = False
    board, baseboard, playx, playy, enemyx, enemyy = readPic('deathstar.png')
    drawInventory()
    hintText1 = 'Controls:'
    hintText2 = 'Use arrow keys or WASD to move'
    hintText3 = 'Space bar will adjust lightsaber'
    hintText4 = 'which changes movement speed.'

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
    startx, starty = playx, playy
    pygame.display.update()

    time = pygame.time.get_ticks()
    cooldown = 0
    while True:
        updateClock()

        cooldown -= pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE:
                ANAKIN.lightsaber = not ANAKIN.lightsaber
                if ANAKIN.lightsaber:
                    ANAKIN.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
                else:
                    ANAKIN.image = pygame.transform.scale(image.load('darthvadernl.png'), (BOXSIZE, BOXSIZE))
                move(ANAKIN.direction, playx, playy, board, baseboard, mobmove)

        keys = pygame.key.get_pressed()
        if cooldown <= 0:
            if ANAKIN.lightsaber:
                cooldown = 200
            else:
                cooldown = 100

            if (keys[K_LEFT] or keys[K_a]) and checkForMove(board, playx - 1, playy):
                playx -= 1
                playx, playy = move(LEFT, playx, playy, board, baseboard, mobmove)
                if checkForVoid(board, playx, playy):
                    playx, playy = startx, starty
                    move(RIGHT, playx, playy, board, baseboard, mobmove)

            elif (keys[K_RIGHT] or keys[K_d]) and checkForMove(board, playx + 1, playy):
                playx += 1
                playx, playy = move(RIGHT, playx, playy, board, baseboard, mobmove)
                if checkForVoid(board, playx, playy):
                    playx, playy = startx, starty
                    move(RIGHT, playx, playy, board, baseboard, mobmove)

            elif (keys[K_UP] or keys[K_w]) and checkForMove(board, playx, playy - 1):
                playy -= 1
                playx, playy = move(UP, playx, playy, board, baseboard, mobmove)
                if checkForVoid(board, playx, playy):
                    playx, playy = startx, starty
                    move(RIGHT, playx, playy, board, baseboard, mobmove)

            elif (keys[K_DOWN] or keys[K_s]) and checkForMove(board, playx, playy + 1):
                playy += 1
                playx, playy = move(DOWN, playx, playy, board, baseboard, mobmove)
                if checkForVoid(board, playx, playy):
                    playx, playy = startx, starty
                    move(RIGHT, playx, playy, board, baseboard, mobmove)
            else:
                cooldown = 0

        if playx == 59 and playy == 93:
            mobmove = True

            left, top = leftTopCoordsOfBox(playx, playy)
            GLOBALSURF.blit(ANAKIN.image, (left, top))
        pygame.display.update()


def readPic(filename):
    blocks = {
        LGRAY: BLANK,
        DGRAY: WALL,
        GREEN: DOOR,
        BLACK: VOID,
        TEAL: SHIELD,
        ORANGE: DROID,
        YELLOW: MINIBOSS,
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
    baseboard = full(size, BLANK, dtype=Block)
    global GLOBALSURF
    print(boxx * BOXSIZE, boxy * BOXSIZE)
    GLOBALSURF = Surface((boxx * BOXSIZE, boxy * BOXSIZE))
    GLOBALSURF.fill(BLACK)
    startx, starty, enemyx, enemyy = 0, 0, 0, 0
    for y in range(boxx):
        for x in range(boxy):
            color = pix[y, x][:3]
            board[y][x] = blocks[color]
            baseboard[y][x] = blocks[color]
            if color == RED:
                pygame.draw.rect(GLOBALSURF, DGREEN, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(ANAKIN.image, (y * BOXSIZE, x * BOXSIZE))
                startx, starty = y, x
                board[y][x] = blocks[DGREEN]
                baseboard[y][x] = blocks[DGREEN]
            elif color == BLUE:
                pygame.draw.rect(GLOBALSURF, LGRAY, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(ENEMY.image, (y * BOXSIZE, x * BOXSIZE))
                enemyx, enemyy = y, x
            elif color == ORANGE:
                pygame.draw.rect(GLOBALSURF, LGRAY, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)), (y * BOXSIZE, x * BOXSIZE))
                baseboard[y][x] = blocks[LGRAY]
            else:
                pygame.draw.rect(GLOBALSURF, color, (y * BOXSIZE, x * BOXSIZE, BOXSIZE, BOXSIZE))
    left, top = leftTopCoordsOfBox(startx, starty)
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(GLOBALSURF,
                     (int(WINDOWWIDTH / 2 / BOXSIZE) * BOXSIZE - left, int(WINDOWHEIGHT / 2 / BOXSIZE) * BOXSIZE - top))

    return board, baseboard, startx, starty, enemyx, enemyy


def move(direction, playx, playy, board, baseboard, mobmove):

    left, top = leftTopCoordsOfBox(playx, playy)
    pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))

    checkForItem(board, playx, playy)
    checkForKey(board, playx, playy)

    if direction == LEFT:
        if ANAKIN.lightsaber:
            ANAKIN.image = pygame.transform.scale(image.load('darthvaderr.png'), (BOXSIZE, BOXSIZE))
        else:
            ANAKIN.image = pygame.transform.scale(image.load('darthvadernlr.png'), (BOXSIZE, BOXSIZE))
        ANAKIN.direction = LEFT
        GLOBALSURF.blit(ANAKIN.image, (left, top))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx + 1][playy]], (left + BOXSIZE, top, BOXSIZE, BOXSIZE))
        DISPLAYSURF.blit(GLOBALSURF, (WINDOWWIDTH / 2 - left, WINDOWHEIGHT / 2 - top))
        while checkForShield(board, playx, playy):
            wait = 1000
            while wait > 0:
                wait -= pygame.time.get_ticks()
            if checkForMove(board, playx - 1, playy):
                playx -= 1
                playx, playy = move(LEFT, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx, playy - 1):
                playy -= 1
                playx, playy = move(UP, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx, playy + 1):
                playy += 1
                playx, playy = move(DOWN, playx, playy, board, baseboard, mobmove)
            if checkForVoid(board, playx, playy):
                return playx, playy
            pygame.display.update()

    elif direction == RIGHT:
        if ANAKIN.lightsaber:
            ANAKIN.image = pygame.transform.scale(image.load('darthvader.png'), (BOXSIZE, BOXSIZE))
        else:
            ANAKIN.image = pygame.transform.scale(image.load('darthvadernl.png'), (BOXSIZE, BOXSIZE))
        ANAKIN.direction = RIGHT
        GLOBALSURF.blit(ANAKIN.image, (left, top))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx - 1][playy]], (left - BOXSIZE, top, BOXSIZE, BOXSIZE))
        DISPLAYSURF.blit(GLOBALSURF, (WINDOWWIDTH / 2 - left, WINDOWHEIGHT / 2 - top))
        while checkForShield(board, playx, playy):
            wait = 1000
            while wait > 0:
                wait -= pygame.time.get_ticks()
            if checkForMove(board, playx + 1, playy):
                playx += 1
                playx, playy = move(RIGHT, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx, playy + 1):
                playy += 1
                playx, playy = move(DOWN, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx, playy - 1):
                playy -= 1
                playx, playy = move(UP, playx, playy, board, baseboard, mobmove)
            if checkForVoid(board, playx, playy):
                return playx, playy
            pygame.display.update()

    elif direction == UP:
        GLOBALSURF.blit(ANAKIN.image, (left, top))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy + 1]], (left, top + BOXSIZE, BOXSIZE, BOXSIZE))
        DISPLAYSURF.blit(GLOBALSURF, (WINDOWWIDTH / 2 - left, WINDOWHEIGHT / 2 - top))
        while checkForShield(board, playx, playy):
            wait = 1000
            while wait > 0:
                wait -= pygame.time.get_ticks()
            if checkForMove(board, playx, playy - 1):
                playy -= 1
                playx, playy = move(UP, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx + 1, playy):
                playx += 1
                playx, playy = move(RIGHT, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx - 1, playy):
                playx -= 1
                playx, playy = move(LEFT, playx, playy, board, baseboard, mobmove)
            if checkForVoid(board, playx, playy):
                return playx, playy
            pygame.display.update()

    elif direction == DOWN:
        GLOBALSURF.blit(ANAKIN.image, (left, top))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy - 1]], (left, top - BOXSIZE, BOXSIZE, BOXSIZE))
        DISPLAYSURF.blit(GLOBALSURF, (WINDOWWIDTH / 2 - left, WINDOWHEIGHT / 2 - top))
        while checkForShield(board, playx, playy):
            wait = 1000
            while wait > 0:
                wait -= pygame.time.get_ticks()
            if checkForMove(board, playx, playy + 1):
                playy += 1
                playx, playy = move(DOWN, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx - 1, playy):
                playx -= 1
                playx, playy = move(LEFT, playx, playy, board, baseboard, mobmove)
            elif checkForMove(board, playx + 1, playy):
                playx += 1
                playx, playy = move(RIGHT, playx, playy, board, baseboard, mobmove)
            if checkForVoid(board, playx, playy):
                return playx, playy
            pygame.display.update()

    drawInventory()

    if board[playx][playy] == 11:
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
        elif playx == 59:
            if playy == 93:
                hintText1 = "The plans are behind these rebels."
                hintText2 = "Beware to not get killed."
                hintText3 = "They move in random directions"
                hintText4 = "and may move more than once"
                hintText5 = "but often times won't"
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

        if mobmove:
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == 5:
                        moveDir = randint(0, 3)
                        if moveDir == 0:
                            if checkForMove(board, x - 1, y) and board[x - 1][y] not in [5, 8]:
                                board[x - 1][y] = 5
                                left, top = leftTopCoordsOfBox(x - 1, y)
                                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)),
                                                (left, top))
                                left, top = leftTopCoordsOfBox(x, y)
                                board[x][y] = baseboard[x][y]
                                pygame.draw.rect(GLOBALSURF, BLOCKS[board[x][y]], (left, top, BOXSIZE, BOXSIZE))
                        elif moveDir == 1:
                            if checkForMove(board, x + 1, y) and board[x + 1][y] not in [5, 8]:
                                board[x + 1][y] = 5
                                left, top = leftTopCoordsOfBox(x + 1, y)
                                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)),
                                                (left, top))
                                left, top = leftTopCoordsOfBox(x, y)
                                board[x][y] = baseboard[x][y]
                                pygame.draw.rect(GLOBALSURF, BLOCKS[board[x][y]], (left, top, BOXSIZE, BOXSIZE))
                        elif moveDir == 2:
                            if checkForMove(board, x, y - 1) and board[x][y - 1] not in [5, 8]:
                                board[x][y - 1] = 5
                                left, top = leftTopCoordsOfBox(x, y - 1)
                                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)),
                                                (left, top))
                                left, top = leftTopCoordsOfBox(x, y)
                                board[x][y] = baseboard[x][y]
                                pygame.draw.rect(GLOBALSURF, BLOCKS[board[x][y]], (left, top, BOXSIZE, BOXSIZE))
                        else:
                            if checkForMove(board, x, y + 1) and board[x][y + 1] not in [5, 8]:
                                board[x][y + 1] = 5
                                left, top = leftTopCoordsOfBox(x, y + 1)
                                GLOBALSURF.blit(pygame.transform.scale(image.load('rebel.png'), (BOXSIZE, BOXSIZE)),
                                                (left, top))
                                left, top = leftTopCoordsOfBox(x, y)
                                board[x][y] = baseboard[x][y]
                                pygame.draw.rect(GLOBALSURF, BLOCKS[board[x][y]], (left, top, BOXSIZE, BOXSIZE))
                        pygame.display.flip()

    return playx, playy


def checkForMove(board, playx, playy):
    canMove = False
    if board[playx][playy] == 1:
        canMove = False
    elif board[playx][playy] in [0, 3, 4, 6, 10]:
        canMove = True
    elif board[playx][playy] == 7 and ANAKIN.item:
        canMove = True
    elif board[playx][playy] == 2 and ANAKIN.key:
        canMove = True
        openDoor(board, playx, playy)
    elif board[playx][playy] in [5, 8] and ANAKIN.lightsaber:
        canMove = True
    elif board[playx][playy] == 11:
        canMove = True
    return canMove


def checkForVoid(board, playx, playy):
    if board[playx][playy] == 3:
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx + 1][playy]], (left + BOXSIZE, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx - 1][playy]], (left - BOXSIZE, top, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy + 1]], (left, top + BOXSIZE, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy - 1]], (left, top - BOXSIZE, BOXSIZE, BOXSIZE))
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))
        return True
    return False


def checkForShield(board, playx, playy):
    if board[playx][playy] == 4:
        return True
    return False


def checkForItem(board, playx, playy):
    if board[playx][playy] == 6:
        ANAKIN.item = True
        board[playx][playy] = 0
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def checkForKey(board, playx, playy):
    if board[playx][playy] == 10:
        ANAKIN.key = True
        board[playx][playy] = 0
        left, top = leftTopCoordsOfBox(playx, playy)
        pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def openDoor(board, playx, playy):
    board[playx][playy] = 0
    left, top = leftTopCoordsOfBox(playx, playy)
    pygame.draw.rect(GLOBALSURF, BLOCKS[board[playx][playy]], (left, top, BOXSIZE, BOXSIZE))


def drawInventory():
    pygame.draw.rect(DISPLAYSURF, DGRAY, (0, 0, WINDOWWIDTH, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, DGRAY, (WINDOWWIDTH - BOXSIZE * 3, 0, BOXSIZE * 3, WINDOWHEIGHT))
    pygame.draw.rect(DISPLAYSURF, LGRAY, (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE * 2))
    if ANAKIN.item:
        pygame.draw.rect(DISPLAYSURF, YELLOW,
                         (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE))
    if ANAKIN.key:
        pygame.draw.rect(DISPLAYSURF, MAGENTA,
                         (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 3 / 2, BOXSIZE, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, BLACK, (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 3 / 2, BOXSIZE, BOXSIZE), 5)
    pygame.draw.rect(DISPLAYSURF, BLACK, (WINDOWWIDTH - int(BOXSIZE * 3 / 2), WINDOWHEIGHT - BOXSIZE * 5 / 2, BOXSIZE, BOXSIZE), 5)

    titleFont = getScaledFont(200, 100, 'A New Hope', 'Comic Sans')
    titleText = titleFont.render('A New Hope', 1, BLACK)
    titleText_rect = titleText.get_rect(center=(100, 75))
    DISPLAYSURF.blit(titleText, titleText_rect)

    updateClock()


def updateClock():
    pygame.draw.rect(DISPLAYSURF, DGRAY, (WINDOWWIDTH - BOXSIZE * 5, 0, BOXSIZE * 2, BOXSIZE))
    numSeconds = int(pygame.time.get_ticks() / 1000)
    secFont = getScaledFont(100, 100, str(000), 'Comic Sans')
    text = secFont.render(str(numSeconds), 1, BLACK)
    text_rect = text.get_rect(center=(WINDOWWIDTH - BOXSIZE * 4, BOXSIZE / 2))
    DISPLAYSURF.blit(text, text_rect)


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
