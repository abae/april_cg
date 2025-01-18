import requests
from bs4 import BeautifulSoup
from ultralytics import YOLO
import pyautogui
import random

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8s_playing_cards.pt")  # load a pretrained model (recommended for training)

# Use the model
# results = model.train(data="coco128.yaml", epochs=3)  # train the model
# results = model.val()  # evaluate model performance on the validation set
results = model("ghAutoJob")  # predict on an image
# success = YOLO("yolov8n.pt").export(format="onnx")  # export a model to ONNX format
print([x for x in results])

def clickMouse(x, y):
    pyautogui.moveTo(x+(random.random()*10)-5, y+(random.random()*10)-5, 0.5+random.random(), pyautogui.easeOutQuad)
    pyautogui.click()

def read_cards_on_screen():
    # Load a model
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model = YOLO("yolov8s_playing_cards.pt")  # load a pretrained model (recommended for training)

    # Use the model
    # results = model.train(data="coco128.yaml", epochs=3)  # train the model
    # results = model.val()  # evaluate model performance on the validation set
    results = model("ghAutoJob")  # predict on an image
    # success = YOLO("yolov8n.pt").export(format="onnx")  # export a model to ONNX format
    print([x for x in results])
    print(f"card detected: {results[0][0][5]}")
    pass

def send_cards_to_server(cards):
    # Making a GET request
    r = requests.get('https://casinointellect.com/tools/vpa_calcpr.php/4h9d6h5d2d-jb-mc65', verify=False)

    if (r.status_code == 200):
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.prettify())
    pass

def click_hold_cards(response):
    # Implement the logic to click on hold cards
    pass

if __name__ == "__main__":
    for i in range(1):
        # clickMouse(100, 100)
        cards = read_cards_on_screen()
        # response = send_cards_to_server(cards)
        # click_hold_cards(response)
        # clickMouse(200, 200)
