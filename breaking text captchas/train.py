# train.py
# A variation of the scripts I usually run for ML projects
#
# source ./venv1/bin/activate
# python3 -W ignore train.py


from sklearn.preprocessing import LabelBinarizer
from process import Pprocess
from net import Butterfly_Net
from net import Spiderweb_Net
from results import Result
from tuning import Tune
import numpy as np
import argparse
import pickle


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--savemodel", type=str, default="model.model")
ap.add_argument("-p", "--plot", type=str, default="plot.png")
ap.add_argument("-d", "--dataset", type=str, default="train_captchas")
ap.add_argument("-a", "--aug", type=str, default="original")
ap.add_argument("-m", "--model", type=str, default="Butterfly_Net")
ap.add_argument("-o", "--opt", type=str, default="Adam2")
ap.add_argument("-i", "--imgsz", type=str, default="xs")
ap.add_argument("-e", "--epochs", type=int, default=20)
ap.add_argument("-b", "--bs", type=str, default="m")
ap.add_argument("-k", "--kernelsize", type=int, default=3)
args = vars(ap.parse_args())


EPOCHS = args["epochs"]
BS = Tune.batch_size(args["bs"])
HXW = Tune.img_size(args["imgsz"])
k = args["kernelsize"]
notes = "\n** with adaptive threshold **\n"


print("\n...pre-processing the data...\n")
(data, cl_labels) = Pprocess.pre_process(args["dataset"], HXW)
lb = LabelBinarizer()
cl_labels = lb.fit_transform(cl_labels)
num_classes = len(lb.classes_)
loss_type = "categorical_crossentropy"
(trainX, testX, trainY, testY) = Pprocess.split(data, np.array(cl_labels), num_classes)
aug = Pprocess.data_aug(args["aug"])

print("\n...building the model...\n")
if args["model"] == "Spiderweb_Net":
    model = Spiderweb_Net.build(width=HXW, height=HXW, depth=1, k=k, classes=num_classes)
else:
    model = Butterfly_Net.build(width=HXW, height=HXW, depth=1, k=k, classes=num_classes)
opt = Tune.optimizer(args["opt"], EPOCHS)
model.compile(loss=loss_type, optimizer=opt, metrics=["accuracy"])

print("\n...training the model...\n")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS, epochs=EPOCHS, verbose=1)
model.save(args["savemodel"] )
f = open("lb.pickle", "wb")
f.write(pickle.dumps(lb))
f.close()

print("\n...getting results of training & testing...\n")
Result.save_info(args["model"], args["opt"], args["aug"], args["imgsz"], EPOCHS, BS, HXW, notes)
predictions = model.predict(testX, batch_size=BS)
Result.display_metrix(testX, testY, predictions, model, lb.classes_, aug, BS)
Result.display_plot((args["plot"]), EPOCHS, H)



#
