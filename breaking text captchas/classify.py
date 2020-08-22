# classify.py
# August 2020
# Experimenting how to use the trained model to break the captchas
# And how to translate the output to something useful and meaningful
#
# This has optional bools for displaying images, to see how the model is making predictions
#
# However this is most useful for processing thousands of test captchas
# And reporting an accuracy rate, how many the model was able to break
#
# Also has some other informational metrics to see how the model is performing
#
# source ./venv1/bin/activate
# python3 -W ignore classify.py


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


dataset = "test_captchas"
HXW = 24
data = []
labels = []
img_paths = sorted(list(paths.list_images(dataset)))
img_show = False
model = load_model("model5.model")
lb = pickle.loads(open("lb.pickle", "rb").read())
total_correct = 0
incorrect_chs = []
display_montage = False
display_results = False
print()


# Load each original captcha
for img_path in img_paths:
    filename = img_path.split(os.path.sep)[-1]
    filename = os.path.splitext(filename)[0]
    filename_cpy = filename
    chars = list(filename)
    # Extract each char from the captcha
    img = cv2.imread(img_path)
    img_cpy = img
    if img_show:
        cv2.imshow(filename_cpy, img)
        cv2.waitKey(0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    i = 0
    while i < 5:
        img = cv2.adaptiveThreshold(img, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        img = cv2.threshold(img, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        i += 1
    if img_show:
        cv2.imshow("threshold", img)
        cv2.waitKey(0)
    contours = cv2.findContours(img.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    tmp_data = [] # This will be a list of the extracted images of the chars, after formatting
    tmp_labels = [] # This ended up not used here
    boxs = [] # This is the list of raw extracted images of the chars
    labels = [] # This will be for comparing accuracy of each individual char, if a decoding is wrong
    # Make sure the chars are sorted from left to right
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        boxs.append( (x, y, w, h) )
        #print(x, y, w, h)
    boxs = sorted(boxs, key=lambda x: x[0])
    # Save the char and its corresponding label to lists
    for (box, ch) in zip(boxs, chars):
        (x, y, w, h) = box
        cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 2)
        box = img[y-2:y+h+2, x-2:x+w+2]
        tmp_data.append(box)
        tmp_labels.append(ch)
        if img_show:
            cv2.imshow(ch, box)
            cv2.waitKey(0)
    if len(tmp_data) != 4:
        continue
    decoded_captcha = ""
    # Make a prediction for each char and concat that char to the decoded captcha string
    for (img, label, ch) in zip(tmp_data, tmp_labels, chars):
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
    if display_results:
        print("Filename:", img_path)
    if decoded_captcha == filename_cpy:
        decoded_captcha += " - correct"
        total_correct += 1
    else:
        #print("incorrect -", filename_cpy)
        decoded_captcha += " - wrong"
        # figure out which char(s) came out wrong
        for (label, ch) in zip(labels, chars):
            if label != ch:
                #print("Predicted:", label, "actual:", ch)
                incorrect_chs.append(ch)
    if display_results:
        print("    Decoded captcha is:", decoded_captcha, "\n")
    if img_show:
        cv2.imshow(decoded_captcha, img_cpy)
        cv2.waitKey(0)
    # This will display the original image with the threshold and the extracted chars
    # It's only informational, and only if you are testing with a few inputs (not thousands)
    if display_montage:
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


# This is another interesting metric I wanted to see
# Which characters A through Z and 1 through 9 were the most and least accurate
if display_results:
    incorrect_counts = []
    print("\nHow many times each character was predicted incorrectly")
    vals = Counter(incorrect_chs).values()
    keyz = Counter(incorrect_chs).keys()
    incorrect_counts = list(zip(vals, keyz))
    for val in sorted(incorrect_counts):
        print(val)



#
