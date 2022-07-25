
import cv2
from cv2 import waitKey

def imageDisplay(tuningPara, rawImageQueue, outPutImageQueue):
    while True:
        # print("Hello world from get1")
        img = rawImageQueue.get()
        img2 = outPutImageQueue.get()
        cv2.imshow('rawImageDisplay',img)
        cv2.imshow('outPutImageDisplay',img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break