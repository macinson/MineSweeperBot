import pyautogui
import time
import random
import keyboard
import numpy as np

game_h = 9
game_w = 9
mines = 99

init_x = 990
init_y = 350
side_width = 32

lose_pixel = (1108,293)
lose_color = (111,111,37)

tile_gray = (188,188,189)

def click_randomly(board):
    available_tiles = np.argwhere(board==-1)
    tile = random.choice(available_tiles)
    rand_x = init_x + side_width * tile[0]
    rand_y = init_y + side_width * tile[1]
    pyautogui.click(rand_x, rand_y)

def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0
    # pull up the window
    pyautogui.getWindowsWithTitle("Minesweeper Online")[0].maximize()

    board = np.full((game_w, game_h), -1)
    start_time = time.time()

    while not keyboard.is_pressed('q') and time.time() < start_time + 240:
        if pyautogui.pixel(lose_pixel[0], lose_pixel[1]) == lose_color:
            pyautogui.click(lose_pixel[0], lose_pixel[1])
            board = np.full((game_w, game_h), -1)
        click_randomly(board)
        # to see what's happening
        # time.sleep(1)

if __name__ == "__main__":
    main()