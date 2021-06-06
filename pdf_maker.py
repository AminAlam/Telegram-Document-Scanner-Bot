#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:39:19 2020

@author: mohammadamin alamalhoda
"""
#from fpdf import FPDF
#import os

#pdf = FPDF()   

#def pdf_maker(imagelist,file_name):
 #   print(imagelist)
  #  for image in imagelist:
   #     pdf.add_page()
    #    pdf.image(image,5,5,210,297)
  #  pdf.output(file_name, "F")
 #  for i in imagelist:
      #  os.remove(i)
    
import os
import img2pdf
from text_puter import text_put
import cv2
def pdf_maker(imagelist,file_name,first_page,path_to_file):
    if first_page:
        imagelist.insert(0,path_to_file+'first_page.jpg')
    with open(file_name, "wb") as f:
        f.write(img2pdf.convert([i for i in imagelist]))
    for i in imagelist:
        os.remove(i)


