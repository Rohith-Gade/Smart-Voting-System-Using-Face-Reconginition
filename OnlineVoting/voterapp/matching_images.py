import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pickle as pk
import os
# Create a directory to save the captured images
if not os.path.exists("captured_images"):
    os.makedirs("captured_images")
# Capture multiple frames from the default camera and save them to the directory
cap = cv.VideoCapture(0)
if  not cap.isOpened():
    raise IOError("cannot open webcam")
for i in range(1):
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
    c = cv.waitKey(1)
    stop=input()
    if c==stop:
        break
    cv.imshow('Input', frame)
    filename = "captured_images/image{}.jpg".format(i)
    cv.imwrite(filename, frame)
# Release the camera and close the window
cap.release()
cv.destroyAllWindows()
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
img = cv.imread('C:\Users\pc\Desktop\images', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img2 = img.copy()
template = cv.imread('keer1.jpg', cv.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()