





import importlib 
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature, io, segmentation, color
from skimage.color import rgb2gray, gray2rgb, convert_colorspace
from skimage.transform import probabilistic_hough_line, resize
from time import time

original_img = io.imread("dog.jpg")
img = ndi.gaussian_filter(rgb2gray(original_img), 2.5)
img = feature.canny(img, sigma=3)
img1 = (255 - img) * 2

# io.imshow(img)

original_img = io.imread("dog.jpg")
img = ndi.gaussian_filter(rgb2gray(original_img), 3)
img = feature.canny(img, sigma=4)
img = 255 - img


io.imshow(img1 + img, cmap='gray')


plt.show()