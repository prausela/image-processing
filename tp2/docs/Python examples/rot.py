#!/usr/bin/python3

from PIL import Image
import sys

try:
    mi_imagen = Image.open("image.jpg")

except IOError:
    print("Unable to load image")
    sys.exit(1)
    
rotated = mi_imagen.rotate(180)
rotated.save('image_rotated.jpg') 

