



from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
from imutils import build_montages
from imutils import paths
from PIL import Image
from collections import Counter
import random

#def break(img_path):





def main():
    window_text = "Are you a robot?"
    dataset = "test_captchas"
    HXW = 24
    img_paths = list(paths.list_images(dataset))
    random.shuffle(img_paths)
    img_paths = img_paths[:2]
    model = load_model("model5.model")
    lb = pickle.loads(open("lb.pickle", "rb").read())
    for img_path in img_paths:
        print("Loading captcha:", img_path)
        filename = img_path.split(os.path.sep)[-1]
        actual_captcha = os.path.splitext(filename)[0]
        actual_chars = list(actual_captcha)
        img = img_cpy = cv2.imread(img_path)
        cv2.imshow(window_text, img)
        cv2.waitKey(500)
        print("Processing captcha")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        i = 0
        while i < 5:
            print("Threshold")
            img = cv2.adaptiveThreshold(img, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
            cv2.imshow(window_text, img)
            cv2.waitKey(100)
            img = cv2.threshold(img, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cv2.imshow(window_text, img)
            cv2.waitKey(100)
            i += 1
        print("Detecting characters")
        contours = cv2.findContours(img.copy(),
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        mont = []
        mont2 = []
        mont.append(img_cpy)
        mont2.append(img_cpy)
        detected_chars = []
        detected_chars_imgs = []
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            detected_chars_imgs.append( (x, y, w, h) )
        detected_chars_imgs = sorted(detected_chars_imgs, key=lambda x: x[0])
        print("Extracting characters")
        for box in detected_chars_imgs:
            (x, y, w, h) = box
            cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 2)
            box = img[y-2:y+h+2, x-2:x+w+2]
            detected_chars.append(box)
        decoded_captcha = ""
        for (detected_char, actual_char) in zip(detected_chars, actual_chars):
            if img.shape[0] < 10 or img.shape[1] < 10:
                print("No character detected")
                predicted_char = "?"
            else:
                print("Processing detected character")
                img = cv2.resize(detected_char, (HXW, HXW))
                img = img.astype("float") / 255.0
                img = img_to_array(img)
                img = np.expand_dims(img, axis=0)
                print("Predicting character")
                proba = model.predict(img)[0]
                idx = np.argmax(proba)
                predicted_char = lb.classes_[idx]
            decoded_captcha += predicted_char
            if predicted_char == actual_char:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            img = cv2.merge((detected_char, detected_char, detected_char))
            mont.append(img)
            montage = build_montages(mont, (128, 128), (5, 1))[0]
            cv2.imshow(window_text, montage)
            cv2.waitKey(700)
            cv2.putText(img, predicted_char, (2,10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
            mont2.append(img)
            montage2 = build_montages(mont2, (128, 128), (5, 1))[0]
            cv2.imshow(window_text, montage2)
            cv2.waitKey(700)
        if decoded_captcha == actual_captcha:
            cv2.imshow(window_text, cv2.imread("assets/passed.png"))
            cv2.waitKey(500)
        else:
            cv2.imshow(window_text, cv2.imread("assets/failed.png"))
            cv2.waitKey(500)



main()



#
