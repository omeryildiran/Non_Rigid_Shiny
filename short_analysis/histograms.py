from cgitb import reset
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.misc import ascent
import cv2 as cv
from PIL import Image, ImageChops

res = cv.imread('texture_maps\perlin_matched.png')
# calculate mean value from RGB channels and flatten to 1D array
res = res.mean(axis=2).flatten()
# calculate histogram
counts, bins = np.histogram(res, range(257))
# plot histogram centered on values 0..255
plt.subplot(1, 3, 3)
plt.title("Matched")

plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
plt.xlim([-0.5, 258.5])

source = cv.imread('texture_maps\perlin_v2.png')
#source= cv.imread('texture_maps\perlin.png')
source = source.mean(axis=2).flatten()
# calculate histogram
counts, bins = np.histogram(source, range(257))
# plot histogram centered on values 0..255
plt.subplot(1, 3, 1)
plt.title("Source")

plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
plt.xlim([-0.5, 258.5])

template = cv.imread('HDR files\galileo_probe.png')
template = template.mean(axis=2).flatten()
# calculate histogram
counts, bins = np.histogram(template, range(257))
# plot histogram centered on values 0..255
plt.subplot(1, 3, 2)
plt.title("Reference")

plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
plt.xlim([-0.5, 258.5])
plt.show()
# histr_source = cv.calcHist([source],[0],None,[256],[0,256])
# histr_template = cv.calcHist([template],[0],None,[256],[0,256])

# histr_matched = cv.calcHist([res],[0],None,[256],[0,256])

# fig2=plt.figure()

# gs = plt.GridSpec(1, 3)
# ax1 = fig2.add_subplot(gs[0, 0])
# ax2 = fig2.add_subplot(gs[0, 1], sharex=ax1, sharey=ax1)
# ax3 = fig2.add_subplot(gs[0, 2], sharex=ax1, sharey=ax1)
# ax1.plot(histr_source, label='Texture')
# ax2.plot(histr_template, label='Light')
# ax3.plot(histr_matched, label='Matched')
# plt.plot(histr_source)
# plt.show()
