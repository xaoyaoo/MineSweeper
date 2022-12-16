import sys

sys.path.append(".")
from MineSweeper.game import *
from mineAI import AI

pygame.init()
pygame.display.set_caption("扫雷")
start_game(BLOCK_WIDTH, BLOCK_HEIGHT, MINE_COUNT)
draw_init()

ai = AI()
set_global()
BLOCK_HEIGHT = 5  # 格子高度
BLOCK_WIDTH = 5  # 格子宽度
# 地雷数
MINE_COUNT = 2

while True:
    event_handler()
    pygame.display.update()
    map, map_flag, game_display, MINE_COUNT, BLOCK_WIDTH, BLOCK_HEIGHT, game_state, x_start, y_start, img_size, DISPLAY_WIDTH, DISPLAY_HEIGHT, start_time, end_time, change, mine, normal, bomb, flag, ask, unflag, opened, win_flag = get_global()
    pargs = (map, map_flag, game_display, MINE_COUNT, BLOCK_WIDTH, BLOCK_HEIGHT, game_state, x_start, y_start, img_size, DISPLAY_WIDTH, DISPLAY_HEIGHT, start_time, end_time, change, mine, normal, bomb, flag, ask, unflag, opened, win_flag)
    if end_time - start_time >= 0 and end_time - start_time < 0.2:
        ai.init(*pargs)
    if end_time - start_time >= 0 and (game_state == 1 or game_state == 0):
        ai.run(map_flag)
