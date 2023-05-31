import cv2
import serial
import time
import serial.tools.list_ports
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)
detector=HandDetector(detectionCon=0.5,maxHands=1)
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
#dict_={0:"Stop",1:"Forward",2:"Right",3:"Left",4:"Back",5:"Gar"}
dict_={0:"0",1:"1",2:"2",3:"3",4:"4",5:"5"}
portsList = []
for onePort in ports:
    portsList.append(str(onePort))
    print (str(onePort))
val = input("Select Port: COM")
for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print (portVar)
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

def write_read(x):
    serialInst.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    data = serialInst.readline()
    return data

def get_value(x):
    return dict_[x]
while True:
    ret,frame=cap.read()
    hands,frame=detector.findHands(frame)
    if not hands:
        print("Nothing")
        command=get_value(0)
        serialInst.write(command.encode('utf-8'))
    else:
        handsl=hands[0]
        fingers=detector.fingersUp(handsl)
        count=fingers.count(1)
        command=get_value(count)
        serialInst.write(command.encode('utf-8'))
        #write_read(str(count))
        print(count)
    cv2.imshow("FRAME",frame)   
    if cv2.waitKey(1)&0xFF==27:
        break
    time.sleep(1)
