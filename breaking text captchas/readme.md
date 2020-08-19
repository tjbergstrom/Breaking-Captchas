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

Here are some preliminary results after training with only 1,000 images and 10 training epochs:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord3.gif)


<br>
<br>


So it's definitely do-able! Fom here I could start over and build a proper model with the 10,000 images that I have, or try
something more challenging - this model can only break these specific captchas, and I might be more interested in collecting
other more challenging types.


<br>
<br>


It also appears that, moving forward, you need to process the images better to extract the text:

(the four squares on the right are not just a close up, they are the extracted images created by finding contours, and the model trains with them)

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord2.gif)

This improves accuracy just a little:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/screenrecord4.gif)

After training with about 8,000 captchas and testing with almost 2,000 I can get one out of four correct:

![alt text](https://raw.githubusercontent.com/tjbergstrom/Breaking-Captchas/master/breaking%20text%20captchas/assets/ss7.png)

5. Get more labeled captchas and different types and train other models.

6. Start over with trying out better or different data collection.

7. Tune a really good model and try to increase it's accuracy (with better data and hyper-tuning).

