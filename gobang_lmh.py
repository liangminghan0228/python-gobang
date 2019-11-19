import pygame as pg
import math
WIDTH = 40
COLUMN = 15
ROW = 15

list_ai = []
list_hu = []
list_sum = [] #双方下过的
list_all = [] #整个棋盘的店

def board():#绘制界面
    pg.init()
    pg.display.set_caption('五子棋')
    screen = pg.display.set_mode((WIDTH*(COLUMN+1), WIDTH*(ROW+1)))
    screen.fill((249, 214, 91))
    i1 = WIDTH/2

    while i1 <= WIDTH * (COLUMN + 1):
        l = pg.draw.line(screen, (0, 0, 0), (i1, WIDTH/2), (i1, WIDTH * (COLUMN + 1/2)), 2)
        i1 = i1 + WIDTH
    i2 = WIDTH/2

    while i2 <= WIDTH * (ROW + 1):
        l = l = pg.draw.line(screen, (0, 0, 0), (WIDTH/2, i2), (WIDTH * (ROW + 1/2), i2), 2)
        i2 = i2 + WIDTH
    return screen


def main():
    gobang = board()
    #初始化list_all
    for i in range(COLUMN+1):
        for j in range(ROW+1):
            list_all.append((i, j))
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit()
            pg.display.flip()
            # 默认人先下
            ai_turn = False
            while True:
                if ai_turn:
                    pg.event.wait()
                    #ai的col和row由计算获得
                    if pg.mouse.get_pressed()[0] == 1:
                        x, y = pg.mouse.get_pos()
                        col = math.floor(x / 40)
                        row = math.floor(y / 40)
                        if not (col, row) in list_sum:
                            list_sum.append((col, row))
                            x = int((col + 1 / 2) * WIDTH)
                            y = int((row + 1 / 2) * WIDTH)
                            print(list_sum)
                            pg.draw.circle(gobang, (255, 255, 255), (x, y), 15, 0)
                            pg.display.flip()
                            print('lmh')
                            ai_turn = False

                else:
                    pg.event.wait()
                    if pg.mouse.get_pressed()[0] == 1:
                        x, y = pg.mouse.get_pos()
                        col = math.floor(x / 40)
                        row = math.floor(y / 40)
                        if not (col, row) in list_sum:
                            list_sum.append((col, row))
                            x = int((col + 1 / 2) * WIDTH)
                            y = int((row + 1 / 2) * WIDTH)
                            print(list_sum)
                            pg.draw.circle(gobang, (0, 0, 0), (x, y), 15, 0)
                            pg.display.flip()
                            print('lmh')
                            ai_turn = True

if __name__ == '__main__':
    main()