import pyautogui
import time
from pynput import keyboard
import random

# Coordinates to click
spot1 = (3050, 1290)
spot2 = (2347, 1090)
upperleft = (1540, 330)
lowerright = (3158, 1121)

stop_flag = False

def on_press(key):
    global stop_flag
    try:
        if key.char == 'q':
            stop_flag = True
            return False  # Stop listener
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Clicking... Press 'q' to stop.")

while not stop_flag:
    pyautogui.click(spot1)
    pyautogui.click(spot2)
    pyautogui.click()
    time.sleep(0.01)

print("Stopped.")
