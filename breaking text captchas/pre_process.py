# pre_process.py
# August 2020
# Experimenting with extracting characters from a captcha image


#####################################
#
# P$UED0 C0DE
#
#   load image paths
#   for path in image paths:
#       load image
#       get filename
#       thresh hold the image
#       find contours
#       for contour in contours:
#           make image, a box around the contour
#           save this image to a list
#           save the corresponding label from the filename to a list
#   now you have the two lists that will be used for training
#
#
#####################################


from imutils import paths
import cv2
import os
from imutils import build_montages

dataset = "testing"
HXW = 24
data = []
labels = []
img_paths = sorted(list(paths.list_images(dataset)))
img_show = True

# Load each original captcha
for img_path in img_paths:
    mont = []
    filename = img_path.split(os.path.sep)[-1]
    filename_cpy = filename
    filename = os.path.splitext(filename)[0]
    digits = list(filename)
    # Extract each char from the captcha
    img = cv2.imread(img_path)
    #if img_show:
        #cv2.imshow(filename_cpy, img)
        #cv2.waitKey(0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.merge((img, img, img))
    mont.append(img2)


    i = 0
    while i < 4:
        img = cv2.adaptiveThreshold(img, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        img = cv2.threshold(img, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        i += 1


    #if img_show:
        #cv2.imshow("gray scale", img)
        #cv2.waitKey(0)

    #img = cv2.threshold(img, 0, 255,
        #cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    img = cv2.adaptiveThreshold(img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    img2 = cv2.merge((img, img, img))
    mont.append(img2)

    img = cv2.threshold(img, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    img2 = cv2.merge((img, img, img))
    mont.append(img2)




    #img = cv2.threshold(img,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #if img_show:
        #cv2.imshow("threshold", img)
        #cv2.waitKey(0)
    contours = cv2.findContours(img.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    digit_boxs = []
    tmp_data = []
    tmp_labels = []
    boxs = []
    # Make sure the chars are sorted from left to right
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
        box = cv2.merge((box, box, box))
        mont.append(box)
        #if img_show:
            #cv2.imshow(digit, box)
            #cv2.waitKey(0)
    if len(tmp_data) != 4:
        continue
    for (img, label) in zip(tmp_data, tmp_labels):
        if img.shape[0] < 10 or img.shape[1] < 10:
            continue
        data.append(img)
        labels.append(label)
    montage = build_montages(mont, (128, 128), (7, 1))[0]
    cv2.imshow("", montage)
    cv2.waitKey(0)


print(len(data))
print(len(labels))




#
