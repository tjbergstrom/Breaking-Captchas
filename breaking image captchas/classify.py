# classify.py
# $ python3 classify.py
#
# Dec. 27 2020
# Currently this is just using some tricks to extract image thumbnails from a captcha
# And also extract the title text - what boxes it wants you to select
# Just weeing how to do this before moving on


import cv2
import os
from imutils import paths
import numpy as np
import statistics
import pytesseract
import time
import sys


def img_show(img, t=0, show=1):
    if show:
        cv2.imshow("", img)
        cv2.waitKey(t)


def y_box_coords(img):
    white_line = True
    upper_y_coords = []
    lower_y_coords = []
    lower_y = 0
    for y in range(0, img.shape[0]):
        x_line = []
        for x in range(0, img.shape[1]):
            x_line.append(img[y,x])
        x_line = statistics.mean(x_line)
        if x_line > 180:
            if not white_line:
                lower_y = y
            white_line = True
        elif white_line:
            white_line = False
            upper_y_coords.append(y)
            lower_y_coords.append(lower_y)
    upper_y_coords.pop(0)
    upper_y_coords.pop()
    lower_y_coords.pop(0)
    lower_y_coords.pop(0)
    return upper_y_coords, lower_y_coords


def x_box_coords(img, upper_y_coords, lower_y_coords):
    white_line = True
    left_x_coords = []
    right_x_coords = []
    right_x = 0
    for x in range(0, img.shape[1]):
        y_line = []
        for y in range(upper_y_coords[0], lower_y_coords[len(lower_y_coords)-1]):
            y_line.append(img[y,x])
        y_line = statistics.mean(y_line)
        if y_line > 180:
            if not white_line:
                right_x = x
            white_line = True
        elif y_line > 90:
            continue
        elif white_line:
            white_line = False
            left_x_coords.append(x)
            right_x_coords.append(right_x)
    right_x_coords.append(right_x)
    right_x_coords.pop(0)
    return left_x_coords, right_x_coords


def extract_thumbs(img_path):
    img = cv2.imread(img_path)
    img_cpy = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img , 225, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    img_contours = np.zeros(img.shape)
    cv2.drawContours(img_contours, contours, -1, (255,255,255), 3)
    cv2.imwrite("tmp.png", img_contours)
    img = cv2.imread("tmp.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_show(img, t=600)

    upper_y_coords, lower_y_coords = y_box_coords(img)
    left_x_coords, right_x_coords = x_box_coords(img, upper_y_coords, lower_y_coords)

    boxs = []
    thumbs = []
    for start_y, end_y in zip(upper_y_coords, lower_y_coords):
        for start_x, end_x in zip(left_x_coords, right_x_coords):
            if end_x - start_x < 0 or end_y - start_y < 0:
                continue
            boxs.append((start_x, end_x, start_y, end_y))
            thumbs.append(img_cpy[start_y:end_y, start_x:end_x])
            cv2.rectangle(img_cpy, (start_x, start_y), (end_x, end_y), (255, 0, 215), 2)
            img_show(img_cpy, t=100)
    return thumbs, boxs


def extract_txt(img_path):
    img = cv2.imread(img_path)
    img = img[0:img.shape[0]//4, 0:img.shape[1]]
    img_cpy = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    txt = [i for i in details.get("text") if len(i) > 2]
    captcha = ""
    captcha_dictionary = [
        "crosswalk", "crosswalks",
        "traffic light", "traffic lights", "traffic", "lights",
        "fire hydrant", "fire hydrants", "fire", "hydrant", "hydrants",
        "parking meter", "parking meters",
        "bus", "busses", "school bus", "school busses",
    ]
    for t in txt:
        if t in captcha_dictionary:
            captcha = t
            break
    if captcha == "traffic":
        captcha = "traffic light"
    img_show(img, t=600)
    cv2.putText(img_cpy, captcha, (10, img_cpy.shape[0]//2), 0, 1, (0, 0, 255), 3)
    img_show(img_cpy, t=600)
    return captcha


if __name__ == "__main__":
    dataset = "test_uploads"
    img_paths = sorted(list(paths.list_images(dataset)))
    for img_path in img_paths:
        captcha_txt = extract_txt(img_path)
        if not captcha_txt:
            continue
        thumbnails = extract_thumbs(img_path)
        if len(thumbnails) < 6:
            continue
        img_path = img_path.split(os.path.sep)[-1]
        expected_selections = list(os.path.splitext(img_path))[0]
        make_selections(thumbnails, expected_selections)



##
