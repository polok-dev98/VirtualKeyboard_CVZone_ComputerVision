#importing the library
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
 
cap = cv2.VideoCapture(0)
#set the height and width of the camera.
cap.set(3, 1280)
cap.set(4, 720)

#initialize the hand detector.
detector = HandDetector(detectionCon=0.8)
# Set the keyboard button.
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
 
keyboard = Controller()
 
# Draw the keyboard layout.
def drawAll(img, buttonList):
     imgNew = np.zeros_like(img, np.uint8)
     for button in buttonList:
         
         x, y = button.pos
         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                       (255, 0, 255), cv2.FILLED)
         cv2.putText(imgNew, button.text, (x + 40, y + 60),
                     cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)

     out = img.copy()
     alpha = 0.5
     mask = imgNew.astype(bool)
     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
     return out
 
# create the button class.
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
 
 
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
 
while True:
    success, img = cap.read()
    hands,img = detector.findHands(img)
    img = drawAll(img, buttonList)
    
    if hands:
        hand= hands[0]
        lmlist= hand["lmList"]
 
        if lmlist:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
 
                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(lmlist[8],lmlist[12], img)
                
 
                ## when clicked
                    if l < 30:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)
 
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
 
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
