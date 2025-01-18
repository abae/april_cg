import time
import pyautogui
import sys

tmfPos = (656, 844)
stakePos = (1593, 667)
orange = (238, 125, 58)

loop = 0

if __name__ == "__main__":
    while loop < int(sys.argv[1]):
        loop += 1
        while not pyautogui.pixelMatchesColor(tmfPos[0], tmfPos[1], orange, tolerance=1) or not pyautogui.pixelMatchesColor(stakePos[0], stakePos[1], orange, tolerance=1):
            time.sleep(1)
        time.sleep(2)
        pyautogui.click(tmfPos[0], tmfPos[1])
        pyautogui.click(stakePos[0], stakePos[1])
        print(f"Loop: {loop}/{sys.argv[1]}")
        time.sleep(20)