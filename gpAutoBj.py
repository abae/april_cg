import cv2
from skimage.metrics import structural_similarity as ssim
import os
import pyscreenshot as ImageGrab
import time
import pyautogui
import numpy as np
import random
import sys
from PIL import Image
import easyocr
import datetime
import yagmail

playerPos = (876, 616)
playerPosR = tuple(np.subtract(playerPos, (181, 6)))
playerPosL = tuple(np.subtract(playerPos, (-150, 6)))
dealerPos = (874, 238)
hitPos = (649, 993)
standPos = (383, 991)
splitPos = (580, 870)
doublePos = (329, 866)
replayPos = standPos
insurancePos = (1052, 645)
handWidth = 250
handHeight = 220

redCol = (236, 33, 43)
redCol2 = (164, 30, 35)
redCol3 = (210, 138, 142)
grayCol = (157, 157, 157)
grayCol2 = (118, 118, 118)
grayCol3 = (39, 39, 39)

splitStatus = ['none']

loop = 0
notify_cycle = 100
target_cycle = notify_cycle

image_contrast_alpha = 7.0
image_contrast_beta = -80.0

debug = True

allowed_chars = "0123456789JQKA"

# strat tables 0 = hit, 1 = stand, 2 = split, 3 = double/hit, 4 = double/stand
hardStrat = [
    [0,0,0,0,0,0,0,0,0,0], # 5
    [0,0,0,0,0,0,0,0,0,0], # 6
    [0,0,0,0,0,0,0,0,0,0], # 7
    [0,0,0,0,0,0,0,0,0,0], # 8
    [0,3,3,3,3,0,0,0,0,0], # 9
    [3,3,3,3,3,3,3,3,0,0], # 10
    [3,3,3,3,3,3,3,3,0,0], # 11
    [0,0,1,1,1,0,0,0,0,0], # 12
    [1,1,1,1,1,0,0,0,0,0], # 13
    [1,1,1,1,1,0,0,0,0,0], # 14
    [1,1,1,1,1,0,0,0,0,0], # 15
    [1,1,1,1,1,0,0,0,0,0], # 16
    [1,1,1,1,1,1,1,1,1,1], # 17
    [1,1,1,1,1,1,1,1,1,1], # 18
    [1,1,1,1,1,1,1,1,1,1], # 19
    [1,1,1,1,1,1,1,1,1,1], # 20
    [1,1,1,1,1,1,1,1,1,1]  # 21
]
softStrat = [
    [0,0,0,3,3,0,0,0,0,0], # A2
    [0,0,0,3,3,0,0,0,0,0], # A3
    [0,0,3,3,3,0,0,0,0,0], # A4
    [0,0,3,3,3,0,0,0,0,0], # A5
    [0,3,3,3,3,0,0,0,0,0], # A6
    [4,4,4,4,4,1,1,0,0,0], # A7
    [1,1,1,1,4,1,1,1,1,1], # A8
    [1,1,1,1,1,1,1,1,1,1], # A9
    [1,1,1,1,1,1,1,1,1,1]  # A10
]
pairStrat = [
    [2,2,2,2,2,2,0,0,0,0], # 2,2
    [2,2,2,2,2,2,0,0,0,0], # 3,3
    [0,0,0,2,2,0,0,0,0,0], # 4,4
    [3,3,3,3,3,3,3,3,0,0], # 5,5
    [2,2,2,2,2,0,0,0,0,0], # 6,6
    [2,2,2,2,2,2,0,0,0,0], # 7,7
    [2,2,2,2,2,2,2,2,0,0], # 8,8
    [2,2,2,2,2,1,2,2,1,1], # 9,9
    [1,1,1,1,1,1,1,1,1,1], # 10,10
    [2,2,2,2,2,2,2,2,2,0]  # A,A
]

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def captureHandGrayImage(x,y):
    array_alpha = np.array([image_contrast_alpha])
    array_beta = np.array([image_contrast_beta])

    im=ImageGrab.grab(bbox=(x,y,x+handWidth,y+handHeight))

    img_np=np.array(im)

    gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # add a beta value to every pixel 
    cv2.add(gray_img, array_beta, gray_img)                    

    # # multiply every pixel value by alpha
    cv2.multiply(gray_img, array_alpha, gray_img)

    width = 640
    height = 640
    image_pil = Image.new("RGB", (width, height), "white")
    gray_img_pil = Image.fromarray(cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB))
    image_pil.paste(gray_img_pil, (100, 170))

    return image_pil

def detect_letter(image_path):
    reader = easyocr.Reader(['en'], recog_network="english_g2", user_network_directory=None)
    result = reader.readtext(image_path, allowlist=allowed_chars)

    if debug:
        print(f"read: {result}")

    return result

def redReady(pos):
    return pyautogui.pixelMatchesColor(pos[0], pos[1], redCol, tolerance=20) or pyautogui.pixelMatchesColor(pos[0], pos[1], redCol2, tolerance=20) or pyautogui.pixelMatchesColor(pos[0], pos[1], redCol3, tolerance=20)

def grayReady(pos):
    return pyautogui.pixelMatchesColor(pos[0], pos[1], grayCol, tolerance=20) or pyautogui.pixelMatchesColor(pos[0], pos[1], grayCol2, tolerance=20) or pyautogui.pixelMatchesColor(pos[0], pos[1], grayCol3, tolerance=20)
    

def getValue(str):
    if str == 'A':
        return 11
    elif str == 'K' or str == 'Q' or str == 'J' or str == '10':
        return 10
    elif str == '9' or str == '8' or str == '7' or str == '6' or str == '5' or str == '4' or str == '3' or str == '2':
        return int(str)
    
def getHand(x, y):
    num = captureHandGrayImage(x, y)
    target_image_path = "tmp/tmp_num.png"
    num.save(target_image_path)

    detected_letter = detect_letter(target_image_path)
    # detected_letter = pytesseract.image_to_string(Image.open(target_image_path), config='--psm 10 -c tessedit_char_whitelist="AJQK0123456789"')
    # detected_letter = "".join(detected_letter.split())
    print(f"found {detected_letter}")

    if detected_letter != 'A' and detected_letter != 'K' and detected_letter != 'Q' and detected_letter != 'J' and detected_letter != 'I0' and detected_letter != '10' and detected_letter != '1O' and detected_letter != 'IO' and detected_letter != '1Q' and detected_letter != 'IQ' and detected_letter != '1K' and detected_letter != '9' and detected_letter != '8' and detected_letter != '7' and detected_letter != '6' and detected_letter != '5' and detected_letter != '4' and detected_letter != '3' and detected_letter != '2' and detected_letter != '0' and detected_letter != '1':
        num.save("tmp/tmp_problem.png")

    # global loop
    # num.save("tmp/" + str(getValue(detected_letter)) + "/" + str(loop) + "_" + str(uuid.uuid4()) + ".png")

    return detected_letter

def handTotal(hand):
    total = 0
    ace = False
    for card in hand:
        if card == 11:
            ace = True
        total += card
    while ace and total >= 21:
        total -= 10
    return total

def handTotalHigh(hand):
    total = 0
    for card in hand:
        total += card
    return total

def getStrat(hand, dealer):
    if len(hand) == 2 and hand[0] == hand[1] and (splitStatus[0] == 'none'):
        return pairStrat[hand[0]-2][dealer-2]
    elif 11 in hand and handTotalHigh(hand) < 21:
        return softStrat[handTotal(hand)-13][dealer-2]
    else:
        return hardStrat[handTotal(hand)-5][dealer-2]

def playHand(playerHand, dealerHand):
    strat = getStrat(playerHand, dealerHand[0])
    if strat == 0:
        return "hit"
    elif strat == 1:
        return "stand"
    elif strat == 2:
        return "split"
    elif strat == 3:
        return "double/hit"
    elif strat == 4:
        return "double/stand"

def waitForReady():
    print("waiting for go")
    time.sleep(0.2)
    while(redReady(hitPos)):
        time.sleep(0.2)
        pyautogui.click()
    print("waiting for ready")
    while(not redReady(hitPos)):
        if debug:
            print(pyautogui.pixel(hitPos[0], hitPos[1]))
        time.sleep(0.2)

def clickMouse(x, y):
    pyautogui.moveTo(x+(random.random()*10)-5, y+(random.random()*10)-5, 0.5+random.random(), pyautogui.easeOutQuad)
    pyautogui.click()


def doAction(action):
    if action == "hit" or action == "end":
        clickMouse(hitPos[0], hitPos[1])
    elif action == "stand":
        clickMouse(standPos[0], standPos[1])
    elif action == "split":
        clickMouse(splitPos[0], splitPos[1])
    elif action == "double":
        clickMouse(doublePos[0], doublePos[1])
    elif action == "insurance":
        clickMouse(insurancePos[0], insurancePos[1])
    waitForReady()

def playGame(playerHand, dealerHand):
    print(playerHand, dealerHand)
    print(splitStatus)
    global loop
    if handTotal(playerHand) >= 21:
        return "end" #shouldn't be here. Read error
    playerAction = playHand(playerHand, dealerHand)
    print(playerAction)
    if playerAction == "double/hit":
        if len(playerHand) == 2:
            playerAction = "double"
        else:
            playerAction = "hit"
    if playerAction == "double/stand":
        if len(playerHand) == 2:
            playerAction = "double"
        else:
            playerAction = "stand"
    if playerAction == "hit":
        doAction("hit")
        if splitStatus[0] == 'none':
            playerHand = getHand(playerPos[0], playerPos[1])
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'R':
            playerHand = getHand(playerPosR[0], playerPosR[1])
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'L':
            playerHand = getHand(playerPosL[0], playerPosL[1])
            playGame(playerHand, dealerHand)
    elif playerAction == "stand":
        doAction("stand")
        return "end"
    elif playerAction == "split":
        doAction("split")
        loop += 1
        if(playerHand[0] == 11 and playerHand[1] == 11):
            return "end"
        if splitStatus[0] == 'none':
            splitStatus[0] = 'R'
            playerHandR = getHand(playerPosR[0], playerPosR[1])
            playGame(playerHandR, dealerHand)
            splitStatus[0] = 'L'
            playerHandL = getHand(playerPosL[0], playerPosL[1])
            playGame(playerHandL, dealerHand)
    elif playerAction == "double":
        doAction("double")
        loop += 1
        return "end"


if __name__ == "__main__":

    if len(sys.argv) - 1 != 1:
        print("Usage: python gpAutoBj.py [number of hands]")
        sys.exit()

    yag = yagmail.SMTP("abae.yusung@gmail.com", 'xlmj oqln whgl zhsc')

    while loop < int(sys.argv[1]):
        loop += 1
        print("checking for ready")
        while not redReady(hitPos):
            print(pyautogui.pixel(hitPos[0], hitPos[1]))
            time.sleep(0.2)

        print("ready")
        doAction("stand")

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Starting hand {loop}/{sys.argv[1]} [{timestamp}]")

        if(pyautogui.pixelMatchesColor(doublePos[0], doublePos[1], grayCol3, tolerance=5)):
            continue # player/dealer blackjack
        splitStatus[0] = 'none'
        if(grayReady(insurancePos)):
            doAction("insurance") # insurance
        if(pyautogui.pixelMatchesColor(doublePos[0], doublePos[1], grayCol3, tolerance=5)):
            continue # game over after insurance
        playerHand = getHand(playerPos[0], playerPos[1])
        dealerHand = getHand(dealerPos[0], dealerPos[1])
        playGame(playerHand, dealerHand)

        if loop >= target_cycle:
            target_cycle += notify_cycle
            yag.send("abae.yusung@gmail.com", contents=f"I'm on blackjack hand {loop}/{sys.argv[1]}")
    yag.send("abae.yusung@gmail.com", contents="I finished playing blackjack 🎉!")
