import numpy as np
import os
import cv2 as cv
from skimage import exposure

# Set the directory for noise images
dir_noises = "HDR files/a_pure_noise_hdrs/"
noise_list = os.listdir(dir_noises)

# Set the directory for HDR images
dir_hdrs = "HDR files/light_fields_gray_v2_04112022/"
hdr_list = os.listdir(dir_hdrs)
s_width, s_height = [2048, 1024]

# Loop through noise images and HDR images
for noise in noise_list:
    for hdr in hdr_list:
        # Get the noise image
        noise_address = dir_noises + noise
        noise_name = noise_address.split('/')[-1].split('.')[0]
        source = cv.imread(noise_address, cv.IMREAD_ANYDEPTH)
        source = cv.resize(source, (s_width, s_height))

        # Get the HDR image
        hdr_address = dir_hdrs + hdr
        probe_name = hdr_address.split('/')[-1].split('.')[0]
        template = cv.imread(hdr_address, cv.IMREAD_ANYDEPTH)
        template = cv.resize(template, (s_width, s_height))

        # Match histograms
        multi = True if source.shape[-1] > 1 else False
        matched = exposure.match_histograms(source, template, multichannel=multi)

        # Convert to grayscale
        gray_32bit = cv.cvtColor(matched, cv.COLOR_BGR2GRAY)

        # Save the matched image
        cv.imwrite("HDR files/matched_noise_b_v2_04112022/" + probe_name + 'HM' + noise_name + ".hdr", gray_32bit)

# This part is just for plotting the histograms (you can uncomment it if needed)
def ecdf(x):
    """Convenience function for computing the empirical CDF"""
    vals, counts = np.unique(x, return_counts=True)
    ecdf = np.cumsum(counts).astype(np.float64)
    ecdf /= ecdf[-1]
    return vals, ecdf


def plot_matches(noise_im, hdr_im, matched):
    x1, y1 = ecdf(noise_im.ravel())
    x2, y2 = ecdf(hdr_im.ravel())
    x3, y3 = ecdf(matched.ravel())

    fig = plt.figure()
    gs = plt.GridSpec(2, 3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], sharex=ax1, sharey=ax1)
    ax3 = fig.add_subplot(gs[0, 2], sharex=ax1, sharey=ax1)
    ax4 = fig.add_subplot(gs[1, :])
    for aa in (ax1, ax2, ax3):
        aa.set_axis_off()

    ax1.imshow(noise_im, cmap=plt.cm.gray)
    ax1.set_title('Texture')
    ax2.imshow(hdr_im, cmap=plt.cm.gray)
    ax2.set_title('Light Probe')
    ax3.imshow(matched, cmap=plt.cm.gray)
    ax3.set_title('Matched')

    ax4.plot(x1, y1 * 100, '-r', lw=3, label='Texture')
    ax4.plot(x2, y2 * 100, '-k', lw=3, label='Light Probe')
    ax4.plot(x3, y3 * 100, '--r', lw=3, label='Matched')
    #ax4.set_xlim(x1[0], x1[-1])
    ax4.set_xlabel('Pixel value')
    ax4.set_ylabel('Cumulative %')
    ax4.legend(loc=5)

    plt.show()

# Call the plot_matches function with appropriate images (uncomment this if needed)
# plot_matches(source, template, matched)
