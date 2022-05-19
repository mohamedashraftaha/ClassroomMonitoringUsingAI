from asyncio import constants
import os
from threading import Thread
import cv2
import numpy as np
import time
from skimage import data, feature
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, GlobalMaxPooling2D
from keras.layers.advanced_activations import PReLU, LeakyReLU
from keras.models import model_from_json
import boto3
import requests
import sys
import getopt
import socket
import mediapipe as mp
import math

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
class Utilities:
    def findObjects(self, mOutputs, THRESH, SUP_THRESH):
        boundingBoxLocations = []
        classes = []
        confidence = []
        for output in mOutputs:
            for prediction in output:
                classProbs = prediction[5:]
                class_id = np.argmax(classProbs)
                conf = classProbs[class_id]
                if conf > THRESH:
                    w, h = int(prediction[2] * 320), int(prediction[3] * 320)
                    x, y = int((prediction[0] * 320) - w/2), int((prediction[1] * 320)-h/2)
                    boundingBoxLocations.append([x, y, w, h])
                    confidence.append(float(conf))
                    classes.append(class_id)
        boxesToKeep = cv2.dnn.NMSBoxes(boundingBoxLocations, confidence, THRESH, SUP_THRESH, )
        return boxesToKeep, boundingBoxLocations, classes, confidence

    def showDetectedImages(self, img, boundingBoxIDs, allBoundingBoxes, classIDs, confidenceVals, widthR, heightR):
        finalLocations = []
        for i in boundingBoxIDs:
            box = allBoundingBoxes[i]
            x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            x = int(x * widthR)
            y = int(y * heightR)
            w = int(w * widthR)
            h = int(h * heightR)
            x = int(x - (w / 2))
            y = int(y - (h / 5))
            w = w * 2
            h = int(h * 1.2)
            if classIDs[i] == 0:
                finalLocations.append([x, y, w, h])
        return finalLocations

    def YOLO(self, frame, THRESH, SUP_THRESH):
        originalW, originalH = frame.shape[1], frame.shape[0]

        neuralNetwork = cv2.cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
        neuralNetwork.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        neuralNetwork.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), True, crop=False)
        neuralNetwork.setInput(blob)
        layerNames = neuralNetwork.getLayerNames()
        outputNames = [layerNames[index - 1] for index in neuralNetwork.getUnconnectedOutLayers()]
        outputs = neuralNetwork.forward(outputNames)

        predictedObjects, bBoxLocations, classIDs, convValues = self.findObjects(self, outputs, THRESH, SUP_THRESH)
        finalLocationsInFrame = self.showDetectedImages(self, frame, predictedObjects, bBoxLocations, classIDs, convValues, originalW / 320, originalH / 320)
        return finalLocationsInFrame

    def sendLocationsToDB(self, studentNumber, classInstance, X, Y, W, H):
        url = f"https://classroommonitoring.herokuapp.com/api/user/add_students_locations"
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        data = {
            "student_number": studentNumber,
            "exam_instance_id": classInstance,
            "x": X,
            "y": Y,
            "w": W,
            "h": H
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            #print("JSON Response ", response.json()['status'])
            if response.json()['status'] != 'success':
                pass
#                print("An error has occured")
            else:
                pass
#                print("student added successfully")

class ProcessingStudent:
    def __init__(self, locations, sensitivity, classInstance):
        self.locations = locations
        self.sensitivity = sensitivity
        self.classInstance = classInstance
        self.cheatingInstance = 1
        # for l in range(len(self.locations)):
        #     self.cheatingInstance.append(1)

        self.loaded_model = keras.models.Sequential()
        self.loaded_model = Sequential()
        self.loaded_model.add(Conv2D(32, (4, 4), activation='relu', input_shape=(256, 256, 1)))
        self.loaded_model.add(MaxPooling2D(pool_size=(2, 2)))
        self.loaded_model.add(Dropout(0.25))
        self.loaded_model.add(Conv2D(64, (3, 3), activation='relu'))
        self.loaded_model.add(MaxPooling2D(pool_size=(2, 2)))
        self.loaded_model.add(Dropout(0.25))
        self.loaded_model.add(Flatten())
        self.loaded_model.add(Dense(128, activation='relu'))
        self.loaded_model.add(Dense(4, activation='softmax'))

        self.loaded_model.load_weights("ModelHOG___Date_Time_2022_05_06__23_58_33___Loss_0.77988600730896___Accuracy_0.82666015625.h5")
        self.loaded_model.compile(loss = 'categorical_crossentropy', optimizer= 'adam', metrics = ['accuracy'])
        
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
        self.mp_drawing = mp.solutions.drawing_utils 

    def hog(self, image):
        hogImage = cv2.resize(image, (256, 256))
        hogImage = cv2.cvtColor(hogImage, cv2.COLOR_RGB2GRAY)
        hogVector, hogImage = feature.hog(hogImage, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2', visualize=True)
        hogImage = hogImage.reshape((1,) + hogImage.shape)
        hogImage = np.transpose(hogImage)
        hogImage = hogImage.reshape((1,) + hogImage.shape)
        hogImage = np.asarray(hogImage)
        return hogImage

    def sendToDB(self, filePath, fileName):
 
        pass
        
        # client = boto3.client('s3', aws_access_key_id='AKIAWKAZELKAIHEHAREM', aws_secret_access_key='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')
        # bucket = 'classroommonitoring'
        # bucket_file_path = str(fileName)
        # client.upload_file(filePath, bucket, bucket_file_path, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'})
        # print(" ########## Case frame uploaded successfully ###################")
        # time.sleep(8)
        # #print(" Waiting for next case ...")

    def imwriteToJPG(self, image, classInstance, studentNumber, studentsCheatingInstance):
        fileName = "c" + str(studentsCheatingInstance) + "-" + classInstance + "-" + str(studentNumber) + ".jpg"
  #      cv2.imwrite(fileName, image)
        print(type(image))
        image_string = cv2.imencode('.jpg', image)[1].tostring()     
        client = boto3.client('s3', aws_access_key_id='AKIAWKAZELKAIHEHAREM', aws_secret_access_key='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')
        bucket = 'classroommonitoring'
        client.put_object(Bucket=bucket, Key = fileName, Body =image_string, ContentType= 'image/jpeg', ACL= 'public-read') 
        # print("Frame uploaded")
        print(" ########## Case frame uploaded successfully ###################")
     #   time.sleep(8)
        time.sleep(0.5)
        studentsCheatingInstance += 1
        studentNumber+=1    
        return fileName, studentsCheatingInstance

    def detectPose(self, image):

        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imageRGB)
        landmarks = []
        if results.pose_landmarks:
             #   self.mp_drawing.draw_landmarks(output_image, landmark_list=results.pose_landmarks, connections = self.mp_pose.POSE_CONNECTIONS)
                height, width, _ = image.shape
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append((int(landmark.x * width), int(landmark.y * height)))
        return landmarks

    def calcDistance(self, noseLandmark, leftLandmark, rightLandmark):
        x1, y1= noseLandmark 
        x2, y2= leftLandmark
        x3, y3= rightLandmark 
        distance = math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2)
        distance2 = math.sqrt( (x1 - x3) ** 2 + (y1 - y3) ** 2)
        return abs(distance-distance2)


    def mediaPipe(self, image):
        landmarks = self.detectPose(image)
        if landmarks:
            distance = self.calcDistance(landmarks[self.mp_pose.PoseLandmark.NOSE.value],landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value] , landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
            print('distance', distance)
            if(distance > 75):
                return True, distance
            else:
                return False, distance
        else:
            return False, 0

    def predict(self, frames, studentNumber, X, Y, W, H):
        
        confValues = []
        distances = []
        studentCropImages = []
        for frame in frames:
            studentCrop = frame[int(Y): int(Y + H), int(X): int(X + W)]
            studentCropImages.append(studentCrop)
            flagMP, distance = self.mediaPipe(studentCrop)
            if(flagMP):
                distances.append(distance/100)
                confValues.append(1)
            else:
                hogImage = self.hog(studentCrop)
                pred = (self.loaded_model.predict(hogImage)[0][0:3])
                maxClass = max(pred)
                confValues.append(maxClass)
    #    print("Student Number: ", studentNumber)
        if confValues:
            q75, q25 = np.percentile(confValues, [75, 25])
            iqr = q75 - q25
            low = q25 - (1.5 * iqr)
            up = q75 + (1.5 * iqr)
            filteredConfValues = []
            filteredConfIndeces = []
            for i in confValues:
                #print("modelpred ",i, "  model pred  ")
                if (i >= low) and (i <= up):
                    filteredConfValues.append(i)
                    filteredConfIndeces.append(confValues.index(i))
            confValues = np.asarray(confValues)
            avgConf = np.average(filteredConfValues)
            if(avgConf >= 0.05):
                print("Creating Case")
                url ='https://classroommonitoring.herokuapp.com/api/user/create_possible_case'
                headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
                student_num  = studentNumber + 1 
                print (self.cheatingInstance ,student_num   ,str(sum) )
                data = {
                    "case_id": self.cheatingInstance ,
                    "exam_instance_id": self.classInstance,
                    "student_number": student_num,
                    "confidence": str(sum)
                }


                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    print("JSON Response ", response.json()['status'])
                    if response.json()['status'] != 'success':
                        print("An error has occured", response.json())
        
                    else:
                        print("case created successfully")
                        
                # print(distances.index(max(distances)))        
                fileName, self.cheatingInstance = \
                self.imwriteToJPG(studentCropImages[distances.index(max(distances))], \
                self.classInstance, student_num , self.cheatingInstance)
            #  self.sendToDB(fileName, fileName)


    def runThreading(self, frames):
        studentThreads = []
        for l in self.locations:
            t = Thread(target = self.predict, args=(frames, self.locations.index(l), l[0], l[1], l[2], l[3]))
            t.start()
            studentThreads.append(t)

        for st in studentThreads:
            st.join()

    def runSequential(self, frames):
        for l in self.locations:
            self.predict(frames, self.locations.index(l), l[0], l[1], l[2], l[3])

########################################################################################################################
frameRate = None
sensitivity = None
classInstanceID = None
########################################################################################################################
utils = Utilities

YOLO_THRESH = 0.1
YOLO_SUPPRESSION_THRESH = 0.1

feedEnd = False
allImages = []
frameCount = 0

def retrieveFrames(source):
    global feedEnd
    cap = cv2.VideoCapture(source)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            allImages.append(frame)
        else:
            break
    feedEnd = True;
    # print("done")
    # print(len(allImages))

def yolo2sec(frameRate):
    global frameCount
    print("Yolo Running")
    frameInit = frameCount
    start_time = time.time()
    maxLocations = []
    while(frameCount < frameRate * 2):
        if(frameRate % frameRate) == 0:
            tempLocations = utils.YOLO(Utilities, allImages[frameCount], YOLO_THRESH, YOLO_SUPPRESSION_THRESH)
            if(len(tempLocations) > len(maxLocations)):
                maxLocations = tempLocations
        frameCount = frameCount + 1

    duration = time.time() - start_time
#    frameCount = frameInit + (frameRate * int(duration))
    print("--- %s seconds ---" % (time.time() - start_time))
    return maxLocations, frameCount


def examVariables():
    """@brief: This function is responsible for retrieving sensitivity, exam instance id & fps"""
    sensitivity_arg = None
    exam_instance_id_arg = None
    fps = None
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 's:e:v:')
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

if __name__ == "__main__":
    sensitivity, frameRate, classInstanceID = examVariables()
    frameRate=frameRate
    gatherFrames = Thread(target = retrieveFrames, args = ("/home/cse-p07-g06f/Downloads/t12.mp4",) )
    gatherFrames.start()

    time.sleep(1)
    studentLocations, frameCount = yolo2sec(frameRate)
    print("Students Found: ",len(studentLocations))

    for l in studentLocations:
        utils.sendLocationsToDB(Utilities, (studentLocations.index(l) + 1), classInstanceID, l[0], [1], l[2], l[3])

    processing = ProcessingStudent(studentLocations, sensitivity, classInstanceID)
    frameCount = frameCount + frameRate

    while(True):
        check = feedEnd is True and frameCount >= len(allImages)
      #  print(frameCount, check, sep='\t')
        if check is True:
            break
        response = requests.get(f"https://classroommonitoring.herokuapp.com/api/user/check_exam_ended/{classInstanceID}")
      #  print(response.json())
      #  print(response.json()['data'])
        if (response.json()['data'] == "exam ended"):
            break
        if(frameCount % (frameRate) == 0):
            # processing.runThreading(allImages[frameCount - frameRate: frameCount])
            processing.runSequential(allImages[frameCount - (frameRate): frameCount])
        frameCount = frameCount + 1

    gatherFrames.join()
