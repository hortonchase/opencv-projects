# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 18:54:26 2020

@author: Chase
"""
import argparse
import imutils
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("image", image)
cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("image", gray)
cv2.waitKey(0)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow("image", blurred)
cv2.waitKey(0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    #Calculating center x and y
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    cv2.drawContours(image, [c], -1, (0, 255, 0))
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX-20, cY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    cv2.imshow("Image", image)
    cv2.waitKey(0)