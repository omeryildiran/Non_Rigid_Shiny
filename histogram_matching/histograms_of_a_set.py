import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt

# Set the directory for light images
light_list_dir = 'texture_maps/real_textures_v2_04112022/'
light_list = os.listdir(light_list_dir)
n_light = len(light_list)

# Loop through the light images
for i in range(len(light_list)):
    plt.subplot(3, n_light // 3 + (n_light % 3 != 0), i + 1)

    # Read the light image and convert it to grayscale
    light = cv.imread(light_list_dir + light_list[i])
    light = cv.cvtColor(light, cv.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv.imwrite("HDR files/real_textures_v2_04112022/" + str(light_list[i][0:-4]) + ".hdr", light)

    # Plot the histogram
    plt.hist(np.reshape(light, [-1]), bins=60)
    plt.title(light_list[i][0:-4])

plt.show()
