#!/usr/bin/python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('image.jpg',cv2.IMREAD_GRAYSCALE)

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.plot([200,300,400],[100,200,300],'g', linewidth=5)
plt.show()
