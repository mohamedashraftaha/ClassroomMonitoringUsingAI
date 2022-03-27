from threading import Thread
import time
from skimage import data, feature
import cv2

class ProcessingStudent:
    def __init__(self, studentNumber, X, Y, W, H, image, sensitivity):
        self.image = image[int(Y - H / 2): int(Y - H / 2 + H), int(X - W / 2): int(X - W / 2 + W)]
        self.studentNumber = studentNumber
        self,sensitivity = sensitivity

# def backgroundRemoval(self,):

def hog(self,):
    # self.image = backgroundRemoval()
    self.image = cv2.resize(self.image, (256, 256))
    self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
    hogVector, hogImage = feature.hog(self.image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2', visualize=True)
    return hogImage

# def predict(self,):

# def sendToDB(self,):