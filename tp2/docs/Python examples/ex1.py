import numpy as np
import matplotlib.pyplot as plt

im = np.zeros((5, 5)) # image  (5x5 array)
im[2, 3] = 255 # Access pixels with (row,col)=(2,3)

print(im)

plt.imshow(im,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.show()
