# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:56:49 2020

@author: Chase
"""

import cv2
import imutils

image = cv2.imread("jp.jpg")
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))

(B, G, R) = image[100, 50]
print("R={}, G={}, B={}".format(R, G, B))


cv2.imshow("Image", image)
cv2.waitKey(0)


roi = image[50:100, 300:500]
cv2.imshow("ROI", roi)
cv2.waitKey(0)


resized = cv2.resize(image, (512, 512))
cv2.imshow("Resized", resized)
cv2.waitKey(0)

#resize without imutils

r = 750 / h
h = 750
w = int(w* r)
print(w)
dim = (w, 700)
resized = cv2.resize(image, dim)
cv2.imshow("aspect conserved", resized)
cv2.waitKey(0)

# or simply

resized = imutils.resize(image, height = 750)
cv2.imshow("imutils", resized)
cv2.waitKey(0)


cv2.destroyAllWindows()
image = resized

center = (w // 2, h //2)
M = cv2.getRotationMatrix2D(center, -45, 1)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("Rotated", rotated)
cv2.waitKey(0)

# or simply
rotated = imutils.rotate(image, -45)
cv2.imshow("Imutils Rotated", rotated)
cv2.waitKey(0)

#note that opencv doesn't care if image is clipped by rotation, this can be solved with bound rotation

rotated = imutils.rotate_bound(image, 45)
cv2.imshow("Bound Rotation", rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

#blurring image

blurred = cv2.GaussianBlur(image, (11, 11), 0)
cv2.imshow("blurred", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()


##DRAWING
output = image.copy()
#rectangle parameters = image, top left, bottom right, BGR tuple, thickness (negative = solid)
cv2.rectangle(output, (400,600), (700, 500), (0, 0, 255), 3)
cv2.imshow("rectangle", output)
cv2.waitKey(0)

output = image.copy()
#circle parameters = image, center, radius, color, thickness
cv2.circle(output, (300, 150), 80, (255, 0, 0), -1)
cv2.imshow("Circle", output)
cv2.waitKey(0)

# draw a 5px thick red line from x=60,y=20 to x=400,y=200
output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
cv2.imshow("Line", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Text

output = image.copy()

#text parameters = image, text, starting point, font, font scale factor, color, thickness
cv2.putText (output, "Testing Text Placement!s", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow("Text", output)
cv2.waitKey(0)
cv2.destroyAllWindows()