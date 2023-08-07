"""Basic Usage"""
#   open terminal
#   requirements: python, opencv
#>> ipython
#>> from im_conv import conv
#>> conv(dir_inp="...", dir_out="...", to="FILE FORMAT to be Converted")
#>> conv(dir_inp="texture_maps/matched_noise/",dir_out="HDR files/a_matched_hdrs/",to="hdr")

import os
import cv2 as cv

def conv(dir_inp,dir_out=None,to="hdr"):
    if dir_out==None:
        dir_out=dir_inp   
    if dir_inp[-4]==".":
        a= cv.imread(dir_inp)
        cv.imwrite(dir_out[0:-4]+"."+to, a)    
    else:
        file_list=os.listdir(dir_inp)
        for i in file_list:
            a= cv.imread(dir_inp+i)
            cv.imwrite(dir_out+i[0:-4]+"."+to, a)

conv(dir_inp="texture_maps/pure_noise/",dir_out="HDR files/a_pure_noise_hdrs/", to="hdr")




