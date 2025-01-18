import pyautogui
import time
import random

def clickMouse(x, y):
    pyautogui.moveTo(x+(random.random()*4)-2, y+(random.random()*4)-2, 0.5+random.random(), pyautogui.easeOutQuad)
    pyautogui.click()

while True:
    if(not pyautogui.pixelMatchesColor(1649, 1033, (244, 244, 244))):
        clickMouse(955, 752)
        time.sleep(1)
        clickMouse(294,199)
        time.sleep(5)
        clickMouse(268, 317)
        clickMouse(913, 456)
        time.sleep(10)
        clickMouse(955, 752)
        time.sleep(1)
        clickMouse(955, 752)
        time.sleep(10)
        clickMouse(955, 752)
        time.sleep(2)
        for i in range(0, 10):
            clickMouse(1235, 1049)
        clickMouse(1651, 902)
        time.sleep(5)
        clickMouse(1514, 1049)
        clickMouse(1509, 963)
        clickMouse(1649, 1033)
    time.sleep(1)