#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:18:14 2020

@author: mohammadamin alamalhoda
"""
import arabic_reshaper

# install: pip install python-bidi
from bidi.algorithm import get_display

# install: pip install Pillow
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import cv2
import os



def text_put(path_to_file,text,poem):
    W, H = (1200,1400)
    if poem:
        image = Image.open(os.getcwd()+'/'+"EyGhom.jpg") 
    else:
        image = Image.new("RGBA",(W,H),"white")
        
    num = len(text)
    # use a good font!
    fontFile = "arial.ttf"
        
    # load the font and image
    font = ImageFont.truetype(fontFile, 50)

    
    
    for i in np.linspace(0,num-1,num,dtype=int):
        
        text_n = text[i]
        reshaped_text = arabic_reshaper.reshape(text_n)    # correct its shape
        bidi_text = get_display(reshaped_text)           # correct its direction
        draw = ImageDraw.Draw(image)
        
        
        draw.text((70,150*(1+i)), bidi_text, (10,10,10), font=font)
        draw = ImageDraw.Draw(image)
        
    # save it
    image.save(path_to_file+'first_page'+'.png')
    image = cv2.imread(path_to_file+'first_page'+'.png')
    if poem != 1:
        image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT,value=[0,0,0]) 
        image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT,value=[255,255,255]) 
    os.remove(path_to_file+'first_page'+'.png')
    cv2.imwrite(path_to_file+'first_page.jpg', image)



