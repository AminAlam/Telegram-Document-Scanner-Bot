#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 23:27:54 2020

@author: mohammadamin alamalhoda
"""
# Import necessary libraries
from pyimagesearch import four_point_transform
import cv2
import imutils

def page_detect(image):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    #image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT) 
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    # loop over the contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    	# if our approximated contour has four points, then we
    	# can assume that we have found our screen
    	if len(approx) == 4:
    		screenCnt = approx
    		break
    # show the contour (outline) of the piece of paper
    
    try: 
    
        screenCnt = screenCnt
        #min_x = np.min([screenCnt[0][0][0],screenCnt[1][0][0],screenCnt[2][0][0],screenCnt[3][0][0]])
        #min_y = np.min([screenCnt[0][0][1],screenCnt[1][0][1],screenCnt[2][0][1],screenCnt[3][0][1]])
        #max_x = np.max([screenCnt[0][0][0],screenCnt[1][0][0],screenCnt[2][0][0],screenCnt[3][0][0]])
        #max_y = np.max([screenCnt[0][0][1],screenCnt[1][0][1],screenCnt[2][0][1],screenCnt[3][0][1]])
        #screenCnt[0][0][0] = min_x
        #screenCnt[0][0][1] = min_y
        #screenCnt[1][0][0] = min_x
        #screenCnt[1][0][1] = max_y
        #screenCnt[2][0][0] = max_x
        #screenCnt[2][0][1] = min_y
        #screenCnt[3][0][0] = max_x
        #screenCnt[3][0][1] = max_y
        
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
        return warped
        
    except:
        return orig
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    