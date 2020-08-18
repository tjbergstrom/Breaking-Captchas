# pre_process.py
# August 2020
# Experimenting how to use the trained model to break the captchas
# And how to translate the output to something useful and meaningful


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


dataset = "test_captchas"
HXW = 24
data = []
labels = []
img_paths = sorted(list(paths.list_images(dataset)))
img_show = False
model = load_model("model.model")
lb = pickle.loads(open("lb.pickle", "rb").read())
total_correct = 0

print()

# Load each original captcha
for img_path in img_paths:
    filename = img_path.split(os.path.sep)[-1]
    filename = os.path.splitext(filename)[0]
    filename_cpy = filename
    digits = list(filename)
    # Extract each char from the captcha
    img = cv2.imread(img_path)
    img_cpy = img
    if img_show:
        cv2.imshow(filename_cpy, img)
        cv2.waitKey(0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img_show:
        cv2.imshow("gray scale", img)
        cv2.waitKey(0)
    img = cv2.threshold(img, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    if img_show:
        cv2.imshow("threshold", img)
        cv2.waitKey(0)
    contours = cv2.findContours(img.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    digit_boxs = []
    tmp_data = []
    tmp_labels = []
    boxs = []
    labels = []
    # Make sure the chars are sorted from left to right
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        boxs.append( (x, y, w, h) )
        #print(x, y, w, h)
    boxs = sorted(boxs, key=lambda x: x[0])
    # Save the char and its corresponding label to lists
    for (box, digit) in zip(boxs, digits):
        (x, y, w, h) = box
        cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 2)
        box = img[y-2:y+h+2, x-2:x+w+2]
        tmp_data.append(box)
        tmp_labels.append(digit)
        if img_show:
            cv2.imshow(digit, box)
            cv2.waitKey(0)
    if len(tmp_data) != 4:
        continue
    decoded_captcha = ""
    for (img, label) in zip(tmp_data, tmp_labels):
        if img.shape[0] < 10 or img.shape[1] < 10:
            continue
        img = cv2.resize(img, (HXW, HXW))
        img = img.astype("float") / 255.0
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        data.append(img)
        #labels.append(label)
        proba = model.predict(img)[0]
        idx = np.argmax(proba)
        label = lb.classes_[idx]
        labels.append(label)
        #print(label)
        decoded_captcha += label
    print("Filename:", img_path)
    if decoded_captcha == filename_cpy:
        decoded_captcha += " - correct"
        total_correct += 1
        #print("correct")
    else:
        decoded_captcha += " - wrong"
        #print("wrong")
    print("    Decoded captcha is:", decoded_captcha, "\n")
    #cv2.imshow(decoded_captcha, img_cpy)
    #cv2.waitKey(0)
    mont = []
    mont2 = []
    mont.append(img_cpy)
    mont2.append(img_cpy)
    for (box, label, img) in zip(boxs, labels, tmp_data):
        (startX, startY, endX, endY) = box
        #cv2.rectangle(img_cpy, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(img_cpy, label, (startX, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

        #cv2.imshow(decoded_captcha, img_cpy)
        #cv2.waitKey(0)
        #cv2.imshow(label, img)
        #cv2.waitKey(0)
        '''img2 = np.zeros_like(img)
        img2[:,:,0] = img
        img2[:,:,1] = img
        img2[:,:,2] = img
        img = Image.convert('RGB')'''
        img2 = img
        img = cv2.merge((img, img, img))
        img2 = cv2.merge((img2, img2, img2))
        mont2.append(img2)
        cv2.putText(img, label, (2,10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
        mont.append(img)
    #mont.append(img_cpy)
    #mont2.append(img_cpy)
    montage = build_montages(mont, (128, 128), (5, 1))[0]
    montage2 = build_montages(mont2, (128, 128), (5, 1))[0]
    #cv2.imshow(decoded_captcha, montage2)
    #cv2.waitKey(0)
    #cv2.imshow(decoded_captcha, montage)
    #cv2.waitKey(0)
    cv2.imshow(decoded_captcha, img_cpy)
    cv2.waitKey(0)


accuracy = (total_correct / len(img_paths)) * 100
accuracy = str(accuracy) + "%"
print(total_correct, "correct out of", len(img_paths), accuracy)






#
