import ProcessingStudent
import os
from threading import Thread
import cv2

allImages = []
def readTextFile(path):
    with open(os.path.join(path)) as file:
        fileData = file.read().splitlines()
    sensitivity = fileData[0]
    studentDetails = []
    for f in fileData:
        if fileData.index(f) != 0:
            tempData = f.split()
            studentDetails.append(tempData)
    return sensitivity, studentDetails

def retrieveFrames(source):
    cap = cv2.VideoCapture(source)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            allImages.append(frame)
        else:
            break

    print(len(allImages))

readTextFile("/Users/marwanawad1/Desktop/test.txt")
gatherFrames = Thread(target = retrieveFrames, args = ("/Users/marwanawad1/Downloads/file_example_MP4_480_1_5MG.mp4",) )
gatherFrames.start()

print(len(allImages))