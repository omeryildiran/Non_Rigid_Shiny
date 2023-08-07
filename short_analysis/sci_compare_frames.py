# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2 as cv2

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
# 	help="first input image")
# ap.add_argument("-s", "--second", required=True,
# 	help="second")
# args = vars(ap.parse_args())

img1 = cv2.imread('C:/Users/omeru/Documents/FND/My Repos/Blender/Objects/obj_0/non_rigid_matte_0_0001.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('C:/Users/omeru/Documents/FND/My Repos/Blender/Objects/obj_0/non_rigid_matte_0_0002.png', cv2.IMREAD_GRAYSCALE)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(img1, img2, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(round(score,3)))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

