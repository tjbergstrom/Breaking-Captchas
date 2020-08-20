# process.py
# August 2020
# A variation of the processing I usually do for ML nets


from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import numpy as np
import random
import cv2
import os


class Pprocess:


    def pre_process(dataset, HXW):
        data = []
        labels = []
        img_paths = sorted(list(paths.list_images(dataset)))
        #random.seed(42)
        random.shuffle(img_paths)
        # Load each original captcha
        for img_path in img_paths:
            filename = img_path.split(os.path.sep)[-1]
            filename = os.path.splitext(filename)[0]
            digits = list(filename)
            # Extract each char from the captcha
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            i = 0
            while i < 5:
                img = cv2.adaptiveThreshold(img, 255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
                img = cv2.threshold(img, 0, 255,
                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                i += 1
            contours = cv2.findContours(img.copy(),
                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0]
            digit_boxs = []
            tmp_data = []
            tmp_labels = []
            boxs = []
            # Make sure the extracted chars are sorted from left to right
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                boxs.append( (x, y, w, h) )
            boxs = sorted(boxs, key=lambda x: x[0])
            # Save the char and its corresponding label to lists
            for (box, digit) in zip(boxs, digits):
                (x, y, w, h) = box
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 2)
                box = img[y-2:y+h+2, x-2:x+w+2]
                tmp_data.append(box)
                tmp_labels.append(digit)
            if len(tmp_data) != 4:
                continue
            # Other regular data pre-processing
            for (img, label) in zip(tmp_data, tmp_labels):
                if img.shape[0] < 10 or img.shape[1] < 10:
                    continue
                img = cv2.resize(img, (HXW, HXW))
                img = img_to_array(img)
                data.append(img)
                labels.append(label)
        data = np.array(data, dtype="float") / 255.0
        print(len(data), len(labels))
        return data, labels


    def split(data, labels, num_classes):
        (trainX, testX, trainY, testY) = train_test_split(data,
		    labels, test_size=0.20, random_state=42)
        if num_classes == 2:
            trainY = to_categorical(trainY, num_classes=num_classes)
            testY = to_categorical(testY, num_classes=num_classes)
        return trainX, testX, trainY, testY


    def data_aug(aug):
        if aug == "original":
            return ImageDataGenerator(rotation_range=30, width_shift_range=0.2,
            height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, fill_mode="nearest")
        elif aug == "light":
            return ImageDataGenerator(rotation_range=15, width_shift_range=0.1,
            height_shift_range=0.1, shear_range=0.1, zoom_range=0.1, fill_mode="nearest")
        elif aug == "heavy":
            return ImageDataGenerator(rotation_range=45, width_shift_range=0.3,
            height_shift_range=0.2, shear_range=0.3, zoom_range=0.3, fill_mode="nearest")
        else:
            return ImageDataGenerator()



#
