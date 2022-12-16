# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         扫雷算法.py
# Description:  
# Author:       xaoyaoo
# Date:         2022/12/15
# -------------------------------------------------------------------------------
import random
import time

import numpy as np
import win32gui
import win32con
import win32api

import pyautogui


# from .MineSweeper.game import *


def get_window_pos(class_name, title_name):
    """
    获取窗口位置
    :param hwnd:
    :return:
    """
    hwnd = win32gui.FindWindow(class_name, title_name)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return left, top, right, bottom
    else:
        return None


def mouse_click(x, y, button=1):
    """
    鼠标点击
    :param x:
    :param y:
    :return:
    """
    win32api.SetCursorPos((x, y))
    if button == 1:
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

        pyautogui.click(x, y, button='left')  # 单击左键
    elif button == 3:
        # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

        pyautogui.click(x, y, button='right')  # 单击右键
    elif button == 2:
        # win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
        pyautogui.click(x, y, button='middle')  # 单击中间


class AI:
    """
    扫雷算法
    :param map:
    :param map_flag:
    :return:
    """

    # 1. 扫雷算法
    # 2. 鼠标点击
    # 3. 递归
    def __init__(self):
        pass

    def init(self, map, map_flag, game_display, MINE_COUNT, BLOCK_WIDTH, BLOCK_HEIGHT, game_state, x_start, y_start,
             img_size, DISPLAY_WIDTH, DISPLAY_HEIGHT, start_time, end_time, change, mine, normal, bomb, flag, ask,
             unflag, opened, win_flag):
        self.map = map
        self.map_flag = map_flag
        self.game_display = game_display
        self.MINE_COUNT = MINE_COUNT
        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.BLOCK_HEIGHT = BLOCK_HEIGHT
        self.game_state = game_state
        self.x_start = x_start
        self.y_start = y_start
        self.img_size = img_size
        self.DISPLAY_WIDTH = DISPLAY_WIDTH
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.start_time = start_time
        self.end_time = end_time
        self.change = change
        self.mine = mine
        self.normal = normal
        self.bomb = bomb
        self.flag = flag
        self.ask = ask
        self.unflag = unflag
        self.opened = opened
        self.win_flag = win_flag

        self.block_pos = np.full((map.shape[0], map.shape[1], 2), -1)
        self.my_map = np.full((map.shape[0], map.shape[1]), -1)
        self.get_block_pos(self.map)

    # 获取格子位置
    def get_block_pos(self, map):
        """
        获取格子位置
        :return:
        """
        left, top, right, bottom = get_window_pos("pygame", "扫雷")
        left = left + 8
        top = top + 32
        right = right - 8
        bottom = bottom - 8
        display_width = right - left
        display_height = bottom - top

        m, n = map.shape[0], map.shape[1]
        block_width = n * self.img_size
        block_height = m * self.img_size

        block_left = left + (display_width - block_width) // 2
        block_top = top + (display_height - block_height - 80) // 2 + 80

        for i in range(m):
            for j in range(n):
                self.block_pos[i, j, 0] = block_left + j * self.img_size + self.img_size // 2
                self.block_pos[i, j, 1] = block_top + i * self.img_size + self.img_size // 2

    def click(self, i, j, button=1):
        """
        点击
        :param i:
        :param j:
        :return:
        """
        x, y = self.block_pos[i, j]
        mouse_click(x, y, button)
        print("点击", i, j, button)
        # time.sleep(0.5)

    # 获取周围的格子
    def get_around_block(self, x, y):
        """
        获取周围的格子
        :param x:
        :param y:
        :return:
        """
        m, n = self.map.shape[0], self.map.shape[1]
        around_block = []
        for i in range(max(0, y - 1), min(m, y + 2)):
            for j in range(max(0, x - 1), min(n, x + 2)):
                if i != y or j != x:
                    around_block.append((j, i))
        return around_block

    # 获取周围未点开的格子
    def get_around_mine_count(self, x, y):
        map = self.my_map
        count = 0
        flag_count = 0
        for j, i in self.get_around_block(x, y):
            if map[i, j] not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                count += 1
            if map[i, j] == self.flag:
                flag_count += 1
        return count, flag_count

    def run(self, map_flag):
        self.map_flag = map_flag
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map_flag[i, j] == self.opened:
                    self.my_map[i, j] = self.map[i, j]
                elif self.map_flag[i, j] == self.flag:
                    self.my_map[i, j] = self.flag
                elif self.map_flag[i, j] == self.unflag:
                    self.my_map[i, j] = self.unflag
                elif self.map_flag[i, j] == self.ask:
                    self.my_map[i, j] = self.ask
                else:
                    self.my_map[i, j] = -1
        if np.sum(self.my_map) == self.unflag * self.my_map.shape[0] * self.my_map.shape[1]:
            # 随机点开一个格子】
            i = random.randint(0, self.map.shape[0] - 1)
            j = random.randint(0, self.map.shape[1] - 1)
            self.click(i, j, 1)
            return
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):  # 逐个扫描
                count, flag_count = self.get_around_mine_count(j, i)  # 获取周围未点开的格子，以及周围旗子的数量
                # print(i, j, count, flag_count, self.my_map[i, j])
                if self.my_map[i, j] == count:  # 如果周围未点开的格子数量等于周围旗子的数量
                    for x, y in self.get_around_block(j, i):  # 遍历周围的格子
                        if self.my_map[y, x] == self.unflag:  # 如果格子是未点开的
                            self.click(y, x, 3)  # 标记旗子
                            return
                elif self.my_map[i, j] == flag_count:  # 如果周围旗子的数量等于格子上的数字
                    for x, y in self.get_around_block(j, i):  # 遍历周围的格子
                        if self.my_map[y, x] == self.unflag:  # 如果格子是未点开的
                            self.click(y, x, 1)
                            return
                elif self.my_map[i, j] == self.ask:
                    self.click(i, j, 3)
                    return
