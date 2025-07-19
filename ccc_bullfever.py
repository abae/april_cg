import pyautogui
import time
from pynput import keyboard
import random

# Coordinates to click
spot1 = (1450, 925)
spot2 = (950, 790)

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

loop = 5000
while not stop_flag and loop >= 0:
    pyautogui.click(spot1)
    pyautogui.click(spot2)
    pyautogui.click()
    time.sleep(0.01)
    loop = loop - 1
    print(loop)

print("Stopped.")
