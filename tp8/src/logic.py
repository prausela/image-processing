import numpy as np
from skimage.transform import radon, iradon
from skimage.draw import ellipse

def new_phantom() -> np.ndarray:
   phantom = np.zeros((250, 250))
   return phantom

def new_ellipse(
    phantom: np.ndarray,
    I: int,
    A: int,
    X: int,
    Y: int,
    CX: int,
    CY: int
) -> tuple[np.ndarray, np.ndarray, int]:
    
    rad_A = A*np.pi/180
    
    scaled_X = (X * phantom.shape[1])/2
    scaled_Y = (Y * phantom.shape[0])/2

    scaled_CX = (CX * phantom.shape[1]/2) + phantom.shape[1]/2
    scaled_CY = phantom.shape[0] - ((CY * phantom.shape[0]/2) + phantom.shape[0]/2)
    
    rr, cc = ellipse(r=scaled_CY, c=scaled_CX, r_radius=scaled_Y, c_radius=scaled_X, rotation=rad_A, shape=phantom.shape)
    
    return rr, cc, I

def add_ellipse(phantom: np.ndarray, ellipse: tuple[np.ndarray, np.ndarray, int]) -> np.ndarray:
    rr, cc, I = ellipse
    phantom[rr, cc] = I
    return phantom

def calculate_radon_transform(phantom: np.ndarray, start: int, step: int, end: int) -> tuple[np.ndarray, np.ndarray]:
    theta = np.array(list(range(start, end, step)))
    radon_transform = radon(phantom, theta)
    return radon_transform, theta

def calculate_inverse_radon_transform(radon_transform: np.ndarray, theta: np.ndarray, interpolation_name: str, filter_name: str) -> np.ndarray:
    side = radon_transform.shape[0]
    iphantom = iradon(radon_transform, 
                    theta, 
                    side, 
                    interpolation=interpolation_name,
                    filter_name=filter_name)
    return iphantom