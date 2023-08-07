from cv2 import IMREAD_ANYDEPTH
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.misc import ascent
import cv2 as cv
from PIL import Image, ImageChops
from skimage import exposure
import matplotlib.image as mpimg


text=cv.imread('HDR files/a_pure_noise_hdrs/4_10_perlinLL.hdr',cv.IMREAD_ANYDEPTH)
light=cv.imread('HDR files/new_hdrs/abandoned_workshop_02_2k.hdr',cv.IMREAD_ANYDEPTH)
#print(np.max(light))
matched=cv.imread('HDR files/new_matched_noise_hdrs/4_10_perlinLL_HM_abandoned_workshop_02_2k_gray.hdr',cv.IMREAD_ANYDEPTH)
#plt.hist(np.reshape(im, [-1]),bins=500)
#plt.xlim([0,1])
#plt.show()

plt.subplot(1,3,1)
plt.hist(np.reshape(text, [-1]),bins=100)
plt.title("Uffizi")
plt.subplot(1,3,2)
plt.hist(np.reshape(light, [-1]),bins=100)
plt.title("RNL")
plt.subplot(1,3,3)
plt.title("Matched")
plt.hist(np.reshape(matched, [-1]),bins=100)

#fig, axs = plt.subplots(1,3)
#axs[0]=plt.hist(np.reshape(text, [-1]))
#axs[1]=plt.hist(np.reshape(light, [-1]))
#axs[2]=plt.hist(np.reshape(matched, [-1]))
#axs[2].set_xlim()
plt.show()



