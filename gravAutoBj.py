from playwright.sync_api import sync_playwright
import time
import pyautogui
import random
import sys
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

siteList = {
    "test": "https://client.petros04.com/?token=01K6KF2VC8KJ3JM7P4YY8MQY9E&cid=luckyHands&brand=luckyHands&launchAlias=launch_main_ssbj_01&nolobby=1&social=1&username=75381369-711c-440c-a264-5edf5677a8fa_gc",
    "luckyhands": "https://client.petros04.com/?token=01K6HN2HTX7WT5ME3H8K7V1QVA&cid=luckyHands&brand=luckyHands&launchAlias=launch_main_ssbj_01&nolobby=1&social=1&username=75381369-711c-440c-a264-5edf5677a8fa_ss#launch_main_ssbj_01",
    "realprize": "https://www.realprize.com",
    "b2": "https://www.megabonanza.com/"
}

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
    [2,2,2,2,2,2,2,2,0,2], # 8,8
    [2,2,2,2,2,1,2,2,1,1], # 9,9
    [1,1,1,1,1,1,1,1,1,1], # 10,10
    [2,2,2,2,2,2,2,2,2,2]  # A,A
]

def getHand(handStr):
    hand = []

    result = handStr.split("/")
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

def getStrat(hand, dealer, splitCheck=True):
    if hand[1] % 2 == 0 and splitCheck:
        if hand[0]:
            return pairStrat[9][dealer-2]
        else:
            return pairStrat[int(round(hand[1]/2))-2][dealer-2]
    elif hand[0]:
        return softStrat[handTotal(hand)-13][dealer-2]
    else:
        return hardStrat[handTotal(hand)-5][dealer-2]

def playHand(playerHand, dealerHand, splitCheck=True):
    strat = getStrat(playerHand, dealerHand[1], splitCheck)
    backupStrat = ""
    if splitCheck and strat == 2:
        backupStrat = playHand(playerHand, dealerHand, False)
    if strat == 0:
        return "hit"
    elif strat == 1:
        return "stand"
    elif strat == 2:
        return "split/"+str(backupStrat)
    elif strat == 3:
        return "double/hit"
    elif strat == 4:
        return "double/stand"

def clickMouse(x, y):
    pyautogui.moveTo(x+(random.random()*10)-5, y+(random.random()*10)-5, 0.1+(random.random()*0.05), pyautogui.easeOutQuad)
    pyautogui.click()


def doAction(action):
    if action == "hit":
        clickMouse(hit_x, decision_y)
    elif action == "stand":
        clickMouse(stand_x, decision_y)
    elif action == "double":
        clickMouse(double_x, decision_y)
    elif action == "split":
        clickMouse(split_x, decision_y)
    elif action == "no_insurance":
        clickMouse(stand_x, decision_y)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 gravAutoBj.py <site> <chip (0-6)> <number of chips to bet> <number of hands>")
        sys.exit(1)
    
    chips_y = 778
    chips_x_start = 1600-1080
    chips_dist = 48
    # chips_y = 726
    # chips_x_start = 539
    # chips_dist = 36
    replay_x = 1720-1080
    replay_y = 628
    decision_y = 460
    double_x = 1609-1080
    hit_x = 1677-1080
    stand_x = 1758-1080
    split_x = 1829-1080

    site = sys.argv[1]
    chip_choice = int(sys.argv[2])
    chip_quant = int(sys.argv[3])
    hand_count = int(sys.argv[4])
    split_active = False

    loop = 0
    refreshRate = 30
    refreshLoop = 0
    isReady = True
    refreshMin = 5
    refreshTime = datetime.now() + timedelta(minutes=refreshMin)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = frame = browser.new_page()
        page.goto(siteList[site])

        if "b2" in site:
            # frame = page.frame_locator("iframe.GameCanvas_iframe__h40la").frame_locator("iframe.styles_root__frK1Y")
            frame = page.frame_locator("iframe.styles_iframe__bzIFL").frame_locator("iframe.styles_root__frK1Y")
            chips_y = 732
            chips_x_start = 560
            chips_dist = 35
            # chips_y = 726
            # chips_x_start = 539
            # chips_dist = 36
            replay_x = 1712-1080
            replay_y = 607
            decision_y = 480
            double_x = 1628-1080
            hit_x = 1680-1080
            stand_x = 1744-1080
            split_x = 1795-1080
        elif "realprize" in site:
            frame = page.frame_locator("iframe#gwindow")
        chip_x = chips_x_start + chip_choice * chips_dist

        betting_panel = frame.locator("div.gameContent__bettingPanel-b3eK9c.gameContent__bettingPanel_active-S8htDn")
        player_hands = frame.locator("div.playerHands__mainHand-i6TJiP")
        player_hand_value = player_hands.locator("div.blackjackCardsStack__value-sxwR0n")
        dealer_hand = frame.locator("div.gameContent__dealerCardsStack-pzxdrb")
        dealer_hand_value = dealer_hand.locator("div.blackjackCardsStack__value-sxwR0n")
        split_hand = frame.locator("div.playerHands__splitHand-ZCTUCP")
        hit_button = frame.locator("[data-locator='hit-button']")
        no_button = frame.locator("[data-locator='no-insurance-button']")
        split_button = frame.locator("[data-locator='split-button']")
        double_button = frame.locator("[data-locator='double-button']")
        close_button = frame.locator("[data-locator='close-client-behavior']")

        try:
            while True:
                if datetime.now() > refreshTime:
                    print("Timed out... refreshing page...")
                    page.reload()
                    time.sleep(100)
                    refreshTime = datetime.now() + timedelta(minutes=refreshMin)
                time.sleep(0.5)
                action = None

                if betting_panel.count() > 0:
                    action = "betting_panel"
                elif hit_button.count() > 0:
                    action = "hit_button"
                elif no_button.count() > 0:
                    action = "noins_button"

                if action is not None and not isReady:
                    print(f"Found {action}, but waiting for reset...")
                    continue
                isReady = False

                if action == "betting_panel":
                    if loop >= hand_count:
                        print("Reached hand count, exiting.")
                        break
                    loop += 1
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Betting hand {loop}/{hand_count}")
                    clickMouse(chip_x, chips_y)
                    for _ in range(chip_quant):
                        clickMouse(replay_x, replay_y)
                    split_active = False
                    
                elif action == "hit_button":
                    refreshTime = datetime.now() + timedelta(minutes=refreshMin)
                    playerHand = ""
                    dealerHand = ""
                    if player_hand_value.count() > 0:
                        playerData = getHand(player_hand_value.first.inner_text())
                        if playerData[1] >= 21:
                            split_active = True
                    if split_hand.count() > 0 and split_active:
                        print("Found active split hand")
                        playerHand = split_hand.locator(".blackjackCardsStack__value-sxwR0n").inner_text()
                        print("Score:", playerHand)
                    elif player_hand_value.count() > 0:
                        print("Found player hand")
                        playerHand = player_hand_value.first.inner_text()
                        print("Score:", playerHand)
                    if dealer_hand_value.count() > 0:
                        dealerHand = dealer_hand_value.first.inner_text()
                        print("Dealer Score:", dealerHand)
                    playerHandData = getHand(playerHand)
                    dealerHandData = getHand(dealerHand)
                    strat = playHand(playerHandData, dealerHandData)
                    print(f"Strategy: {strat}")
                    print(f"Double allowed: {double_button.is_enabled()}")
                    print(f"Split allowed: {split_button.is_enabled()}")
                    for act in strat.split("/"):
                        if act == "double" and double_button.is_enabled():
                            doAction("double")
                            loop += 1
                            split_active = True
                            break
                        elif act == "split" and split_button.is_enabled():
                            doAction("split")
                            loop += 1
                            break
                        elif act == "hit" or act == "stand":
                            doAction(act)
                            if act == "stand":
                                split_active = True
                            break

                elif action == "noins_button":
                    print(f"No insurance allowed: {no_button.is_enabled()}")
                    if no_button.is_enabled():
                        doAction("no_insurance")
                    
                else:
                    # print("Neither appeared within timeout.")
                    isReady = True

                
        except KeyboardInterrupt:
            print("Script interrupted by user.")
