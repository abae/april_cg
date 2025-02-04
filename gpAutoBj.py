import cv2
from skimage.metrics import structural_similarity as ssim
import os
import pyscreenshot as ImageGrab
import time
import pyautogui
import numpy as np
import random
import sys
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import easyocr
import datetime
import yagmail
import requests
from bs4 import BeautifulSoup
from ultralytics import YOLO
import yaml

model = YOLO("yolov8s_playing_cards.pt")

playerPos = ()
playerPosR = ()
playerPosRR = ()
playerPosRL = ()
playerPosL = ()
playerPosLR = ()
playerPosLL = ()
dealerPos = ()
hitPos = ()
standPos = ()
splitPos = ()
doublePos = ()
handWidth = 100
handHeight = 100
hitCol = ()
insuranceCol = ()

splitStatus = ['none']

loop = 0
notify_cycle = 100
target_cycle = notify_cycle

yaml_data = {}

# strat tables 0 = hit, 1 = stand, 2 = split, 3 = double/hit, 4 = double/stand
hardStrat = [
    [0,0,0,0,0,0,0,0,0,0], # 5
    [0,0,0,0,0,0,0,0,0,0], # 6
    [0,0,0,0,0,0,0,0,0,0], # 7
    [0,0,0,0,0,0,0,0,0,0], # 8
    [0,3,3,3,3,0,0,0,0,0], # 9
    [3,3,3,3,3,3,3,3,0,0], # 10
    [3,3,3,3,3,3,3,3,3,3], # 11
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
    [2,2,2,2,2,2,2,2,2,2], # 8,8
    [2,2,2,2,2,1,2,2,1,1], # 9,9
    [1,1,1,1,1,1,1,1,1,1], # 10,10
    [2,2,2,2,2,2,2,2,2,2]  # A,A
]

def getValue(str):
    if str == 'A':
        return 11
    elif str == 'K' or str == 'Q' or str == 'J' or str == '10':
        return 10
    elif str == '9' or str == '8' or str == '7' or str == '6' or str == '5' or str == '4' or str == '3' or str == '2':
        return int(str)

def getHandInArea(x, y):
    im = ImageGrab.grab(bbox=(x,y,x+handWidth,y+handHeight))
    im.save(".tmpBJcapture.png")
    results = model(".tmpBJcapture.png")  # predict on an image
    hand = []
    for card in results[0]:
        hand.append(getValue(yaml_data.get(int(card[5]))[:-1]))
    print(hand)
    return hand

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
    if len(hand) == 2 and hand[0] == hand[1] and (splitStatus[0] == 'none' or splitStatus[0] == 'R' or splitStatus[0] == 'L'):
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
    while(not pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], (0, 0, 0), tolerance=5)):
        time.sleep(0.2)
        pyautogui.click()
    print("waiting for ready")
    while(pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], (0, 0, 0), tolerance=5)):
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
            playerHand = getHandInArea(playerPos[0], playerPos[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'R':
            playerHand = getHandInArea(playerPosR[0], playerPosR[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'RR':
            playerHand = getHandInArea(playerPosRR[0], playerPosRR[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'RL':
            playerHand = getHandInArea(playerPosRL[0], playerPosRL[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'L':
            playerHand = getHandInArea(playerPosL[0], playerPosL[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'LR':
            playerHand = getHandInArea(playerPosLR[0], playerPosLR[1], playerHand)
            playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'LL':
            playerHand = getHandInArea(playerPosLL[0], playerPosLL[1], playerHand)
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
            playerHandR = getHandInArea(playerPosR[0], playerPosR[1], [playerHand[1]])
            playGame(playerHandR, dealerHand)
            splitStatus[0] = 'L'
            playerHandL = getHandInArea(playerPosL[0], playerPosL[1], [playerHand[0]])
            playGame(playerHandL, dealerHand)
        elif splitStatus[0] == 'R':
            splitStatus[0] = 'RR'
            playerHandR = getHandInArea(playerPosRR[0], playerPosRR[1], [playerHand[1]])
            playGame(playerHandR, dealerHand)
            splitStatus[0] = 'RL'
            playerHandL = getHandInArea(playerPosRL[0], playerPosRL[1], [playerHand[0]])
            playGame(playerHandL, dealerHand)
        elif splitStatus[0] == 'L':
            splitStatus[0] = 'LR'
            playerHandR = getHandInArea(playerPosLR[0], playerPosLR[1], [playerHand[1]])
            playGame(playerHandR, dealerHand)
            splitStatus[0] = 'LL'
            playerHandL = getHandInArea(playerPosLL[0], playerPosLL[1], [playerHand[0]])
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

    with open('playing_cards.yaml', 'r') as f:
        yaml_data = yaml.full_load(f)
        yaml_data = yaml_data.get('names')

    while loop < int(sys.argv[1]):
        loop += 1
        print("checking for ready")
        if(pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], hitCol, tolerance=5)):
            print("ready")
            doAction("hit")

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Starting hand {loop}/{sys.argv[1]} [{timestamp}]")

        if(pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], hitCol, tolerance=5)):
            continue # player/dealer blackjack
        splitStatus[0] = 'none'
        if(pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], insuranceCol, tolerance=5)):
            doAction("hit") # insurance
        if pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], hitCol, tolerance=5):
            continue # game over
        playerHand = getHandInArea(playerPos[0], playerPos[1])
        dealerHand = getHandInArea(dealerPos[0], dealerPos[1])
        playGame(playerHand, dealerHand)

        if loop >= target_cycle:
            target_cycle += notify_cycle
            yag.send("abae.yusung@gmail.com", contents=f"I'm on blackjack hand {loop}/{sys.argv[1]}")
    yag.send("abae.yusung@gmail.com", contents="I finished playing blackjack 🎉!")
