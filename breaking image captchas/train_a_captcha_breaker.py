


from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import numpy as np
import random
import cv2
import sys
import os
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.models import Sequential
from keras.layers.core import Dense
from keras import backend as K
from keras.callbacks import LearningRateScheduler
from keras.optimizers import Adadelta
from keras.optimizers import RMSprop
from keras.optimizers import Adam
from keras.optimizers import SGD
from collections import OrderedDict
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from keras import metrics
import numpy as np
import pickle
import time
import matplotlib
matplotlib.use("Agg")



def process(captcha, hxw):
	data = []
	labels = []
	img_paths = list(paths.list_images(f"dataset/{captcha}/{captcha}"))
	img_paths += list(paths.list_images(f"dataset/{captcha}/not_{captcha}"))
	random.seed(79)
	random.shuffle(img_paths)
	for img_path in img_paths:
		img = cv2.imread(img_path)
		img = cv2.resize(img, (hxw, hxw))
		img = img_to_array(img)
		data.append(img)
		label = img_path.split(os.path.sep)[-2]
		labels.append(label)
	data = np.array(data, dtype="float") / 255.0
	return data, labels


def split(data, labels, num_classes, test_size=0.2):
	labels = np.array(labels)
	(train_x, test_x, train_y, test_y) = train_test_split(
		data, labels,
		test_size=test_size,
		random_state=64)
	if num_classes == 2:
		train_y = to_categorical(train_y, num_classes=num_classes)
		test_y = to_categorical(test_y, num_classes=num_classes)
	return train_x, test_x, train_y, test_y


def data_aug(aug="default"):
	aug = ImageDataGenerator(
		horizontal_flip=True, fill_mode="nearest",
		rotation_range=15, shear_range=0.1, zoom_range=0.1,
		width_shift_range=0.1, height_shift_range=0.1)
	return aug


def optimizer(epochs):
	#return Adam(lr=0.001, decay=0.001/epochs, amsgrad=True)
	return Adam(lr=0.001, beta_1=0.9, beta_2=0.999, amsgrad=True)
	#return Adadelta(lr=1.0, rho=0.9)


def fitgen(model, aug, num_epochs, bs, dataset):
	(train_x, test_x, train_y, test_y) = dataset
	hist = model.fit_generator(
		aug.flow(train_x, train_y, batch_size=bs),
		validation_data=(test_x, test_y),
		steps_per_epoch=len(train_x)//bs,
		epochs=num_epochs,
		class_weight=[1.0,1.0],
		shuffle=False,
		verbose=2)
	return hist


def metrix(test_x, test_y, predictions, model, classes, aug):
	cr = classification_report(
		test_y.argmax(axis=1),
		predictions.argmax(axis=1),
		target_names=classes)
	print(cr)


class JustaNet:
	def build(w, h, k=3, d=3, classes=2):
		model = Sequential()
		input_shape = (h, w, d)
		if K.image_data_format() == "channels_first":
			input_shape = (d, h, w)
		model.add(Conv2D(32, (k, k), padding="same", input_shape=input_shape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))
		model.add(Conv2D(64, (k, k), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))
		model.add(Conv2D(128, (k, k), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))
		model.add(Conv2D(264, (k, k), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
		model.add(Dropout(0.2))
		model.add(Flatten())
		model.add(Dense(512))
		model.add(Activation("relu"))
		model.add(Dense(classes))
		model.add(Activation("softmax"))
		return model


if __name__ == "__main__":
	captcha = "traffic_lights"
	bs = 16
	hxw = 24
	epochs = 24
	data, labels = process(captcha, hxw)
	lb = LabelBinarizer()
	labels = lb.fit_transform(labels)
	num_classes = len(lb.classes_)
	loss = "binary_crossentropy"
	dataset = split(data, labels, num_classes)
	(train_x, test_x, train_y, test_y) = dataset
	aug = data_aug()
	model = JustaNet.build(hxw, hxw, classes=num_classes)
	opt = optimizer(epochs)
	model.compile(loss=loss, optimizer=opt, metrics=["accuracy"])
	hist = fitgen(model, aug, epochs, bs, dataset)
	model.save(f"models/{captcha}.model")
	predictions = model.predict(test_x, batch_size=bs)
	metrix(test_x, test_y, predictions, model, lb.classes_, aug)



##
