#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:18:14 2020

@author: mohammadamin alamalhoda
"""

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile 
import numpy as np
import os 
import random

def email_send(filename,receiver_email,JPG = 0,counts = None,PDF_name = None,First_page = 0):
    
    mail_base = [ "MedALScanner@gmail.com",  "medalscanner1@gmail.com" ,  "medalscanner2@gmail.com"  ,  "medalscanner3@gmail.com"  ,   "medalscanner4@gmail.com" ,    "medalscanner5@gmail.com" ,   "medalscanner6@gmail.com" ,    "medalscanner7@gmail.com" ,   "medalscanner8@gmail.com"   ,   "medalscanner9@gmail.com"]
    subject = "Your File By MedAL Scanner"
    body = " "
    sender_email = random.choice(mail_base)
    print(sender_email)
    password = "ICANSEEYOU1232821Ai82b1al1!adu3ja#qenuxpoi9923ndiwaksdhfie"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
  # In same directory as script
    # Open PDF file in binary mode
    if JPG==0:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        filename = 'PDF_MedAL.pdf'
        
    else:
        zipObj = zipfile.ZipFile(filename+"photos_MedAL.zip", 'w' ,zipfile.ZIP_DEFLATED)
        um_list = np.linspace(1,counts-1,counts-1,dtype=int)
        if First_page: 
            img_name = filename+'first_page.jpg'
            arcname = 'first_page.jpg'
            zipObj.write(img_name,arcname)
            os.remove(img_name)
            
        # Add multiple files to the zip
        for i in um_list:
            img_name = filename+'scanned_'+str(i)+'.jpg'
            arcname = 'scanned_'+str(i)+'.jpg'
            zipObj.write(img_name,arcname)
            os.remove(img_name)
            # close the Zip File
        zipObj.close()
        with open(filename+"photos_MedAL.zip", "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        filename = filename+"photos_MedAL.zip"
        os.remove(filename)
        filename = "photos_MedAL.zip"
            

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

#email_send("1079952092","ma.alamalhoda@gmail.com")