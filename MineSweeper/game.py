# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         t2.py
# Description:  
# Author:       xaoyaoo
# Date:         2022/12/15
# -------------------------------------------------------------------------------
import os
import random
import time

import numpy as np
import pygame
from pygame.locals import *

# 地雷
mine = 9
# 未点击
normal = -1

bomb = 12

# 标记为地雷
flag = 10
# 标记为问号
ask = 11
# 未标记
unflag = 13
# 已点击
opened = 0

game_state = 0  # 游戏状态 0未开始 1第一轮 -1结束 2即将结束
x_start = 10  # 起始位置 格子
y_start = 10 + 80  # 起始位置 格子
img_size = 24  # 单个格子大小

# 游戏计时
start_time = time.time()
end_time = time.time()
win_flag = False

map = np.full((1, 1), -1)  # 地图 0-8表示周围有0-8个地雷 9表示地雷
# 地图标记  10表示标记为地雷 11表示标记为问号 12表示未标记 opened表示已点击 unflag表示未点击
map_flag = np.full((1, 1), -1)
change = []  # 改变的格子 用于刷新 使用前清空
# 字体路径
root_path = r"D:\_code\python_test\test\20221215扫雷\MineSweeper"
font_path = root_path + r"\font\consola.ttf"


# 创建空白地图 m行 n列
def create_map(m, n):
    # 创建地图
    global map
    map = np.full((m, n), -1)
    global map_flag
    map_flag = np.full((m, n), unflag)
    return map


# 获取周围地雷数
def get_around_mine_count(x, y):
    global map
    count = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if i >= 0 and i < map.shape[0] and j >= 0 and j < map.shape[1] and map[i][j] == mine and (i != y or j != x):
                count += 1
    return count


# 随机生成地雷，保证第一次点击不是地雷 第一次点击运行
def set_mine_random(x, y):
    global map
    global MINE_COUNT
    m, n = map.shape[0], map.shape[1]
    if MINE_COUNT > m * n - 9:
        MINE_COUNT = m * n - 9
    xs = np.arange(n)
    ys = np.arange(m)
    xys = np.array(np.meshgrid(xs, ys)).T.reshape(-1, 2)
    del_index = np.where((xys[:, 0] >= x - 1) & (xys[:, 0] <= x + 1) & (xys[:, 1] <= y + 1) & (xys[:, 1] >= y - 1))[0]
    xys = np.delete(xys, del_index, axis=0)
    np.random.shuffle(xys)  # 打乱顺序
    for j, i in xys[0:MINE_COUNT]:
        map[i][j] = mine
    for i in range(m):
        for j in range(n):
            if map[i][j] != mine:
                map[i][j] = get_around_mine_count(j, i)


# 游戏结束判定
def is_game_over(x, y):
    global game_state
    global map
    global map_flag
    global win_flag

    if map[y][x] == mine:
        print("踩雷了~")
        map[y][x] = bomb
        game_state = 2
        return True
    # 判断是否胜利
    opened_map = np.where(map_flag == opened, 1, 0)
    if np.where(map_flag == opened, 1, 0).sum() == map.shape[0] * map.shape[1] - MINE_COUNT:
        print("你赢啦!")
        game_state = 2
        win_flag = True
        return True


# 翻开点击的格子
def open_block(x, y):
    global map
    global map_flag
    global change
    map_flag[y][x] = opened
    # 翻开周围的格子
    if is_game_over(x, y):
        print("游戏结束!")
        return
    else:
        # 改变的格子
        map[y][x] = get_around_mine_count(x, y)
        change.append([x, y, map[y][x]])

        if map[y][x] == 0:  # 如果周围没有地雷，继续翻开周围的格子
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if i >= 0 and i < map.shape[0] and j >= 0 and j < map.shape[1] and map_flag[i][j] == unflag:
                        open_block(j, i)


# 标记为地雷
def set_flag(x, y):
    global map_flag
    if map_flag[y][x] == flag:
        map_flag[y][x] = ask
    elif map_flag[y][x] == ask:
        map_flag[y][x] = unflag
    elif map_flag[y][x] == unflag:
        map_flag[y][x] = flag
    return map_flag[y][x]


def start_game(block_width, block_height, mine_count):
    global game_state
    global map
    global map_flag
    global start_time
    global end_time
    global MINE_COUNT
    global x_start
    global y_start
    global BLOCK_WIDTH
    global BLOCK_HEIGHT
    global win_flag

    BLOCK_WIDTH = block_width
    BLOCK_HEIGHT = block_height
    MINE_COUNT = mine_count

    # 游戏状态 0未开始 1进行中 2结束
    game_state = 0
    win_flag = False
    # 地雷数量
    # 游戏计时
    start_time = time.time()
    end_time = time.time()
    # 创建地图
    create_map(BLOCK_HEIGHT, BLOCK_WIDTH)


def draw_title():
    global game_display
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    font = pygame.font.SysFont(font_path, 35)
    text_title = font.render("Mine Sweeper", True, (0, 0, 0))
    centerTitle = text_title.get_rect(center=(DISPLAY_WIDTH / 2, 20))
    game_display.blit(text_title, centerTitle)


def draw_time_mine_num(use_time, mine_num):
    global game_display
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    # 填充即将显示文字地方为背景
    pygame.draw.rect(game_display, (248, 244, 244), (0, 35, DISPLAY_WIDTH, 35))
    # 显示用时
    # 判断文件是否存在
    font = pygame.font.Font(font_path, 20)
    text = "time:" + str(use_time)
    text_title = font.render(text, True, (0, 0, 0))
    centerTitle = text_title.get_rect(center=(DISPLAY_WIDTH / 4, 20 + 35))  # 居中
    game_display.blit(text_title, centerTitle)
    # 显示剩余地雷数
    text = "mine:" + str(mine_num)
    text_title = font.render(text, True, (0, 0, 0))
    centerTitle = text_title.get_rect(center=(DISPLAY_WIDTH / 4 * 3, 20 + 35))  # 居中
    game_display.blit(text_title, centerTitle)
    return game_display


def draw_img(id, width=16, height=16):
    global map
    img = pygame.image.load(root_path + "/img/" + str(id) + ".bmp")
    img = pygame.transform.scale(img, (width, height))  # 缩放图片
    return img


def draw_block(x, y, id):
    global map
    global map_flag
    global game_state
    global game_display
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    global img_size

    pygame.draw.rect(game_display, (248, 244, 244),
                     (x * img_size + x_start, y * img_size + y_start, img_size, img_size))
    img = draw_img(id, width=img_size, height=img_size)
    game_display.blit(img, (x * img_size + x_start, y * img_size + y_start))


# 绘制全部格子
def draw_all_block():
    global map
    global map_flag
    global img_size
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map_flag[i][j] == opened:
                draw_block(j, i, map[i][j])
            elif map_flag[i][j] == flag:
                draw_block(j, i, 10)
            elif map_flag[i][j] == ask:
                draw_block(j, i, 11)
            elif map_flag[i][j] == unflag:
                draw_block(j, i, 13)


# 绘制初始界面
def draw_init(MIN_WIDTH=500, MIN_HEIGHT=300):
    # 界面宽高
    global img_size  # 单个格子大小
    global x_start  # 起始位置
    global y_start  # 起始位置
    global DISPLAY_WIDTH  # 窗口宽度
    global DISPLAY_HEIGHT  # 窗口高度
    global game_display  # 窗口
    global map  # 地图
    global map_flag  # 地图标记
    global MINE_COUNT  # 地雷数量
    BLOCK_WIDTH, BLOCK_HEIGHT = map.shape[1], map.shape[0]

    DISPLAY_WIDTH = BLOCK_WIDTH * img_size + 20 if BLOCK_WIDTH * img_size + 20 + 80 > MIN_WIDTH else MIN_WIDTH
    DISPLAY_HEIGHT = BLOCK_HEIGHT * img_size + 20 + 80 if BLOCK_HEIGHT * img_size + 20 + 80 > MIN_HEIGHT else MIN_HEIGHT
    if DISPLAY_WIDTH == MIN_WIDTH:
        x_start = (DISPLAY_WIDTH - BLOCK_WIDTH * img_size) / 2
    if DISPLAY_HEIGHT == MIN_HEIGHT:
        y_start = (DISPLAY_HEIGHT - 80 - BLOCK_HEIGHT * img_size) / 2 + 80

    # 初始化界面
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    game_display.fill((248, 244, 244))
    draw_title()  # 绘制标题
    draw_time_mine_num(get_use_time(), MINE_COUNT)  # 绘制时间和地雷数
    draw_all_block()  # 绘制全部格子


def draw_game_over():  # 绘制游戏结束界面
    global game_display
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    global map
    global map_flag
    global img_size
    global x_start
    global y_start
    global MINE_COUNT

    flag_num = np.where(map_flag == flag)[0].size
    draw_time_mine_num(get_use_time(), MINE_COUNT - flag_num)  # 绘制时间和地雷数

    font = pygame.font.Font(font_path, 30)
    text = "game over!"
    if win_flag: text = "you win!"
    text_title = font.render(text, True, (255, 0, 0))
    centerTitle = text_title.get_rect(center=(DISPLAY_WIDTH / 2, 20 + 40))  # 居中
    game_display.blit(text_title, centerTitle)

    draw_all_block()
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map_flag[i][j] == flag:
                if map[i][j] != mine:
                    draw_block(j, i, 12)
                else:
                    draw_block(j, i, 9)
            elif map_flag[i][j] == ask:
                if map[i][j] == mine:
                    draw_block(j, i, "ask2")
                else:
                    draw_block(j, i, 14)
            elif map_flag[i][j] == unflag:
                if map[i][j] == mine and not win_flag:
                    draw_block(j, i, 14)
                elif map[i][j] == mine:
                    draw_block(j, i, map[i][j])


def get_use_time():
    global start_time
    global end_time
    global game_state
    if game_state == 0:
        return 0
    elif game_state == -1 or game_state == 2:
        return int(end_time - start_time)
    else:
        end_time = time.time()
        return int(end_time - start_time)


def event_handler():  # 事件处理
    global map
    global map_flag
    global game_display
    global MINE_COUNT
    global BLOCK_WIDTH
    global BLOCK_HEIGHT
    global game_state
    global x_start
    global y_start
    global img_size
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    global start_time
    global end_time
    global change
    if game_state == 0:  # 游戏未开始
        draw_init()
        start_time = time.time()
        end_time = time.time()
    if game_state == 2:  # 游戏结束
        game_state = -1
        end_time = time.time()
        draw_game_over()
    # 事件处理
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE)):
            pygame.quit()
            quit()
        if event.type == MOUSEBUTTONDOWN:  # 鼠标点击事件
            x1, y1 = event.pos
            if x1 > x_start and x1 < (x_start + BLOCK_WIDTH * img_size) and y1 > y_start and y1 < (
                    y_start + BLOCK_HEIGHT * img_size):
                x = int((x1 - x_start) / img_size)
                y = int((y1 - y_start) / img_size)
                if event.button == 1:  # 左键
                    if game_state == 0:  # 游戏未开始
                        set_mine_random(x, y)  # 初始化地雷
                        game_state = 1  # 游戏开始
                        start_time = time.time()

                        change = []  # 用于记录改变的格子
                        open_block(x, y)
                        for xy in change:
                            draw_block(xy[0], xy[1], xy[2])  # 绘制改变的格子
                    elif game_state == 1:
                        if map_flag[y][x] == flag or map_flag[y][x] == ask:
                            pass
                        else:
                            change = []  # 用于记录改变的格子
                            open_block(x, y)
                            for xy in change:
                                # print(map[xy[1]][xy[0]])
                                draw_block(xy[0], xy[1], xy[2])  # 绘制改变的格子
                elif event.button == 3:
                    if game_state == 1:
                        tm = set_flag(x, y)
                        draw_block(x, y, tm)
                elif event.button == 2:
                    print("鼠标中键")
                    print(x, y)
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                print("空格键")
            elif event.key == K_RETURN:
                print("回车键")
            elif event.key == K_r:
                print("")
                print("重新开始")
                start_game(BLOCK_WIDTH, BLOCK_HEIGHT, MINE_COUNT)
    if game_state == 1:
        end_time = time.time()
        flag_num = np.where(map_flag == flag)[0].size
        draw_time_mine_num(get_use_time(), MINE_COUNT - flag_num)  # 绘制时间和地雷数


# 将全局变量设为函数
def set_global():
    global map
    global map_flag
    global game_display
    global MINE_COUNT
    global BLOCK_WIDTH
    global BLOCK_HEIGHT
    global game_state
    global x_start
    global y_start
    global img_size
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    global start_time
    global end_time
    global change
    # 地雷
    global mine
    # 未点击
    global normal
    global bomb
    # 标记为地雷
    global flag
    # 标记为问号
    global ask
    # 未标记
    global unflag
    # 已点击
    global opened
    # 游戏计时
    global win_flag



def get_global():
    global map
    global map_flag
    global game_display
    global MINE_COUNT
    global BLOCK_WIDTH
    global BLOCK_HEIGHT
    global game_state
    global x_start
    global y_start
    global img_size
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    global start_time
    global end_time
    global change
    # 地雷
    global mine
    # 未点击
    global normal
    global bomb
    # 标记为地雷
    global flag
    # 标记为问号
    global ask
    # 未标记
    global unflag
    # 已点击
    global opened
    # 游戏计时
    global win_flag
    return map, map_flag, game_display, MINE_COUNT, BLOCK_WIDTH, BLOCK_HEIGHT, game_state, x_start, y_start, img_size, DISPLAY_WIDTH, DISPLAY_HEIGHT, start_time, end_time, change, mine, normal, bomb, flag, ask, unflag, opened, win_flag


DISPLAY_WIDTH = 10  # 宽度
DISPLAY_HEIGHT = 5  # 高度

BLOCK_HEIGHT = 16  # 格子高度
BLOCK_WIDTH = 30  # 格子宽度
# 地雷数
MINE_COUNT = 20
