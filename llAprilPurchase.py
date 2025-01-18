import yagmail
import pyautogui
import subprocess
import sys

if __name__ == "__main__":
    bashCommand = "sh ./llPurchase.sh"
    bjCommand = "sh ./llBuyPlay.sh 4"
    yag = yagmail.SMTP("abae.yusung@gmail.com", 'xlmj oqln whgl zhsc')
    for i in range(0, int(sys.argv[1])):
        if (i+1) % 15 == 0:
            # process = subprocess.Popen(bjCommand.split(), stdout=subprocess.PIPE)
            # output, error = process.communicate()

            content = f"I'm purchasing LL pack {i+1}/{int(sys.argv[1])}"
            # yag.send("7045648247@mms.cricketwireless.net", contents=content)
            yag.send("abae.yusung@gmail.com", contents=content)
        
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        print(f"pack {i+1}/{int(sys.argv[1])} purchased")
    # yag.send("7045648247@mms.cricketwireless.net", contents="I finished purchasing LL packs 🎉!")
    yag.send("abae.yusung@gmail.com", contents="I finished purchasing LL packs 🎉!")
