import noise
import numpy as np
from skimage import exposure
import cv2 as cv

# Parameters for Perlin noise
shape = (64, 64, 64)
scale = 90
persistence = 0.3
octaves = 6
lacunarity = 2.0
seed = np.random.randint(0, 500)

# Generate Perlin noise
perlin_noise = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        for z in range(shape[2]):
            perlin_noise[i][j][z] = noise.pnoise3(i / scale,
                                                 j / scale,
                                                 z / scale,
                                                 octaves=octaves,
                                                 persistence=persistence,
                                                 lacunarity=lacunarity,
                                                 repeatx=shape[0],
                                                 repeaty=shape[1],
                                                 repeatz=2048,
                                                 base=seed)

# Normalize and adjust the Perlin noise
img_32bit = perlin_noise.astype(np.float32)
img_32bit = (perlin_noise - np.min(perlin_noise)) / (np.max(perlin_noise) - np.min(perlin_noise))
img_32bit = img_32bit.astype(np.float32)
img_32bit = exposure.adjust_gamma(img_32bit, 2.2)

# Save the Perlin noise as an HDR image
cv.imwrite("texture_maps/created_noises_etc/" + str(scale) + "_" + str(persistence) + "_" + str(lacunarity) + "perlin.hdr",
           img_32bit)

# Create a symmetrical image by flipping the original image
flipped_32 = cv.flip(img_32bit, 1)
symmetric_im = cv.hconcat([img_32bit, flipped_32])

# Save the symmetrical Perlin noise as an HDR image
cv.imwrite("texture_maps/created_noises_etc/perlin_v4." + str(i) + ".hdr", img_32bit)
cv.imwrite("texture_maps/created_noises_etc/" + str(scale) + "_" + str(persistence) + "_" + str(
    lacunarity) + "perlin_M.hdr", symmetric_im)

# Save the symmetrical Perlin noise as a JPG image
symmetric_im_8 = np.floor((symmetric_im + .5) * 255).astype(np.uint8)
cv.imwrite("texture_maps/created_noises_etc/perlin_v4." + str(i) + ".jpg", symmetric_im_8)

# Save the symmetrical Perlin noise as an image using PIL
img_symmetric = Image.fromarray(np.uint8(symmetric_im * 255), mode='L')
img_symmetric.save("texture_maps/created_noises_etc/perlin_v4." + str(i) + ".jpg")
