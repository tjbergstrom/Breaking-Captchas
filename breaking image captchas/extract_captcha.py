# extract_captcha.py
#
# This is the Computer Vision magic
#
# - OpenCV to get contours, threshold, etc
# - My own algorithms to find and extract the thumbnails (not perfect, needs work)
# - Tessaract to extract the text (which object is the captcha asking you to select)


import cv2
import os
from imutils import paths
import numpy as np
import statistics
import pytesseract
import time
import sys
import imutils


class Extract:
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


    def process(img_path):
        img = cv2.imread(img_path)
        img = imutils.resize(img, width=300)
        Extract.img_show(img, t=600)
        img_cpy = img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img , 225, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        img_contours = np.zeros(img.shape)
        cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 3)
        cv2.imwrite("tmp.png", img_contours)
        img = cv2.imread("tmp.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Extract.img_show(img, t=600)
        return img, img_cpy


    def extract_thumbs(img_path):
        img, img_cpy = Extract.process(img_path)

        upper_y_coords, lower_y_coords = Extract.y_box_coords(img)
        left_x_coords, right_x_coords = Extract.x_box_coords(img, upper_y_coords, lower_y_coords)

        boxs = []
        thumbs = []
        for start_y, end_y in zip(upper_y_coords, lower_y_coords):
            for start_x, end_x in zip(left_x_coords, right_x_coords):
                if end_x - start_x < 24 or end_y - start_y < 24:
                    continue
                boxs.append((start_x, end_x, start_y, end_y))
                thumbs.append(img_cpy[start_y:end_y, start_x:end_x])
        return thumbs, boxs


    def extract_txt(img_path):
        img = cv2.imread(img_path)
        img = imutils.resize(img, width=300)
        Extract.img_show(img, t=600)
        img = img[0:img.shape[0]//4, 0:img.shape[1]]
        img_cpy = img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        img = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        txt = [i.lower() for i in details.get("text") if len(i) > 2]
        captcha = ""
        for t in txt:
            if Extract.captcha_dictionary(t):
                captcha = Extract.captcha_dictionary(t)
                break
        if not captcha:
            return 0
        Extract.img_show(img, t=600)
        cv2.putText(img_cpy, captcha, (10, img_cpy.shape[0]//2), 0, 1, (0, 0, 255), 3)
        Extract.img_show(img_cpy, t=600)
        return captcha


    def extract_expected(img_path):
        filename = img_path.split(os.path.sep)[-1]
        expected = os.path.splitext(filename)[0]
        return [int(i) for i in expected]


    def captcha_dictionary(txt):
        captchas = {
            "crosswalk"     : "crosswalks",
            "crosswalks"    : "crosswalks",
            "traffic"       : "traffic lights",
            "twaffic"       : "traffic lights",
            "taffic"        : "traffic lights",
            "lights"        : "traffic lights",
            "traffic light" : "traffic lights",
            "traffic lights": "traffic lights",
            "fire"          : "fire hydrants",
            "hydrant"       : "fire hydrants",
            "hydrants"      : "fire hydrants",
            "fire hydrant"  : "fire hydrants",
            "fire hydrants" : "fire hydrants",
            "parking"       : "parking meters",
            "meter"         : "parking meters",
            "meters"        : "parking meters",
            "parking meter" : "parking meters",
            "parking meters": "parking meters",
            "school"        : "school busses",
            "bus"           : "school busses",
            "buses"         : "school busses",
            "busses"        : "school busses",
            "school bus"    : "school busses",
            "school buses"  : "school busses",
            "school busses" : "school busses",
        }
        implemented = [
            "crosswalks", "traffic lights",
        ]
        if txt in captchas:
            if captchas.get(txt) in implemented:
                return captchas.get(txt)
        return 0



##
