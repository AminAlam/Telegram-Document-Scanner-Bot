#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 20:28:47 2020

@author: mohammadamin alamalhoda
"""

import numpy as np
import cv2
from PIL import Image, ImageEnhance
from page_detector import page_detect

def guassian(img,degree=3):
    
     blur = img
     blur = 255 - blur
     blur = cv2.GaussianBlur(blur,(degree,degree),0)
     blur = 255 -blur
     return blur
    


# shadow remover
def shadow_remover(img):
    
    rgb_planes = cv2.split(img)


    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        result_norm_planes.append(norm_img)
    
    result_norm = cv2.merge(result_norm_planes)
    return result_norm



def adjust_gamma(img_path,filename= None,gamma=1.0):
    image = cv2.imread(img_path)
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
    invGamma = 1.0/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
    return cv2.LUT(image, table)




def Scanner(img_path,filename):
    
    img = cv2.imread(img_path)
    #img=page_detect(img)
    img=shadow_remover(img)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_TOZERO)
    blur = guassian(thresh,1)

    cv2.imwrite(filename, blur)
    im = Image.open(filename)
    enhancer = ImageEnhance.Contrast(im)
    factor = 2 #increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(filename)
    img = cv2.imread(filename)
    cv2.imwrite(filename,img,[cv2.IMWRITE_JPEG_QUALITY, 40])
    

#final_Scanner("3.jpg","1-ff.jpg")






