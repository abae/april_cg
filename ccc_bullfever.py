import pyautogui
import time
from pynput import keyboard
import pyautogui
import sys


# Coordinates to click
spot1 = (3050, 1290)
spot2 = (2347, 1090)
upperleft = (1540, 330)
lowerright = (3158, 1170)

minutes = sys.argv[1]
end_time = time.time() + int(minutes) * 60

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

while not stop_flag and time.time() < end_time:
    try:
        image_location = pyautogui.locateCenterOnScreen('data/coin.png',region=(upperleft[0], upperleft[1], lowerright[0] - upperleft[0], lowerright[1] - upperleft[1]), confidence=0.8)
        if image_location:
            pyautogui.click(image_location)
    except:
        pyautogui.click(spot1)
        pyautogui.click(spot2)
        pyautogui.click()

print("Stopped.")
