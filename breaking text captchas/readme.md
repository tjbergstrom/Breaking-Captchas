This has been done before (there's a reason you don't see these much anymore), just want to see how I would implement it. 

1. Data collection. Need lots of labeled captchas. There are/were about 30 different types of text based captchas used by different
websites. Maybe start with just one type.

2. How to extract characters from a captcha.

input with label in filename

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss1.png)

threshold

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss2.png)

find contours, get label from filename

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss3.png)
![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss4.png)
![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss5.png)
![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss6.png)

3. Use the extracted characters to train a model.

4. Try it out trying to break / crack / decode input captchas.

Here are some early results:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord3.gif)


<br>
<br>
<br>


It's definitely do-able. Fom here I could start over and build a more robust model with more training images, or try
something more challenging - this model can only break these specific captchas, and I might be more interested in collecting
other more challenging types.


<br>
<br>
<br>


It also appears that you need to process the images better to extract the text:

(the four squares on the right are the extracted images created by finding contours, and the model trains with them)

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord2.gif)


<br>
<br>
<br>
<br>


Extra thresholding improves accuracy just a little:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord4.gif)


<br>
<br>


After training with about 8,000 captchas and testing with almost 2,000 it can break about one out of four captchas.
The model is at 85% accuracy per each character, which would be about 52% per four characters in a row, if the characters that it gets 
wrong were evenly distributed.

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss7.png)

<br>

And with better processing, including passing two thresholding filters 5 times, accuracy is up to breaking 2 out of 5 captchas:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss8.png)

<br>

5. Get more labeled captchas and different types and train other models.

6. Start over with trying out better or different data collection.

7. Tune a really good model and try to increase it's accuracy (with better data and hyper-tuning).

<br>
<br>

(10.) Make a demo?

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord5.gif)
