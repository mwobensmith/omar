# omar

Project Omar

**Quick prototype:**
A program that can catalog images and search them using an image as input.

**Step 1:** 
Given a folder of images, produce a JSON file with an entry for each image that contains data about it.
* Path to image
* Hash of image [1]
* All text found in image
* Best guess at title [2]

**Step 2:** 
Given an image, determine if it matches a hash from the JSON file in Step 1.

<hr>
[1] Image hashing in Python is possible with OpenCV, and there are many tutorials online. The image is reduced to an 8x8 greyscale image and then a fingerprint or hash is saved that can be used later for comparison.
https://www.pyimagesearch.com/2017/11/27/image-hashing-opencv-python/

[2] Using Tesseract, etc. can we determine what text is the largest in a given image?
