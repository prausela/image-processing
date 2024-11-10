import numpy as np
from skimage.transform import radon, iradon
from skimage.draw import ellipse
import matplotlib.pyplot as plt

def new_phantom() -> np.ndarray:
   phantom = np.zeros((250, 250))
   return phantom

def add_elipse(
    phantom: np.ndarray,
    I: int,
    A: int,
    X: int,
    Y: int,
    CX: int,
    CY: int
) -> np.ndarray:
    
    rad_A = A*np.pi/180
    
    scaled_X = (X * phantom.shape[1])/2
    scaled_Y = (Y * phantom.shape[0])/2

    scaled_CX = (CX * phantom.shape[1]/2) + phantom.shape[1]/2
    scaled_CY = phantom.shape[0] - ((CY * phantom.shape[0]/2) + phantom.shape[0]/2)
    
    rr, cc = ellipse(r=scaled_CY, c=scaled_CX, r_radius=scaled_Y, c_radius=scaled_X, rotation=rad_A, shape=phantom.shape)
    phantom[rr, cc] = I
    return phantom

def make_sinogram(phantom: np.ndarray, start: int, step: int, end: int) -> tuple[np.ndarray, np.ndarray]:
    theta = list(range(start, end+1, step))
    sinogram = radon(phantom, theta)
    return sinogram, theta