import pyautogui
from time import sleep

sleep(2)
while (not pyautogui.pixelMatchesColor(2426, 1135, (169, 98, 32), tolerance=5)):
    sleep(0.1)
pyautogui.click()
