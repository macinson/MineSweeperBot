import os
# import threading
from functools import partial

import pyautogui
import time
import random
import keyboard
import numpy as np

side_width = 32
MARKER = 99

lose_pixel = (18, 35)

win_pixel = (27, 20)

number_offset = (19, 24)
unclicked_offset = (29, 29)

smiley_yellow = (253, 254, 85)

unclicked_gray = (122, 122, 123)

### board-specific settings

game_h = 16
game_w = 30
mines = 99

# init = (972,336)
init = (952,336)

# game_button = (1090,258)
# game_button = (1202,258)
game_button = (1406,258)

# game_size = (1290 - 940, 650 - 230)
# game_size = (1940 - 940, 870 - 230)
game_size = (1912 - 940, 847 - 230)

def click_randomly(board):
    available_tiles = np.argwhere(board == -1)
    tile = random.choice(available_tiles)
    rand_x = init[0] + side_width * tile[0]
    rand_y = init[1] + side_width * tile[1]
    pyautogui.click(rand_x, rand_y)

def educated_click(board):
    safe_tiles = np.argwhere(board == -2)
    available_tiles = np.argwhere(np.logical_or(board == -1, board == -2))
    if safe_tiles.size > 0:
        for tile in safe_tiles:
            x = init[0] + side_width * tile[0]
            y = init[1] + side_width * tile[1]
            pyautogui.click(x, y)
    else:
        tile = random.choice(available_tiles)
        x = init[0] + side_width * tile[0]
        y = init[1] + side_width * tile[1]
        pyautogui.click(x, y)
    time.sleep(0.05)
    sc = pyautogui.screenshot(region=(init[0], init[1], game_size[0], game_size[1]))
    np.apply_along_axis(partial(update_tile, sc=sc, board=board), 1, available_tiles)

    # place flags on our board
    place_flags(board)
    # identify no-bomb spots
    update_board(board)


def update_tile(t, sc, board):
    x = side_width * t[0]
    y = side_width * t[1]
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

def place_flags(board):
    tiles = np.argwhere(np.logical_and(board >= 1, board <= 8))
    for tile in tiles:
        temp = board[tile[0]][tile[1]]
        board[tile[0]][tile[1]] = MARKER
        neighbours = board[tile[0]-1 : tile[0]+2, tile[1]-1 : tile[1]+2]
        center = np.argwhere(neighbours == MARKER)
        board[tile[0]][tile[1]] = temp
        possible_bombs = np.argwhere(np.logical_or(neighbours == -1, neighbours == 9))

        if possible_bombs.shape[0] == board[tile[0]][tile[1]]:
            for t in possible_bombs:
                board[tile[0] + t[0] - center[0][0]][tile[1] + t[1]- center[0][1]] = 9

def update_board(board):
    tiles = np.argwhere(np.logical_and(board >= 1, board <= 8))
    for tile in tiles:
        temp = board[tile[0]][tile[1]]
        board[tile[0]][tile[1]] = MARKER
        neighbours = board[tile[0] - 1: tile[0] + 2, tile[1] - 1: tile[1] + 2]
        center = np.argwhere(neighbours == MARKER)
        board[tile[0]][tile[1]] = temp
        bombs = np.argwhere(neighbours == 9)
        unknown_tiles = np.argwhere(neighbours == -1)

        if bombs.shape[0] == board[tile[0]][tile[1]]:
            for t in unknown_tiles:
                board[tile[0] + t[0] - center[0][0]][tile[1] + t[1]- center[0][1]] = -2

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
    pyautogui.click(game_button[0], game_button[1])
    board = np.full((game_w, game_h), -1)
    start_time = time.time()

    while not keyboard.is_pressed('q') and time.time() < start_time + 600:
        if pyautogui.pixel(game_button[0] + win_pixel[0], game_button[1] + win_pixel[1]) != smiley_yellow:
            break
        if pyautogui.pixel(game_button[0] + lose_pixel[0], game_button[1] + lose_pixel[1]) != smiley_yellow:
            pyautogui.click(game_button[0], game_button[1])
            board = np.full((game_w, game_h), -1)
            time.sleep(0.1)
        educated_click(board)
        # to see what's happening
        # time.sleep(1)


if __name__ == "__main__":
    main()
