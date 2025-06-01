import os
# import threading
from functools import partial

import pyautogui
import time
import random
import keyboard
import numpy as np

game_h = 9
game_w = 9
mines = 99

init_x = 972
init_y = 336
side_width = 32

lose_pixel = (1108, 293)

win_pixel = (1117, 278)

number_offset = (19, 24)
unclicked_offset = (29, 29)

smiley_yellow = (253, 254, 85)

unclicked_gray = (122, 122, 123)


def click_randomly(board):
    available_tiles = np.argwhere(board == -1)
    tile = random.choice(available_tiles)
    rand_x = init_x + side_width * tile[0]
    rand_y = init_y + side_width * tile[1]
    pyautogui.click(rand_x, rand_y)
    time.sleep(0.05)
    sc = pyautogui.screenshot(region=(940, 230, 1290 - 940, 650 - 230))
    np.apply_along_axis(partial(update_tile, sc=sc, board=board), 1, available_tiles)


def update_tile(t, sc, board):
    x = init_x + side_width * t[0] - 940
    y = init_y + side_width * t[1] - 230
    if sc.getpixel((int(x) + unclicked_offset[0], int(y) + unclicked_offset[1])) != unclicked_gray:
        if sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (0, 0, 244):
            board[t[0]][t[1]] = 1
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (52, 121, 32):
            board[t[0]][t[1]] = 2
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (232, 45, 35):
            board[t[0]][t[1]] = 3
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (0, 0, 118):
            board[t[0]][t[1]] = 4
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (111, 16, 11):
            board[t[0]][t[1]] = 5
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (52,121,122):
            board[t[0]][t[1]] = 6
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (47,47,47):
            board[t[0]][t[1]] = 7
        elif sc.getpixel((int(x) + number_offset[0], int(y) + number_offset[1])) == (122,122,123):
            board[t[0]][t[1]] = 8
        else:
            board[t[0]][t[1]] = 0


def exit():
    while True:
        if keyboard.is_pressed('q'):
            os._exit(0)


def main():
    # escape thread
    # esc = threading.Thread(target=exit)
    # esc.daemon = True
    # esc.start()

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0
    # pull up the window
    pyautogui.getWindowsWithTitle("Minesweeper Online")[0].maximize()

    time.sleep(1)

    # reset board
    pyautogui.click(lose_pixel[0], lose_pixel[1])
    board = np.full((game_w, game_h), -1)
    start_time = time.time()

    while not keyboard.is_pressed('q') and time.time() < start_time + 600:
        if pyautogui.pixel(win_pixel[0], win_pixel[1]) != smiley_yellow:
            break
        if pyautogui.pixel(lose_pixel[0], lose_pixel[1]) != smiley_yellow:
            pyautogui.click(lose_pixel[0], lose_pixel[1])
            board = np.full((game_w, game_h), -1)
            time.sleep(0.1)
        click_randomly(board)
        print(board.T)
        # to see what's happening
        # time.sleep(1)


if __name__ == "__main__":
    main()
