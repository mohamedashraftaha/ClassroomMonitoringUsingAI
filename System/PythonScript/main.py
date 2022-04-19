import ProcessingStudent
import os
import Utilities
from threading import Thread
import cv2

########################################################################################################################
frameRate = 24
sensitivity = 5
########################################################################################################################
utils = Utilities

YOLO_THRESH = 0.5
YOLO_SUPPRESSION_THRESH = 0.3

frameCount = 0
feedEnd = False
allImages = []

def retrieveFrames(source):
    cap = cv2.VideoCapture(source)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            allImages.append(frame)
        else:
            break
    feedEnd = True;
    print(len(allImages))

def yolo2sec():
    maxLocations = []
    while(frameCount < (frameRate * 2)):
        tempLocations = utils.YOLO(Utilities, allImages[frameCount], YOLO_THRESH, YOLO_SUPPRESSION_THRESH)
        frameCount = frameCount + 1
        if(len(tempLocations) > len(maxLocations)):
            maxLocations = tempLocations
    return maxLocations

########################################################################################################################
########################################################################################################################

gatherFrames = Thread(target = retrieveFrames, args = ("/Users/marwanawad1/Downloads/file_example_MP4_480_1_5MG.mp4",) )
gatherFrames.start()

studentLocations = yolo2sec()
# send studentLocations to backend here

processing = ProcessingStudent(studentLocations, sensitivity)
frameCount = frameCount + 1

while(feedEnd == False):
    if(frameCount % frameRate == 0):
        processing.runThreading(allImages[frameCount - frameRate: frameCount])
        # processing.runSequential(allImages[frameCount - frameRate: frameCount])

    frameCount = frameCount + 1
