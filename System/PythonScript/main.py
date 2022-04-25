#import ProcessingStudent
import os
import Utilities
from threading import Thread
import cv2
import getopt
import sys
import requests
##########################



sensitivity = None
frameRate = None
exam_instance_id = None
def examVariables():
    """@brief: This function is responsible for retrieving sensitivity, exam instance id & fps"""
    sensitivity_arg = None
    exam_instance_id_arg = None
    fps = None
    argv = sys.argv[1:]
    try:
        opts , args= getopt.getopt(argv, 's:e:')        
    except getopt.GetoptError as e:
        # Print a message or do something useful
        print(e)
        print('Something went wrong!')
        sys.exit(2)
    
    ## getting arguments from the frontend
    # -s -> Sensitivity
    # -e -> exam instance id    
    for option, argument in opts:
            # if the option is sensitivity
        if option == '-s':
            sensitivity_arg = argument
        
        # if the option is exam_instance_id 
        if option == '-e':
            exam_instance_id_arg = argument

    exam_id_temp = exam_instance_id_arg
    # getting the fps value
    response = requests.get(f"http://classroommonitoring.herokuapp.com/api/user/get_fps/{exam_id_temp}")
    fps = response.json()['data']
    
    return sensitivity_arg, fps, exam_instance_id_arg
    ########################################################################################################################

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

# ########################################################################################################################
# ########################################################################################################################


if __name__ == "__main__":
    
    sensitivity, frameRate, exam_instance_id = examVariables()
    gatherFrames = Thread(target = retrieveFrames, args = ("/Users/marwanawad1/Downloads/file_example_MP4_480_1_5MG.mp4",) )
    gatherFrames.start()

    studentLocations = yolo2sec()
    # send studentLocations to backend here

    processing = ProcessingStudent(studentLocations, se)
    frameCount = frameCount + 1

    while(feedEnd == False):
        if(frameCount % frameRate == 0):
            processing.runThreading(allImages[frameCount - frameRate: frameCount])
            # processing.runSequential(allImages[frameCount - frameRate: frameCount])

        frameCount = frameCount + 1
