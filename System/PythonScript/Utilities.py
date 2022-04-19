import cv2
import numpy as np

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
                    x, y = int((prediction[0] * 320) - w / 2), int((prediction[1] * 320) - h / 2)
                    boundingBoxLocations.append([x, y, w, h])
                    confidence.append(float(conf))
                    classes.append(class_id)
        boxesToKeep = cv2.dnn.NMSBoxes(boundingBoxLocations, confidence, THRESH, SUP_THRESH, )
        return boxesToKeep, boundingBoxLocations, classes, confidence

    def showDetectedImages(self, img, boundingBoxIDs, allBoundingBoxes, classIDs, confidenceVals, widthR, heightR, finalLocations):
        for i in boundingBoxIDs:
            box = allBoundingBoxes[i]
            x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            x = int(x * widthR)
            y = int(y * heightR)
            w = int(w * widthR)
            h = int(h * heightR)
            if classIDs[i] == 0:
                classWithConf = 'Person - ' + str(int(confidenceVals[i] * 100)) + '%'
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 10)
                cv2.putText(img, classWithConf, (x + 5, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0))
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
