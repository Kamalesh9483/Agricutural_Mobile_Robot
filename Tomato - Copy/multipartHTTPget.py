
from cv2 import imdecode
import cv2
from matplotlib.cbook import safe_masked_invalid
import numpy as np
import imutils 
import scipy.spatial.distance as dist
import requests

def empty(a):
    pass

def imageProcessor(dummy, rawImageQueue, outPutImageQueue):
    url = "http://192.168.43.136:81/stream"
    n = 1
    # Creating Trackbar for colour detection
    
    # cv2.namedWindow("Trackbar")
    # cv2.resizeWindow("Trackbar",500,500)

    # Setting HUE, SATURATION, VALUE min and max values
    # cv2.createTrackbar("Hue Min","Trackbar", 11, 179, empty)
    # cv2.createTrackbar("Hue Max","Trackbar", 179, 179, empty)
    # cv2.createTrackbar("Sat Min","Trackbar", 0, 255, empty)
    # cv2.createTrackbar("Sat Max","Trackbar", 255, 255, empty)
    # cv2.createTrackbar("Val Min","Trackbar", 0, 255, empty)
    # cv2.createTrackbar("Val Max","Trackbar", 255, 255, empty)

    # while True:
    r = requests.get(url, stream=True)
    boundary = bytes('\r\n--123456789000000000000987654321\r\nContent-Type: image/jpeg\r\nContent-Length: ', 'utf-8')
    for line in r.iter_lines(delimiter=boundary):
        if line:   
            if n!=0:
                pictureArray = bytearray(line)
                # Reading image and converting BGR to HSV image
                img = imdecode(np.asarray(bytearray(pictureArray[8:])), cv2.IMREAD_COLOR)
                if img is None:
                    continue
                
                # img = cv2.imread("C:\Projects\Mobile robot in hazardous environment\Agricultural Robot\Tomato\Tomato_Images\data\Image_96.jpg")
                # img = cv2.resize(img, (250, 250))
                # img = img.resize((250, 250))
                img_original = img 
                # img_original = cv2.resize(img, (700, 700))
                imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  

                # Getting Trackbar control
                # h_min = cv2.getTrackbarPos("Hue Min","Trackbar")
                # h_max = cv2.getTrackbarPos("Hue Max","Trackbar")
                # s_min = cv2.getTrackbarPos("Sat Min","Trackbar")
                # s_max = cv2.getTrackbarPos("Sat Max","Trackbar")
                # v_min = cv2.getTrackbarPos("Val Min","Trackbar")
                # v_max = cv2.getTrackbarPos("Val Max","Trackbar")
                h_min = 11
                h_max = 179
                s_min = 0
                s_max = 255
                v_min = 0
                v_max = 255
                lower = np.array([h_min, s_min, v_min])
                upper = np.array([h_max, s_max, v_max])
                mask = cv2.inRange(imghsv, lower, upper)
                imgResult = cv2.bitwise_and(img, img, mask=mask)
                mask = cv2.bitwise_not(mask, mask)
                
                # Image contour detectin and bounding box creation
                conts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # print(conts)
                conts = imutils.grab_contours(conts)
                cont_img = np.zeros(img.shape)
                cont_img = cv2.drawContours(img_original, None , -1, (0,0,0), 1)
                
                #midpoint definition
                def midPoint(ptA, ptB):
                    return ((ptA[0] + ptB[0])/2, (ptA[1] + ptB[1])/2)

                # #loop over all the contour coordinates
                for c in conts:
                    # extract box points
                    box = cv2.minAreaRect(c) #(left, top), (right, bottom), accuracy 
                    # print(box)
                    box = cv2.boxPoints(box)
                    #convert box points to integer
                    box = np.array(box, dtype='int')
                    
                    if cv2.contourArea(c) < 350:
                        continue

                    # cv2.drawContours(cont_img, [c], -1, (0,255,0), 1)
                    cv2.drawContours(cont_img, [box], -1, (255,255,255), 1)
                    
                    #print(box)
                    for (x,y) in box:
                        cv2.circle(cont_img, (x, y), 2, (255, 0, 0), 2)
                        (tl, tr, br, bl) = box
                    
                        #calculate midpoints for top-bottom of rectangle
                        (tlX, trX) = midPoint(tl, tr)
                        (brX, blX) = midPoint(br, bl)
                        
                        #draw midpoint dots for top and bottom
                        cv2.circle(cont_img, (int(tlX), int(trX)), 1, (255, 0, 0), 2)
                        cv2.circle(cont_img, (int(brX), int(blX)), 1, (255, 0, 0), 2)
                        
                        #connect the midpoints using line
                        cv2.line(cont_img, (int(tlX), int(trX)), (int(brX), int(blX)), (255, 255, 255), 1)
                        
                        #calculate the distance based on midpoints
                        dA = dist.euclidean((tlX, trX), (brX, blX))
                        
                        
                        #print the size in pixel in each contour rectangle
                        cv2.putText(cont_img, "{:.1f} px".format(dA), (int(tlX-10), int(trX-10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
                        cv2.putText(cont_img, "Tomato", (int(tlX+10), int(trX+10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 1)
                        
                        
                        #calculate midpoints for left-right of rectangle
                        (tlX, trX) = midPoint(tl, bl)
                        (brX, blX) = midPoint(tr, br)
                        
                    
                        #draw midpoint dots for left and right
                        cv2.circle(cont_img, (int(tlX), int(trX)), 1, (255, 0, 0), 2)
                        cv2.circle(cont_img, (int(brX), int(blX)), 1, (255, 0, 0), 2)
                        
                        #connect the midpoints using line
                        cv2.line(cont_img, (int(tlX), int(trX)), (int(brX), int(blX)), (255, 255, 255), 1)
                        
                        #calculate the distance based on midpoints
                        dB = dist.euclidean((tlX, trX), (brX, blX))
                        
                        #print the size in pixel in each contour rectangle
                        cv2.putText(cont_img, "{:.1f} px".format(dB), (int(brX+10), int(blX+10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255,255,255), 2)
                
                

                    # Showing image
                    

                cv2.imshow("Original",cont_img)
                cv2.resizeWindow("Original",250,250)
                outPutImageQueue.put(cont_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # cv2.imshow("HSV",imghsv)
                # cv2.resizeWindow("HSV",250,250)
                # cv2.imshow("mask",mask)
                # cv2.resizeWindow("mask",250,250)
                # cv2.imshow("imgResult",imgResult)
                # cv2.resizeWindow("imgResult",250,250)
                  
                # cv2.waitKey(1)