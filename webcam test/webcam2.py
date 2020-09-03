# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:21:34 2020

@author: Chase
"""


import cv2
import imutils

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gauss = cv2.GaussianBlur(frame, (5, 5), 0)
    # Display the resulting frame
    rotated = imutils.rotate_bound(gauss, 180)
    cv2.imshow('frame', rotated)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()