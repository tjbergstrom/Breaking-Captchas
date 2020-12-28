

This was pretty fun.

I used some Computer Vision tools and some other tricks to extract the thumbnail images from captchas. I used this to help build the datasets, and then I trained some ML models to make binary predictions - for a given captcha, predict if each thumb is or isn't a crosswalk or whichever.

I also used Optical Character Recognition to extract the text from the captcha - the text that asks which object the captcha wants you to select. So I use that to determine which model to use on a given input captcha.

I kinda just wanted to see how or if this would work and I how would implement it. For now it's just a quick rough draft, and maybe I'll do more with it later. It needs a lot more data to be more accurate.

<br>

![alt text](https://raw.githubusercontent.com/tjbergstrom/breaking-captchas/master/breaking%20image%20captchas/dataset/assets/screenrecord0.gif)



