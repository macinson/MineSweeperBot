import pyautogui
import time
import random
import keyboard

game_h = 9
game_w = 9
mines = 99

init_x = 780
init_y = 360
side_width = 35

# pull up the window
pyautogui.getWindowsWithTitle("Minesweeper Online")[0].maximize()

def click_randomly():
    rand_x = init_x + side_width * random.randint(0, game_w-1)
    rand_y = init_y + side_width *random.randint(0, game_h-1)
    pyautogui.click(rand_x, rand_y)

start_time = time.time()

while not keyboard.is_pressed('q') and time.time() < start_time + 240:
    if pyautogui.pixel(914,303) == (139,140,47):
        pyautogui.click(920, 280)
    click_randomly()