# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:57:17 2020

@author: Chase
"""

import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument( "-t","--thresh", required = True,
    help = "threshold value")
args = vars(ap.parse_args())
threshold = args["thresh"]
image = args["image"]
image = cv2.imread(image)
cv2.imshow("Image", image)
cv2.waitKey(0)

#converting to grayscale

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

#finding edges

#parameters = image, minimum threshold, max thresh, kobel kernel size (default 3)
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edges", edged)
cv2.waitKey(0)

#Threshold, turns all values lower than 225 to 255 and all values above 225 to 0 or black
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

#find and draw contours
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

for c in cnts:
    #image, contour, ? -1, color, thickness
    cv2.drawContours(output, [c], -1, (0,0,255), 3)
    cv2.imshow("Contours", output)
    cv2.waitKey(200)
    cv2.destroyAllWindows()

txt = "I have found {} objects!".format(len(cnts))
cv2.putText(output, txt, (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
cv2.imshow("Final", output)
cv2.waitKey(0)
cv2.imshow("Original", image)

"""
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

#erode and dilate

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)
"""
#mask
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
