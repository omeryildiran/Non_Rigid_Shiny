from PIL import Image, ImageChops
import cv2 as cv
import os
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as compare_ssim
import numpy as np

A = "Objects/"
all_scores = []
all_difs = []
b = os.listdir(A)

# Loop through the folders in 'Objects/'
for x in range(15, 20):
    C = os.listdir(A + b[x])

    # Loop through the images in the folder
    for i in range(len(C) - 2):
        im1 = cv.imread(A + b[x] + "/" + str(C[i]), cv.IMREAD_GRAYSCALE)
        im2 = cv.imread(A + b[x] + "/" + str(C[i + 1]), cv.IMREAD_GRAYSCALE)

        # Compute the Structural Similarity Index (SSIM) between the two images
        (score, diff) = compare_ssim(im1, im2, full=True)
        diff = (diff * 255).astype("uint8")
        all_difs.append(diff)
        all_scores.append(round(score, 3))

# Scores are Structural Similarity Index (SSIM)
print("SSIM is ", str(all_scores) + "\n")
print("Mean structural similarities is ", round(sum(all_scores) / len(all_scores), 3))

# Calculate the average difference image
res = sum(all_difs)
res = np.true_divide(res, len(all_difs))

# Show the difference image
cv.imshow("Diff", res)
cv.waitKey(0)

# df = pd.DataFrame(all_difs , columns =['r', 'g' , 'b','alpha'])
# plt.plot(df['b'],label="b")
# #plt.plot(df['alpha'],label="alpha")
# plt.plot(df['g'],label="g")
# plt.plot(df['r'],label="r")
# plt.legend()
# #plt.show()

# Read two images and convert to grayscale
# img1 = cv.imread('C:/Users/omeru/Documents/FND/My Repos/Blender/Objects/obj_0/non_rigid_matte_0_0001.png', cv.IMREAD_GRAYSCALE)
# img2 = cv.imread('C:/Users/omeru/Documents/FND/My Repos/Blender/Objects/obj_0/non_rigid_matte_0_0002.png', cv.IMREAD_GRAYSCALE)
