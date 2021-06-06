#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:18:14 2020

@author: mohammadamin alamalhoda
"""

import cv2
import numpy as np
def Scanner(img_path,filename):

    main = cv2.imread(img_path)
    orig = cv2.medianBlur(main,1)
    kernel = np.array([[-1, -1, -1], 
                       [-1, 9, -1], 
                       [-1, -1, -1]])
    
    sharpen = cv2.filter2D(orig, -1, kernel)
    final = (sharpen/np.amax(sharpen)+orig/np.amax(orig))*255/2
    final = final.astype(np.uint8)
    
    alpha = 1.3 # Simple contrast control
    beta = 1    # Simple brightness control
    final = cv2.convertScaleAbs(final, alpha=alpha, beta=beta)
    gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filename,final,[cv2.IMWRITE_JPEG_QUALITY, 40])
