# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 19:42:33 2020

@author: Chase
"""
import getPerspective
import numpy as np
import argparse
import cv2
import imutils
from skimage.filters import threshold_local

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
ap.add_argument("-o", "--output", required = True,
	help = "output path")
ap.add_argument("-s", "--steps", required = False,
	help = "y to show steps")
args = vars(ap.parse_args())


STEPS = args["steps"] == "y"


def display(image):
    if STEPS:
        cv2.imshow("Image", imutils.resize(image.copy(), height = 500))
        cv2.waitKey(0)
        cv2.destroyAllWindows
#EDGE DETECTION

image = cv2.imread(args["image"])
display(image)


ratio = image.shape[0]/500
orig = image.copy()
image = imutils.resize(image,height = 500)
display(image)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
display(gray)


gray = cv2.GaussianBlur(gray, (5, 5), 0)
display(gray)

edged = cv2.Canny(gray, 75, 200)
display(edged)

#FIND CONTOURS

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
#only keep the 5 biggest
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

#loop through them
for c in cnts:
    
    #approximate number of points in each closed contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
display(image)

#four point transform

warped = getPerspective.four_point_transform(orig, screenCnt.reshape(4, 2)*ratio)
display(warped)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
display(warped)
cv2.destroyAllWindows()
#Threshold

T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

##DONE

finH = int(input("Desired Image Height: "))
cv2.imshow("Original", imutils.resize(orig, height = finH))
cv2.imshow("Scanned", imutils.resize(warped, height = finH))
cv2.imwrite(args["output"], imutils.resize(warped, height = finH))
cv2.waitKey(0)

cv2.destroyAllWindows()


