from threading import Thread
import time
from skimage import data, feature
import cv2
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np

class ProcessingStudent:
    def __init__(self, locations, sensitivity):
        self.locations = locations
        self.sensitivity = sensitivity

        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights("model.h5")
        self.loaded_model.compile(loss = 'categorical_crossentropy', optimizer= 'adam', metrics = ['accuracy'])

    def hog(self, image):
        hogImage = cv2.resize(image, (256, 256))
        hogImage = cv2.cvtColor(hogImage, cv2.COLOR_RGB2GRAY)
        hogVector, hogImage = feature.hog(hogImage, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2', visualize=True)
        return hogImage

    # def sendToDB(self, frames):

    def predict(self, frames, X, Y, W, H):
        confValues = []
        for frame in frames:
            studentCrop = frame[int(Y - H / 2): int(Y - H / 2 + H), int(X - W / 2): int(X - W / 2 + W)]
            hogImage = self.hog(studentCrop)
            confValues.append(np.argmax(self.loaded_model.predict(hogImage)))

        q75, q25 = np.percentile(confValues, [75, 25])
        iqr = q75 - q25
        low = q25 - (1.5 * iqr)
        up = q75 + (1.5 * iqr)
        filteredConfValues = []
        for i in range(len(confValues)):
            if (confValues[i] >= low) and (confValues[i] <= up):
                filteredConfValues.append(confValues[i])
        avgConf = np.average(filteredConfValues)

        if(avgConf >= self.sensitivity):
            # send to bucket


    def runThreading(self, frames):
        studentThreads = []
        for l in self.locations:
            t = Thread(target = self.predict, args=(frames, l[0], l[1], l[2], l[3]))
            t.start()
            studentThreads.append(t)

        for st in studentThreads:
            st.join()

    def runSequential(self, frames):
        for l in self.locations:
            self.predict(frames, l[0], l[1], l[2], l[3])


