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
import shutil
import uuid
import datetime
import yagmail


# playerPos = (2286, 1241)
# playerPosR = (2375, 1237)
# playerPosRR = (2547, 1224)
# playerPosRL = (2375, 1237)
# playerPosL = (2177, 1237)
# playerPosLR = (2177, 1237)
# playerPosLL = (2040, 1224)
# dealerPos = (2304, 972)
# hitPos = (3092, 1535)
# standPos = (1692, 1535)
# splitPos = (1920, 1535)
# doublePos = (2854, 1535)

playerPos = (2286-1400, 1241-529)
playerPosR = (2375-1400, 1237-529)
playerPosRR = (2550-1400, 1224-529)
playerPosRL = (2375-1400, 1237-529)
playerPosL = (2177-1400, 1237-529)
playerPosLR = (2177-1400, 1237-529)
playerPosLL = (2040-1400, 1224-529)
dealerPos = (2304-1400, 972-529)
hitPos = (3092-1400, 1535-529)
standPos = (1692-1400, 1535-529)
splitPos = (1920-1400, 1535-529)
doublePos = (2854-1400, 1535-529)

repeatCol = (50, 0, 110)

letterDim = (21, 29) #tried 26,24
symDim = (21, 26)
cardGap = 28
splitStatus = ['none']

image_contrast_alpha = 7.0
image_contrast_beta = -80.0

wait_count = 0
max_wait_count = 300

loop = 0
notify_cycle = 50
target_cycle = notify_cycle


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

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def captureGrayImage(x,y,width,type):
    array_alpha = np.array([image_contrast_alpha])
    array_beta = np.array([image_contrast_beta])

    if type == 'num':
        im=ImageGrab.grab(bbox=(x,y,x+width,y+letterDim[1]))
    elif type == 'sym':
        im=ImageGrab.grab(bbox=(x,y+symDim[1]-1,x+symDim[0],y+letterDim[1]+symDim[1]))
    else:
        print("Invalid type")
    img_np=np.array(im)

    gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (width, letterDim[1]), interpolation = cv2.INTER_CUBIC)

    # add a beta value to every pixel 
    cv2.add(gray_img, array_beta, gray_img)                    

    # # multiply every pixel value by alpha
    cv2.multiply(gray_img, array_alpha, gray_img)

    width = 400
    height = 400
    image_pil = Image.new("RGB", (width, height), "white")
    gray_img_pil = Image.fromarray(cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB))
    image_pil.paste(gray_img_pil, (180, 170))

    return image_pil

def find_most_similar_image(target_image_path, directory):
    """Finds the most similar image to the target image in the given directory.

    Args:
        target_image_path (str): Path to the target image.
        directory (str): Path to the directory containing images to compare.

    Returns:
        str: Path to the most similar image.
    """

    max_ssim = -1
    most_similar_image = None

    target_image = cv2.imread(target_image_path)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Resize images if necessary for SSIM calculation
            if target_image.shape != image.shape:
                image = cv2.resize(image, target_image.shape[:2])

            ssim_value = ssim(target_image, image)
            print(image_path, ssim_value)

            if ssim_value > max_ssim:
                max_ssim = ssim_value
                most_similar_image = image_path

    if max_ssim < 0.3:
        print("No similar image found.")
        return None

    return most_similar_image[9:-4] # remove data/num/ and .png

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return thresh

def detect_letter(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)

    if result:
        return result[0][1]
    else:
        return None

def getValue(str):
    if str == 'A':
        return 11
    elif str == 'K' or str == 'Q' or str == 'J' or str == 'I0' or str == '10' or str == '1O' or str == 'IO' or str == '1Q' or str == 'IQ' or str == '1K' or str == '0' or str == '1':
        return 10
    elif str == '9' or str == '8' or str == '7' or str == '6' or str == '5' or str == '4' or str == '3' or str == '2':
        return int(str)

def getCard(x, y, width=letterDim[0]):
    num = captureGrayImage(x, y, width, 'num')
    target_image_path = "tmp/tmp_num.png"
    num.save(target_image_path)

    # preprocessed_image = preprocess_image(target_image_path)
    # detected_letter = detect_letter(preprocessed_image)
    detected_letter = pytesseract.image_to_string(Image.open(target_image_path), config='--psm 10 -c tessedit_char_whitelist="AJQK0123456789"')
    detected_letter = "".join(detected_letter.split())
    print(f"found {detected_letter}")

    if detected_letter != 'A' and detected_letter != 'K' and detected_letter != 'Q' and detected_letter != 'J' and detected_letter != 'I0' and detected_letter != '10' and detected_letter != '1O' and detected_letter != 'IO' and detected_letter != '1Q' and detected_letter != 'IQ' and detected_letter != '1K' and detected_letter != '9' and detected_letter != '8' and detected_letter != '7' and detected_letter != '6' and detected_letter != '5' and detected_letter != '4' and detected_letter != '3' and detected_letter != '2' and detected_letter != '0' and detected_letter != '1':
        num.save("tmp/tmp_problem.png")
        if width == 1:
            return -1
        return getCard(x, y, width-1)

    # global loop
    # num.save("tmp/" + str(getValue(detected_letter)) + "/" + str(loop) + "_" + str(uuid.uuid4()) + ".png")

    return detected_letter

def isPartnerReady(x, y, width=letterDim[0]):
    num = captureGrayImage(x, y, width, 'num')
    target_image_path = "tmp/tmp_num.png"
    num.save(target_image_path)

    # preprocessed_image = preprocess_image(target_image_path)
    # detected_letter = detect_letter(preprocessed_image)
    detected_letter = pytesseract.image_to_string(Image.open(target_image_path), config='--psm 10 -c tessedit_char_whitelist="AJQK0123456789"')
    detected_letter = "".join(detected_letter.split())
    print(f"check found {detected_letter}")

    global loop
    # num.save("tmp/" + str(getValue(detected_letter)) + "/" + str(loop) + "_check_" + str(uuid.uuid4()) + ".png")

    if detected_letter != 'A' and detected_letter != 'K' and detected_letter != 'Q' and detected_letter != 'J' and detected_letter != 'I0' and detected_letter != '10' and detected_letter != '1O' and detected_letter != 'IO' and detected_letter != '1Q' and detected_letter != 'IQ' and detected_letter != '1K' and detected_letter != '9' and detected_letter != '8' and detected_letter != '7' and detected_letter != '6' and detected_letter != '5' and detected_letter != '4' and detected_letter != '3' and detected_letter != '2' and detected_letter != '0' and detected_letter != '1':
        num.save("tmp/tmp_problem.png")
        if width == 1:
            return False
        return isPartnerReady(x, y, width-1)
    return True


def getHand(x, y, size):
    hand = []
    for i in range(size):
        card = getCard(x, y)
        hand.append(getValue(card))
        x += cardGap
    return hand

def appendHand(x, y, hand):
    x += cardGap*len(hand)
    card = getCard(x, y)
    hand.append(getValue(card))
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
    global wait_count
    global max_wait_count
    print("waiting for go")
    time.sleep(0.2)
    while(not pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], (0, 0, 0), tolerance=25)):
        time.sleep(0.2)
        pyautogui.click()
    print("waiting for ready")
    while(pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], (0, 0, 0), tolerance=25)):
        time.sleep(0.2)
        wait_count += 1
        if wait_count > max_wait_count:
            clickMouse(292, 199)
            time.sleep(5)
            clickMouse(278, 314)
            time.sleep(0.2)
            clickMouse(574, 448)
            time.sleep(8)
            if(not pyautogui.pixelMatchesColor(1008, 884, (69, 153, 232), tolerance=10)):
                for i in range(int(sys.argv[2])):
                    clickMouse(784, 726)
                    time.sleep(1)
            clickMouse(hitPos[0], hitPos[1])
            wait_count = 0
    wait_count = 0

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
        print(f"seeing {pyautogui.pixel(hitPos[0], hitPos[1])}")
        if pyautogui.pixelMatchesColor(hitPos[0], hitPos[1], repeatCol, tolerance=25):
            return "end" # player bust
        if splitStatus[0] == 'none':
            if(isPartnerReady(playerPos[0] + (cardGap*len(playerHand)), playerPos[1])):
                playerHand = appendHand(playerPos[0], playerPos[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'R':
            if(isPartnerReady(playerPosR[0] + (cardGap*len(playerHand)), playerPosR[1])):
                playerHand = appendHand(playerPosR[0], playerPosR[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'RR':
            if(isPartnerReady(playerPosRR[0] + (cardGap*len(playerHand)), playerPosRR[1])):
                playerHand = appendHand(playerPosRR[0], playerPosRR[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'RL':
            if(isPartnerReady(playerPosRL[0] + (cardGap*len(playerHand)), playerPosRL[1])):
                playerHand = appendHand(playerPosRL[0], playerPosRL[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'L':
            if(isPartnerReady(playerPosL[0] + (cardGap*len(playerHand)), playerPosL[1])):
                playerHand = appendHand(playerPosL[0], playerPosL[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'LR':
            if(isPartnerReady(playerPosLR[0] + (cardGap*len(playerHand)), playerPosLR[1])):
                playerHand = appendHand(playerPosLR[0], playerPosLR[1], playerHand)
                playGame(playerHand, dealerHand)
        elif splitStatus[0] == 'LL':
            if(isPartnerReady(playerPosLL[0] + (cardGap*len(playerHand)), playerPosLL[1])):
                playerHand = appendHand(playerPosLL[0], playerPosLL[1], playerHand)
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
            if(isPartnerReady(playerPosR[0], playerPosR[1])):
                playerHandR = appendHand(playerPosR[0], playerPosR[1], [playerHand[1]])
                playGame(playerHandR, dealerHand)
            splitStatus[0] = 'L'
            if(isPartnerReady(playerPosL[0], playerPosL[1])):
                playerHandL = appendHand(playerPosL[0], playerPosL[1], [playerHand[0]])
                playGame(playerHandL, dealerHand)
        elif splitStatus[0] == 'R':
            splitStatus[0] = 'RR'
            if(isPartnerReady(playerPosRR[0], playerPosRR[1])):
                playerHandR = appendHand(playerPosRR[0], playerPosRR[1], [playerHand[1]])
                playGame(playerHandR, dealerHand)
            splitStatus[0] = 'RL'
            if(isPartnerReady(playerPosRL[0], playerPosRL[1])):
                playerHandL = appendHand(playerPosRL[0], playerPosRL[1], [playerHand[0]])
                playGame(playerHandL, dealerHand)
        elif splitStatus[0] == 'L':
            splitStatus[0] = 'LR'
            if(isPartnerReady(playerPosLR[0], playerPosLR[1])):
                playerHandR = appendHand(playerPosLR[0], playerPosLR[1], [playerHand[1]])
                playGame(playerHandR, dealerHand)
            splitStatus[0] = 'LL'
            if(isPartnerReady(playerPosLL[0], playerPosLL[1])):
                playerHandL = appendHand(playerPosLL[0], playerPosLL[1], [playerHand[0]])
                playGame(playerHandL, dealerHand)
    elif playerAction == "double":
        doAction("double")
        loop += 1
        return "end"


if __name__ == "__main__":

    image_path = "./data/test.png"
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by x-coordinate (to process ranks in order)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    rank_contours = []

    ranks = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small and large contours
        if (w > 10 and w < 50) and (h > 42 and h < 50):
            rank_contours.append(contour)

    for rank_contour in rank_contours:
        x, y, w, h = cv2.boundingRect(rank_contour)
        # Extract ROI (Region of Interest)
        roi = gray[y:y+h, x:x+w]
        scaling = 32/h
        roi = cv2.resize(roi, None, fx=scaling, fy=scaling, interpolation=cv2.INTER_CUBIC)
        _, roi = cv2.threshold(roi, 128, 255, cv2.THRESH_BINARY)  # Step 2: Binarize
        width = 400
        height = 400
        image_pil = Image.new("RGB", (width, height), "white")
        gray_img_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        image_pil.paste(gray_img_pil, (180, 170))
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image_pil, config="--psm 10 -c tessedit_char_whitelist=0123456789JQKA")
        boxes = pytesseract.image_to_boxes(image_pil, config="--psm 10 -c tessedit_char_whitelist=0123456789JQKA")
        print(boxes)
        plt.imshow(image_pil, cmap='gray')
        plt.show()
        print("Extracted Text:", text)

        text = text.strip()
        
        if text:
            ranks.append(text)
    print("Extracted Ranks:", ranks)
    output_image = image.copy()
    cv2.drawContours(output_image, rank_contours, -1, (0, 0, 255), 2)

    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.show()

