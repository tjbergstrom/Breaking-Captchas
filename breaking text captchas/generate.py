# generate.py
# ImageCaptcha can generate a certain type of captcha
# This code will make a directory of new captcha images to train with


from captcha.image import ImageCaptcha
import random
import argparse
import cv2
import numpy as np
import os


ap = argparse.ArgumentParser()
ap.add_argument("-n", "--numcaptchas", type=int, default=10)
ap.add_argument("-i", "--imshow", type=bool, default=False)
ap.add_argument("-m", "--makenewdir", type=bool, default=False)
args = vars(ap.parse_args())
num_captchas = args["numcaptchas"]
save_dir = "generated_captchas/"
print_info = False
len_captcha = 4


# A list of all possible chars that will make the captchas
charz = [
    "0","1","2","3","4","5","6","7","8","9",
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
# Without these chars
remove_charz = ["0","1","I","O"]
for ch in remove_charz:
    charz.remove(ch)


def generate_text():
    text = ""
    for i in range(len_captcha):
        text += random.choice(charz)
    if print_info:
        print("New captcha:", text)
    return text


def generate_img(text):
    captcha = ImageCaptcha()
    img = captcha.generate_image(text)
    try:
        # Add curve noise
        captcha.create_noise_curve(img, img.getcolors())
        # Add dots noise
        captcha.create_noise_dots(img, img.getcolors())
        img_path = save_dir + text + ".png"
        captcha.write(text, img_path)
        if args["imshow"]:
            cv2.imshow(text, np.array(img))
            cv2.waitKey(60)
        if print_info:
            print("New image:", img_path)
    except:
        pass


# Remove any previously generated captchas in the directory
# And start fresh with the desired number of captchas from this run
def make_new_dir():
    cmd = "rm -rf " + save_dir
    os.system(cmd)
    cmd = "mkdir " + save_dir
    os.system(cmd)


def main():
    if args["makenewdir"]:
        make_new_dir()
    generated_captchas = []
    for i in range(num_captchas):
        text = generate_text()
        if text not in generated_captchas:
            generate_img(text)
            generated_captchas.append(text)
    print("Saved:", len(generated_captchas), "new images")


main()



#
