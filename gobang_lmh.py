import pygame as pg
import math
WIDTH = 40
COLUMN = 15
ROW = 15

list_ai = []
list_hu = []
list_sum = [] #双方下过的
list_all = [] #整个棋盘的店
next_step = [0, 0] #ai下一步下的位置
DEPTH = 2 #每次ai搜索的深度
CUT = 0
SEARCH = 0
#棋子形状的分数评估模型
score_shape = [
    (50, (0, 1, 1, 0, 0)),
    (50, (0, 0, 1, 1, 0)),
    (200, (1, 0, 1, 1, 0)),
    (200, (0, 1, 0, 1, 1)),
    (200, (1, 1, 0, 1, 0)),
    (200, (0, 1, 1, 0, 1)),
    (500, (1, 1, 1, 0, 0)),
    (500, (0, 0, 1, 1, 1)),
    (5000, (0, 1, 1, 1, 0)),
    (5000, (0, 1, 0, 1, 1, 0)),
    (5000, (0, 1, 1, 0, 1, 0)),
    (5000, (0, 1, 1, 1, 1)),
    (5000, (1, 1, 1, 1, 0)),
    (5000, (1, 0, 1, 1, 1)),
    (5000, (1, 1, 1, 0, 1)),
    (5000, (1, 1, 0, 1, 1)),
    (50000, (0, 1, 1, 1, 1, 0)),
    (100000000, (1, 1, 1, 1, 1))
]

def ai():
    global  CUT
    global  SEARCH
    CUT = 0
    SEARCH = 0
    neg_max_search(-100000000, 100000000, True, DEPTH)
    print('剪枝数:', CUT)
    print('搜索数:', SEARCH )
    return next_step[0], next_step[1]

def neg_max_search(alpha, beta, is_ai, depth):
    if game_over(list_ai) or game_over(list_hu) or depth == 0:
        total_score = evaluate(is_ai)
        return total_score

    #计算空余位置的集合
    blank_list = list(set(list_all).difference(set(list_sum)))
    #按远近排序
    near_order(blank_list)
    for next in blank_list:
        global SEARCH
        SEARCH += 1
        if not has_neightnor(next):
            continue
        if is_ai:
            list_ai.append(next)
        else:
            list_hu.append(next)
        list_sum.append(next)

        value = -neg_max_search(-beta, -alpha, not is_ai, depth - 1)
        if is_ai:
            list_ai.remove(next)
        else:
            list_hu.remove(next)
        list_sum.remove(next)
        #下一层的值比这一层的最大值要大
        if value > alpha:
            #确定下一步要下的棋子的位置
            if depth == DEPTH:
                next_step[0] = next[0]
                next_step[1] = next[1]
            #下一层的值比这一层的最小值大，剪枝
            if value >= beta:
                global  CUT
                CUT += 1
                return beta
            alpha = value

    return alpha#得分的最大值


# 将上次落点周围的点放在前面
def near_order(list_blank):
    last = list_sum[-1] #最后一次的落点位置
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            elif (last[0] + x, last[1] + y) in list_blank:
                list_blank.remove((last[0] + x, last[1] + y))
                list_blank.insert(0, (last[0] + x, last[1] + y))#插入第一个

def has_neightnor(item):
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            elif(item[0] + x, item[1] + y) in list_sum:#有邻居
                return True
    return False

#评估函数
def evaluate(is_ai):
    #当前局面对于一方的的总得分值
    if is_ai:
        self_list = list_ai
        enemy_list = list_hu
    else:
        self_list = list_hu
        enemy_list = list_ai

    all_score_shape_direct = []
    self_score = 0 #自己当前局面的总分数
    for dot in self_list:
        x = dot[0]
        y = dot[1]
        self_score += calculate(x, y, 1, 0, self_list, enemy_list, all_score_shape_direct)
        self_score += calculate(x, y, 0, 1, self_list, enemy_list, all_score_shape_direct)
        self_score += calculate(x, y, 1, 1, self_list, enemy_list, all_score_shape_direct)
        self_score += calculate(x, y, 1, -1, self_list, enemy_list, all_score_shape_direct)


    enemy_all_score_shape_direct = []
    enemy_score = 0  # 自己当前局面的总分数
    for dot in enemy_list:
        x = dot[0]
        y = dot[1]
        enemy_score += calculate(x, y, 1, 0, enemy_list, self_list, enemy_all_score_shape_direct)
        enemy_score += calculate(x, y, 0, 1, enemy_list, self_list, enemy_all_score_shape_direct)
        enemy_score += calculate(x, y, 1, 1, enemy_list, self_list, enemy_all_score_shape_direct)
        enemy_score += calculate(x, y, 1, -1, enemy_list, self_list, enemy_all_score_shape_direct)

    #规则待改善
    total_score = self_score - enemy_score / 2
    return total_score


#计算某个点所在棋子形状的得分值
def calculate(x, y, direct_x, direct_y, self_list, enemy_list, all_score_shape_direct):
    extra_score = 0
    maxscore_shape = (0, None)

    #该点在此方向已经加入了某种形状的计算，不重复计算
    for item in all_score_shape_direct:
        if (x, y) in item[1] and direct_x == item[2][0] and direct_y == item[2][1]:
            return 0

    #在落点位置的[-5, 5]的范围内查找得分形状，偏移量-5到0范围内，遍历0到5
    for offset in range(-5, 1):
        shape = [] #记录每种偏移量时的形状
        for i in range(0, 6):
            #敌方棋子
            real_offset = i + offset
            if x + real_offset * direct_x < 0 or x + real_offset * direct_x > COLUMN or y + real_offset * direct_y < 0 or y + real_offset * direct_y > ROW:
                break#超出范围
            if (x + real_offset * direct_x, y + real_offset * direct_y) in enemy_list:
                shape.append(-1)
            #我方棋子
            elif(x + real_offset * direct_x, y + real_offset * direct_y) in self_list:
                shape.append(1)
            #空位
            else:
                shape.append(0)
        shape_len5_1 = None
        shape_len5_2 = None
        shape_len6 = None
        #将数组转化为元组
        if len(shape)== 5:
            shape_len5_1 = tuple(shape)
        elif len(shape) == 6:
            shape_len6 = tuple(shape)
            shape_len5_1 = tuple(shape[:5])
            shape_len5_2 = tuple(shape[1:])
        else:#长度小于5不能成功匹配
            continue
        score5 = 0
        score6 = 0
        for item in score_shape:
            if shape_len5_1 == item[1] or shape_len5_2 == item[1]:
                score5 = max(score5, item[0])
            if shape_len6 == item[1]:
                score6 = item[0]
        # 长度为5的棋子形状
        if score5 > 0 and score5 > score6 and score5 > maxscore_shape[0]:
            maxscore_shape = (
                score5,
                (
                    (x + (offset + 0) * direct_x, y + (offset + 0) * direct_y),
                    (x + (offset + 1) * direct_x, y + (offset + 1) * direct_y),
                    (x + (offset + 2) * direct_x, y + (offset + 2) * direct_y),
                    (x + (offset + 3) * direct_x, y + (offset + 3) * direct_y),
                    (x + (offset + 4) * direct_x, y + (offset + 4) * direct_y)
                ),
                (direct_x, direct_y)
            )
        # 长度为6的棋子形状
        elif score6 > 0 and score6 > score5 and score6 > maxscore_shape[0]:
            maxscore_shape = (
                score6,
                (
                    (x + (offset + 0) * direct_x, y + (offset + 0) * direct_y),
                    (x + (offset + 1) * direct_x, y + (offset + 1) * direct_y),
                    (x + (offset + 2) * direct_x, y + (offset + 2) * direct_y),
                    (x + (offset + 3) * direct_x, y + (offset + 3) * direct_y),
                    (x + (offset + 4) * direct_x, y + (offset + 4) * direct_y),
                    (x + (offset + 5) * direct_x, y + (offset + 5) * direct_y)
                ),
                (direct_x, direct_y)
            )
    #如果两个形状有相交的点，整个棋子的布局的得分增加
    if maxscore_shape[0] > 0:
        for item in all_score_shape_direct:
            for dot1 in item[1]:
                for dot2 in maxscore_shape[1]:
                    #活三以上级别的相交，也可以适当修改加分规则
                    if maxscore_shape[0] >= 100 and item[0] >= 100 and dot1 == dot2:
                        #额外获得加分相当于相交的两个个自得分加倍
                        extra_score += item[0] + maxscore_shape[0]
        #将maxscore_shape加入all_score_shape_direct
        all_score_shape_direct.append(maxscore_shape)
    return extra_score + maxscore_shape[0]

#游戏结束
def game_over(list):
    for col in range(COLUMN + 1):
        for row in range(ROW + 1):
            if row < ROW - 3 and (col, row) in list and (col, row + 1) in list and (col, row + 2) in list\
            and (col, row + 3) in list and (col, row + 4) in list:
                return True
            elif col < COLUMN - 3 and row < ROW - 3 and (col, row) in list and (col + 1, row + 1) in list and (col + 2, row + 2) in list\
            and (col + 3, row + 3) in list and (col + 4, row + 4) in list:
                return True
            elif col < COLUMN - 3 and row > 3 and (col, row) in list and (col + 1, row - 1) in list and (col + 2, row - 2) in list\
            and (col + 3, row - 3) in list and (col + 4, row - 4) in list:
                return True
            elif col < COLUMN - 3 and (col, row) in list and (col + 1, row) in list and (col + 2, row) in list\
            and (col + 3, row) in list and (col + 4, row) in list:
                return True
    return False

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
                if game_over(list_ai):
                    print('ai win')
                    break
                if game_over(list_hu):
                    print('human win')
                    break

                if ai_turn:
                    col, row =ai()
                    if not (col, row) in list_sum:
                        x = int((col + 1 / 2) * WIDTH)
                        y = int((row + 1 / 2) * WIDTH)
                        pg.draw.circle(gobang, (255, 255, 255), (x, y), 15, 0)
                        pg.display.flip()
                        ai_turn = False
                        list_ai.append((col, row))
                        list_sum.append((col, row))


                else:
                    pg.event.wait()
                    if pg.mouse.get_pressed()[0] == 1:
                        x, y = pg.mouse.get_pos()
                        col = math.floor(x / WIDTH)
                        row = math.floor(y / WIDTH)
                        if not (col, row) in list_sum:
                            x = int((col + 1 / 2) * WIDTH)
                            y = int((row + 1 / 2) * WIDTH)
                            pg.draw.circle(gobang, (0, 0, 0), (x, y), 15, 0)
                            pg.display.flip()
                            ai_turn = True
                            list_hu.append((col, row))
                            list_sum.append((col, row))










if __name__ == '__main__':
    main()