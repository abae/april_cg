import cv2
import numpy as np
import mss

# Load arrow template
template = cv2.imread("data/chumba/arrow.png", 0)
w, h = template.shape[::-1]

# Setup screen capture
sct = mss.mss()
monitor = {"left": 1779, "top": 1978, "width": 1000, "height": 166}

def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray)

while True:
    frame = np.array(sct.grab(monitor))
    processed = preprocess(frame)

    # Match template
    result = cv2.matchTemplate(processed, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust depending on fade level
    loc = np.where(result >= threshold)

    detected = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (0, 255, 0), 2)
        detected = True

    cv2.imshow("Arrow Detection", frame)
    if detected:
        print("Arrow detected!")

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()