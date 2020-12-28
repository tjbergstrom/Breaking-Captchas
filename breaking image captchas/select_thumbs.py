# select_thumbs.py
#
# Select which model to use based on the decoded text from the input captcha
# Get an input list of thumbnails and use the model to predict
# If this thumbnail is or isn't ___
# And then some neat output to demonstrate how it's going


import cv2
import numpy as np
import imutils
import time
from keras.models import load_model
from keras.preprocessing.image import img_to_array


class Select:
	def __init__(self):
		self.crosswalks = load_model("models/crosswalks.model")
		self.traffic_lights = load_model("models/traffic_lights.model")
		self.fire_hydrants = None
		self.parking_meters = None
		self.school_busses = None


	def make_selections(self, txt, thumbnails, hxw=24):
		model = self.get_model(txt)
		selections = []
		thumbs, boxs = thumbnails
		for thumb in thumbs:
			img = cv2.resize(thumb, (hxw, hxw))
			img = img.astype("float") / 255.0
			img = img_to_array(img)
			img = np.expand_dims(img, axis=0)
			probs = model.predict(img)[0]
			if probs[0] > .500000:
				selections.append(1)
			else:
				selections.append(0)
		return selections


	def draw(self, img_path, thumbnails, selections, expected):
		img = cv2.imread(img_path)
		img = imutils.resize(img, width=300)
		thumbs, boxs = thumbnails
		correct = 0
		for i, box in enumerate(boxs):
			color = (0, 0, 0)
			if selections[i]:
				color = (0, 0, 255)
			(xo, xn, yo, yn) = box
			cv2.rectangle(img, (xo, yo), (xn, yn), color, 2)
			cv2.imshow("", img)
			cv2.waitKey(200)
			if selections[i] == expected[i]:
				correct += 1
		accuracy = (correct / len(expected)) * 100
		cv2.imshow(f"{accuracy:.2f}% accurate", img)
		cv2.waitKey(200)
		time.sleep(2.0)
		return correct, len(expected)


	def get_model(self, txt):
		if txt == "crosswalks":
			return self.crosswalks
		if txt == "traffic lights":
			return self.traffic_lights
		raise ValueError(f"{txt} not supported")



##
