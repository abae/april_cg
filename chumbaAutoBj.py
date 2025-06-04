import cv2
from pathlib import Path
import pyscreenshot as ImageGrab
import time
import pyautogui
from pyautogui import ImageNotFoundException
import numpy as np
import random
import sys
from matplotlib import pyplot as plt
from PIL import Image, ImageGrab
import imagehash
import pytesseract
import shutil
import uuid
import datetime
import json
import mss

gameOver = False
num_split = 0
image_contrast_alpha = 7.0
image_contrast_beta = -80.0

wait_count = 0
max_wait_count = 10

loop = 0
data = []

# Setup screen capture
template = cv2.imread("data/chumba/arrow.png", 0)
sct = mss.mss()
monitor = {}


# strat tables 0 = hit, 1 = stand, 2 = split, 3 = double/hit, 4 = double/stand
hardStrat = [
    [0,0,0,0,0,0,0,0,0,0], # 5
    [0,0,0,0,0,0,0,0,0,0], # 6
    [0,0,0,0,0,0,0,0,0,0], # 7
    [0,0,0,0,0,0,0,0,0,0], # 8
    [0,3,3,3,3,0,0,0,0,0], # 9
    [3,3,3,3,3,3,3,3,0,0], # 10
    [3,3,3,3,3,3,3,3,3,0], # 11
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
    [1,4,4,4,4,1,1,0,0,0], # A7
    [1,1,1,1,1,1,1,1,1,1], # A8
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

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            global data
            data = json.load(file)
            return
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {file_path}")
        return

def find_indicator():
    global data
    global template
    global sct
    global monitor
    w, h = template.shape[::-1]
    while True:
        frame = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.equalizeHist(gray)

        # Match template
        result = cv2.matchTemplate(processed, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust depending on fade level
        loc = np.where(result >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (0, 255, 0), 2)
            return pt[0]+(w/2), pt[1]+(h/2)


def get_image_pos_on_screen(image_path):  
    try:
        global data
        location = pyautogui.locateOnScreen(image_path, confidence=0.96, region=(data['none']['x']+data['check_area']['x'], data['none']['y']+data['check_area']['y'], data['check_area']['w'], data['check_area']['h']))
        if location:
            return pyautogui.center(location)
        else:
            return None
    except ImageNotFoundException:
        return None

def getHand(x, y):
    global data
    width = data['read_width']
    height = data['read_height']
    im=ImageGrab.grab(bbox=(x,y,x+width,y+height))
    im.save(f"./data/{sys.argv[1]}/{x}.{y}.png")
    image=np.array(im)

    # Convert to grayscale
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("data/chumba/.tmp/target.png", thresh)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by x-coordinate (to process ranks in order)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    rank_contours = []

    texts = ""
    hand = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small and large contours
        if (w > data['rank']['minw'] and w < data['rank']['maxw']) and (h > data['rank']['minh'] and h < data['rank']['maxh']):
            rank_contours.append(contour)

    for rank_contour in rank_contours:
        x, y, w, h = cv2.boundingRect(rank_contour)
        # Extract ROI (Region of Interest)
        roi = gray[y:y+h, x:x+w]
        scaling = 32/h
        roi = cv2.resize(roi, None, fx=scaling, fy=scaling, interpolation=cv2.INTER_CUBIC)
        _, roi = cv2.threshold(roi, 128, 255, cv2.THRESH_BINARY)  # Step 2: Binarize

        width = 200
        height = 200
        image_pil = Image.new("RGB", (width, height), "white")
        gray_img_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        image_pil.paste(gray_img_pil, (100, 100))
        # image_np = np.array(image_pil)
        # kernel = np.ones((2, 2), np.uint8)  # you can try (1,2) or (2,1) for directional slimming
        # eroded = cv2.erode(image_np, kernel, iterations=1)
        # image_pil = Image.fromarray(cv2.cvtColor(eroded, cv2.COLOR_BGR2RGB))
        image_pil.save(f"./data/{sys.argv[1]}/.tmp/contour_{x}_{y}.png")
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image_pil, config="--psm 10 -c tessedit_char_whitelist=0123456789/")
        #boxes = pytesseract.image_to_boxes(image_pil, config="--psm 10 -c tessedit_char_whitelist=0123456789JQKA")
        text = text.strip()
        
        if text:
            print(f"found {text}")
            texts += text
        else:
            print(f"failed to find see contour {sys.argv[1]} (assuming it's 4)")
            texts += '4'
            image_pil.save(f"./data/{sys.argv[1]}/error/contour_{sys.argv[1]}_{x}_{y}.png")
    result = texts.split("/")
    if(len(result) == 2):
        hand.append(True)
        result[0] = result[1]
    elif(len(result) == 1):
        hand.append(False)
    else:
        print("Error, more than one delimiter detected")
    hand.append(int(result[0]))
    return hand

def handTotal(hand):
    return hand[1]

def handTotalHigh(hand):
    return hand[1]

def getStrat(hand, dealer):
    if hand[1] % 2 == 0 and checkForButton('split'):
        if hand[0]:
            return pairStrat[9][dealer-2]
        else:
            return pairStrat[int(round(hand[1]/2))-2][dealer-2]
    elif hand[0]:
        return softStrat[handTotal(hand)-13][dealer-2]
    else:
        return hardStrat[handTotal(hand)-5][dealer-2]

def playHand(playerHand, dealerHand):
    strat = getStrat(playerHand, dealerHand[1])
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

def checkForButton(button):
    for i in range(max_wait_count):
        pos = get_image_pos_on_screen(f"./data/{sys.argv[1]}/{button}.png")
        if pos is not None:
            return True
    return False

def waitForReady():
    time.sleep(0.5)
    while True:
        print("Looking for object")
        if get_image_pos_on_screen(f"./data/{sys.argv[1]}/hit.png") != None:
            return "hit"
        if get_image_pos_on_screen(f"./data/{sys.argv[1]}/again.png") != None:
            return "again"
        if get_image_pos_on_screen(f"./data/{sys.argv[1]}/no_ins.png") != None:
            doAction("no_ins")

def clickMouse(x, y):
    pyautogui.moveTo(x+(random.random()*10)-5, y+(random.random()*10)-5, 0.1+(random.random()*0.05), pyautogui.easeOutQuad)
    pyautogui.click()


def doAction(action):
    global gameOver
    pos = get_image_pos_on_screen(f"./data/{sys.argv[1]}/{action}.png")
    while(pos == None):
        print(f"Looking for {action}")
        time.sleep(0.2)
        pos = get_image_pos_on_screen(f"./data/{sys.argv[1]}/{action}.png")
        if action != "again" and (get_image_pos_on_screen(f"./data/{sys.argv[1]}/again.png") != None):
            pos = get_image_pos_on_screen(f"./data/{sys.argv[1]}/again.png")
            gameOver = True
    if not gameOver:
        clickMouse(pos[0], pos[1])
    return waitForReady()

def playGame(dealerHand):
    if gameOver:
        return "end"
    waitForReady()
    ind_x, ind_y = find_indicator()
    playerHand = getHand(data['none']['x'] + data['indicator_area']['x'] + ind_x + data['indicator_offset']['x'], data['none']['y'] + data['indicator_area']['y'] + ind_y + data['indicator_offset']['y'])
    print(playerHand, dealerHand)
    global loop
    if handTotal(playerHand) >= 21:
        doAction("stand")
        return "end" #shouldn't be here. Read error
    #Find out the play
    playerAction = playHand(playerHand, dealerHand)
    print(playerAction)
    if playerAction == "double/hit":
        if checkForButton("double"):
            playerAction = "double"
        else:
            playerAction = "hit"
    if playerAction == "double/stand":
        if checkForButton("double"):
            playerAction = "double"
        else:
            playerAction = "stand"
    # Begin player action
    if playerAction == "hit":
        if doAction("hit") == "again":
            return "end" # player bust
        playGame(dealerHand)
    elif playerAction == "stand":
        doAction("stand")
        return "end"
    elif playerAction == "split":
        loop += 1
        if doAction("split") == "again":
            return "end"
        playGame(dealerHand)
    elif playerAction == "double":
        loop += 1
        doAction("double")
        return "end"


if __name__ == "__main__":

    if len(sys.argv) - 1 != 2:
        print("Usage: python llAutoBj.py [type] [number of hands]")
        sys.exit()

    read_json_file(f"./data/{sys.argv[1]}/data.json")
    print(f"Starting {sys.argv[1]} with {sys.argv[2]} hands")

    folder = Path(f"./data/{sys.argv[1]}/error/")
    for file in folder.iterdir():
        if file.is_file():
            file.unlink()

    monitor = {"left": data['none']['x'] + data['indicator_area']['x'], "top": data['none']['x'] + data['indicator_area']['y'], "width": data['indicator_area']['w'], "height": data['indicator_area']['h']}

    while loop < int(sys.argv[2]):
        gameOver = False
        splitStatus = 'none'
        num_split = 0
        print("checking for ready")
        status = doAction("again")
        loop += 1

        folder = Path(f"./data/{sys.argv[1]}/.tmp/")
        for file in folder.iterdir():
            if file.is_file():
                file.unlink()

        if status == "again":
            continue
        if status == "hit":
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Starting hand {loop}/{sys.argv[2]} [{timestamp}]")

            dealerHand = getHand(data[splitStatus]['x'] + data['deal']['x'], data[splitStatus]['y'] + data['deal']['y'])
            playGame(dealerHand)
