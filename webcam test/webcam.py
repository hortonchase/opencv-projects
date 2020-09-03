# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:13:35 2020

@author: Chase
"""
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import sys
from twilio.rest import Client
import boto3
count = 0
counter = 0
ct = 0
"""
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["video"])
"""
time.sleep(5)
vs = cv2.VideoCapture(0)
time.sleep(2.0)
firstFrame = None
# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()[1]
    #frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=1280)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)


    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]
    #Find the delta and threshold it
    
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)


    for c in cnts:
#        if cv2.contourArea(c) < args["min_area"]:
        if cv2.contourArea(c) < 30000:
            continue
        
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
        text = "Occupied"
        
        
        
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    
    
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    
    
    
    
    
    if text == "Occupied":
        count += 1
        if count > 340 and ct == 0:
            cv2.imwrite("pictures/image.png", frame)
            cv2.imwrite("pictures/thresh.png", thresh)
            cv2.imwrite("pictures/delta.png", frameDelta)
            s3 = boto3.client('s3')
            bucket = 'chorton34'
            s3.upload_file("pictures/image.png", bucket, "image.png", ExtraArgs={'ACL':'public-read'})
            s3.upload_file("pictures/thresh.png", bucket, "thresh.png", ExtraArgs={'ACL':'public-read'})
            s3.upload_file("pictures/delta.png", bucket, "delta.png", ExtraArgs={'ACL':'public-read'})
            
            
            
            
            account_sid = 'ACf99363af223008fe5be936ca558d0912'
            auth_token = '93359879ad35fd066b802f6c86bae85a'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                     body="Your Room is Occupied.\n https://chorton34.s3.us-east-2.amazonaws.com/image.png \n https://chorton34.s3.us-east-2.amazonaws.com/delta.png \n https://chorton34.s3.us-east-2.amazonaws.com/thresh.png",
                     from_='+12055288744',
                     to='+13167346373')
            ct+=1
            print("[TEXT SENT]")
    else:
        count = 0
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(counter)
    counter += 1
vs.release()
cv2.destroyAllWindows()

sys.exit()






































