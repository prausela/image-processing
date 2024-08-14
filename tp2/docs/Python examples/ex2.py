import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

img = cv2.imread('lena.jpg',cv2.IMREAD_GRAYSCALE)



plt.figure(1)

plt.imshow(img,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.show(block=False) # Show the plot in non-blocking mode (i.e continue)

plt.figure(2)

Lena_eye=img[251:283,317:349]
plt.subplot(121)
plt.imshow(img,cmap='gray',interpolation='none')
plt.title('Lena'),plt.axis('off') 

plt.subplot(122)
plt.imshow(Lena_eye,cmap='gray',interpolation='none')
plt.title("Right Lena's eye"),plt.axis('off') 

plt.show()



