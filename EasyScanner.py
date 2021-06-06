#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 23:27:54 2020

@author: mohammadamin alamalhoda
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters ,CallbackQueryHandler
from telegram import Bot, ChatAction ,ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from perspective import Scanner
import numpy as np
import os
from  pdf_maker import pdf_maker
from text_puter import text_put
import datetime
from send_email import email_send
from os.path import join as pjoin
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Users:
    user_count = 1
    
    def __init__(self, chat_number, count, history, text, mail = 0 ,delete_message_id = None,PDF = 0, PDF_name = None, user_name = None):
      self.chat_number = chat_number
      self.count = count
      self.history = history
      self.text = text
      self.mail = mail
      self.delete_message_id = delete_message_id
      self.PDF = PDF
      self.PDF_name = PDF_name
      self.user_name = user_name
      Users.user_count = Users.user_count + 1 
   

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    try:    
        user_name = update.effective_user.username
    except :
        user_name = update.message.from_user.username
    chat_id=update.effective_chat.id
    name = 'user_'+str(chat_id)
   
    try:
        if(isinstance(globals()[name], Users)):
                globals()[name].count = 0
                globals()[name].text = 0
    except:
        globals()[name] = Users(chat_id,0,0,0)
            
    globals()[name].user_name = user_name
    date_time = str(datetime.datetime.now()) 
    if update.message.from_user.first_name != None :
        first_name = update.message.from_user.first_name
    else:
        first_name = "Dear"
    context.bot.send_chat_action(chat_id = update.message.chat_id , action = ChatAction.TYPING)
    welcome_message = "Hi " + first_name + " :)" + "\n" + "click on /help for guide."
    if not os.path.exists(os.getcwd()+'/'+str(chat_id)):
        os.mkdir(os.getcwd()+'/'+str(chat_id))
    try:
        update.message.reply_text(welcome_message)
    except:
        welcome_message = "Hi Dear :)" + "\n" + "click on /help for guide."
        update.message.reply_text(welcome_message)
        
    try:
        print(user_name+" started bot at "+date_time)
        context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text = user_name+" started bot at "+date_time)
    except:
        print(str(chat_id)+" started bot at "+date_time)
        context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text =str(chat_id)+" started bot at "+date_time)
    
        
def help_command(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
    """Send a message when the command /help is issued."""
    # help_message = "اگر میخوای فقط یک‌سری عکس رو اسکن و تبدیل به PDF کنی، روی /image ضربه بزن." + "\n" +"ولی اگر میخوای صفحه اول PDF رو نوشته دلخواهت تشکیل بده، روی /text ضربه بزن."+ "\n" +"روی /example ضربه بزن تا یک نمونه از نحوه عملکرد /text رو ببینی :)"+"\n"+"راستی، اگر نگرانی یا شکی در مورد استفاده از بات داری، روی /privacy ضربه بزن."
    help_message = "Click on /image if you just want scan some photos and make them a PDF"+"\n"+"Click on /text if you want to add some scan photos and also add some text to the first page of PDF"+"\n"+"Click on /example to see an example of /text"
    update.message.reply_text(help_message)
    
def example(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
    chat_id=update.effective_chat.id
    # message = "مثلا اگر همیچین پیامی به من بدی:"
    message = "if you send me a message similar to "
    update.message.reply_text(message)
    message = "محمدامین علم‌الهدی"+"\n"+"۹۷۱۰۲۰۹۹"+"\n"+"تمرین سری بیست و سوم اصول الکترونیک"+"\n"+"استاد کاوه وش"
    update.message.reply_text(message)
    # message = "من همچین تصویری به صفحه اول PDF اضافه می‌کنم:"
    message = "i will add this page to first of your pdf"
    update.message.reply_text(message)
    context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.UPLOAD_PHOTO)
    context.bot.sendPhoto(chat_id=chat_id, photo=open('example.jpg', 'rb'))
    
    
def privacy(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
    chat_id=update.effective_chat.id
    message = "احتمالا تعدادی نگران هستند که MedAL از اطلاعاتشون(مثلا نام کاربری یا فایل‌های ارسالی) سواستفاده کنه." + "\n" + "در وهله اول کاملا بهتون حق میدم که این نگرانیو‌ داشته باشید!" + "\n" + "در وهله دوم بهتون اطمینان میدم که اطلاعات شما مثل فایل‌ها یا نام کاربریتون در هیچ جایی ذخیره یا برای کسی غیر از خودتون فرستاده نمیشه." +"\n" + "در مورد اینکه هزینه های bot چطور تامین میشه، باید بگم که از تبلیغات کانال موزیکمون :)"+"\n"+"امیدوارم همیشه موفق، سالم و شاد باشید."+"\n"+"دوست دار شما، Alam"
    update.message.reply_text(message)


def image(update, context):

    """send pdf to resoponse of the user message."""
    chat_id=update.message.chat_id
    name = 'user_'+str(chat_id)
    
    file_id = update.message.photo[-1]
    newFile = context.bot.get_file(file_id)
    
    filename = str(globals()[name].count)+'.jpg'
    path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
    
    newFile.download(path_to_file)
    # context.bot.send_photo(chat_id=update.effective_chat.id,photo=open('scanned_test.jpg','rb'))
    globals()[name].count = globals()[name].count + 1
    
    
    
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu    

def file_type(update,context):
    
    chat_id=update.effective_chat.id
    name = 'user_'+str(chat_id)
    context.bot.send_chat_action(chat_id=chat_id, action = ChatAction.TYPING)
    if globals()[name].count >1 :
        # txt = "خب PDFشون رو بفرستم یا فایل عکس هر کدوم رو؟"
        txt = "you want PDF or all seperate images?"
        button_list = [
        InlineKeyboardButton("PDF", callback_data="PDF"),
        InlineKeyboardButton("images", callback_data="JPG"),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        message_bot = context.bot.send_message(text = txt,chat_id=chat_id, reply_markup=reply_markup)
        globals()[name].delete_message_id = message_bot.message_id
    else:
         # txt = "هنوز عکسی نفرستادی که :/"
         txt = "you didn't send any image"
         context.bot.sendMessage(chat_id=chat_id, text=txt)


def callback_query_handler(update,context):
    query = update.callback_query.data
    chat_id=update.effective_chat.id
    user_name = update.callback_query.from_user.username
    name = 'user_'+str(chat_id)
    file_name = str(chat_id)+str(globals()[name].history)
    context.bot.deleteMessage(chat_id=chat_id,message_id=  globals()[name].delete_message_id)
    globals()[name].delete_message_id = None
    
    if query == "yes_mail":
        # email_meesage = "بیزحمت ایمیلت رو برام بفرست"+"\n"+"فقط حواست باشه ایمیل رو اشتباه واردی نکنی!"
        email_meesage = "please send me your email (be careful!)"
        context.bot.send_message(chat_id=chat_id, text=email_meesage)
        globals()[name].mail = 1
        date_time = str(datetime.datetime.now())
        try:
            print(user_name+" Email request at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" Email request at "+date_time)
        except:
            print(str(chat_id)+" Email request at "+date_time)   
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" Email request at "+date_time)
    
    if query == "no_mail": 
        filename = globals()[name].PDF_name+'.pdf'
        path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
        os.remove(path_to_file)
        globals()[name].history = globals()[name].history + 1
        date_time = str(datetime.datetime.now())
        try :
            print(user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        except:
            print(str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        globals()[name].PDF = 0
        globals()[name].text = 0

        
        

            
    if query == "PDF":
        globals()[name].PDF = 1
        text = 'لطفا اسم فایل PDF رو برام بفرست'
        context.bot.sendMessage(chat_id=chat_id, text = text)
        
    
    if query == "JPG":
        globals()[name].PDF = 0
        send(update,context)
        
    if query == "no_JPG":
        counts = globals()[name].count
        um_list = np.linspace(1,counts-1,counts-1,dtype=int)
        if globals()[name].text:
            filename_main = "first_page.jpg"
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename_main)
            os.remove(path_to_file)
            globals()[name].text = 0
        for i in um_list:
            filename = 'scanned_'+str(i)+'.jpg'
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
            os.remove(path_to_file)
        globals()[name].history = globals()[name].history + 1
        date_time = str(datetime.datetime.now())
        try :
            print(user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        except:
            print(str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        globals()[name].PDF = 0
        globals()[name].text = 0
            
    if query == "yes_JPG":
        globals()[name].PDF = 0
        globals()[name].mail = 1
        # email_meesage =  "بیزحمت ایمیلت رو برام بفرست"+"\n"+"فقط حواست باشه ایمیل رو اشتباه واردی نکنی!"
        email_meesage = "please send me your email (be careful!)"
        context.bot.send_message(chat_id=chat_id, text=email_meesage)
        globals()[name].mail = 1
        date_time = str(datetime.datetime.now())
        try:
            print(user_name+" Email request at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" Email request at "+date_time)
        except:
            print(str(chat_id)+" Email request at "+date_time)   
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" Email request at "+date_time)
        
        
    
def send(update,context):
    chat_id=update.effective_chat.id
    name = 'user_'+str(chat_id)
    user_name = globals()[name].user_name
    if globals()[name].PDF:
        chat_id=update.effective_chat.id
        context.bot.send_chat_action(chat_id=chat_id, action = ChatAction.UPLOAD_DOCUMENT)
        imagelist =[]
        counts = globals()[name].count
        um_list = np.linspace(1,counts-1,counts-1,dtype=int)
        
        for i in um_list:
            filename = 'scanned_'+str(i)+'.jpg'
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
            filename_main = str(i)+'.jpg'
            path_to_file_main = pjoin(os.getcwd()+"/", str(chat_id), filename_main)
            Scanner(path_to_file_main,path_to_file)
            imagelist.append(path_to_file)
            
            os.remove(path_to_file_main)
            
        first_page = globals()[name].text
        globals()[name].text = 0
        filename = globals()[name].PDF_name+'.pdf'
        path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
        pdf_maker(imagelist,path_to_file,first_page,pjoin(os.getcwd()+"/", str(chat_id), ""))   
        context.bot.send_document(chat_id=chat_id, document=open(path_to_file, 'rb'))
        context.bot.send_chat_action(chat_id=chat_id, action = ChatAction.TYPING)
        # txt = "دوست داری PDF بالا رو برات ایمیل کنم؟"
        txt = "do yoy want me to send this PDF to your email?"
        button_list = [
        InlineKeyboardButton("Yes", callback_data="yes_mail"),
        InlineKeyboardButton("No", callback_data="no_mail"),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        message_bot = context.bot.send_message(text = txt,chat_id=chat_id, reply_markup=reply_markup)
        globals()[name].delete_message_id = message_bot.message_id
        globals()[name].PDF = 1
        
    else:
        user_name = update.callback_query.from_user.username
        context.bot.send_chat_action(chat_id=chat_id , action = ChatAction.UPLOAD_DOCUMENT)
        counts = globals()[name].count
        um_list = np.linspace(1,counts-1,counts-1,dtype=int)
        if globals()[name].text:
            filename_main = "first_page.jpg"
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename_main)
            context.bot.sendPhoto(chat_id=chat_id, photo=open(path_to_file, 'rb'))
            #os.remove(path_to_file)
            
        for i in um_list:
            filename = 'scanned_'+str(i)+'.jpg'
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
            filename_main = str(i)+'.jpg'
            path_to_file_main = pjoin(os.getcwd()+"/", str(chat_id), filename_main)
            Scanner(path_to_file_main,path_to_file)
            context.bot.sendPhoto(chat_id=chat_id, photo=open(path_to_file, 'rb'))
            os.remove(path_to_file_main)
            
            
        # txt = "دوست داری عکس‌های بالارو برات ایمیل کنم؟"
        txt = "Do you want me to send this images to your email"
        button_list = [
        InlineKeyboardButton("Yes", callback_data="yes_JPG"),
        InlineKeyboardButton("No", callback_data="no_JPG"),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        message_bot = context.bot.send_message(text = txt,chat_id=chat_id, reply_markup=reply_markup)
        globals()[name].delete_message_id = message_bot.message_id

        
    
    
def begin(update,context):
    chat_id=update.effective_chat.id
    user_id = update.message.from_user.id
    name = 'user_'+str(chat_id)

    
    channel_id = '@MedALMusic'
    state = context.bot.get_chat_member(channel_id, user_id)
    if not os.path.exists(os.getcwd()+'/'+str(chat_id)):
        os.mkdir(os.getcwd()+'/'+str(chat_id))
    if state.status != "left" :
        chat_id = update.effective_chat.id
        date_time = str(datetime.datetime.now())
        
        try:
            if(isinstance(globals()[name], Users)):
                globals()[name].count = 1
                globals()[name].text = 0
                user_name = update.effective_user.username
        except:
            globals()[name] = Users(name,1,1,text = 0)
            try:    
                user_name = update.effective_user.username
            except :
        
               try:
                   user_name = update.message.from_user.username
               except:
                   user_name=globals()[name].user_name
        
        try:
            print(user_name+" image request at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" image request at "+date_time)
        except:
            print(str(chat_id)+" image request at "+date_time)   
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" image request at "+date_time)
        
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        # gidence_message = "عکس‌هایی که می‌خوای اسکن کنم رو به ترتیب برام بفرست و بعدش که آپلود شدن، /end رو بزن." + "\n" + "پیشنهاد می‌کنم عکس‌هات رو کراپ کنی بعد بفرستی."
        gidence_message = "Send me the images and wait till they be uploaded then click on /end"+ "\n" +"I highly recommend crop them first"
        update.message.reply_text(gidence_message)
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        #sorry_message = "همممم، فکر کنم هنوز عضو کانال @MedALMusic نشدی، برای حمایت از ما لطفا عضو کانال شو، بعدش میتونی با فرستادن دوباره دستور از خدماتمون استفاده کنی :)"
        sorry_message = "You must first join @MedALMusic for using this bot."
        update.message.reply_text(sorry_message)

    
        
        
def text_boolian(update,context):
    chat_id=update.effective_chat.id 
    name = 'user_'+str(chat_id)

    
    user_id = update.message.from_user.id
    channel_id = '@MedALMusic'
    state = context.bot.get_chat_member(channel_id, user_id)
    
    if not os.path.exists(os.getcwd()+'/'+str(chat_id)):
        os.mkdir(os.getcwd()+'/'+str(chat_id))
        
    if state.status != "left" :
        
        chat_id = update.effective_chat.id
        name = 'user_'+str(chat_id)
        date_time = str(datetime.datetime.now())
        
        try:
            if(isinstance(globals()[name], Users)):
                globals()[name].text = 1
                globals()[name].count = 1
                user_name = globals()[name].user_name
        except:
            globals()[name] = Users(name,1,1,1)
            user_name = update.message.chat_id
        try:
            print(user_name+" text request at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" text request at "+date_time)
        except:
            print(str(chat_id)+" text request at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" text request at "+date_time)
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        # gidence_message = "خب حالا هر متنی که می‌خوای رو برام بفرست، فقط حواست باشه که همش رو داخل یک پیام بفرستی و بعد از هر خط حتما enter بزنی"
        gidence_message = "Send the text that you want to put on the first page of the pdf.(don't forget to use enter)"
        update.message.reply_text(gidence_message)
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        # sorry_message = "همممم، فکر کنم هنوز عضو کانال @MedALMusic نشدی، برای حمایت از ما لطفا عضو کانال شو، بعدش میتونی با فرستادن دوباره دستور از خدماتمون استفاده کنی :)"
        sorry_message = "You must first join @MedALMusic for using this bot."
        update.message.reply_text(sorry_message)
        
    
    
def text_handler(update,context):
    chat_id = []
    chat_id = update.effective_chat.id
    name = 'user_'+str(chat_id)
    try:    
        user_name = update.effective_user.username
    except :
        
       try:
           user_name = update.message.from_user.username
       except:
           user_name=globals()[name].user_name
    Exit = 0
    
    
    mail_boolian = globals()[name].mail 
    
    if mail_boolian and globals()[name].PDF and Exit !=1:
        filename = globals()[name].PDF_name+'.pdf'
        path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)

        receiver_email = update.message.text
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        if "@" in receiver_email:
            # email_send_message = "برات ایمیل کردمش !"
            email_send_message "I emailed it for you!"

            email_send(path_to_file,receiver_email,JPG = 0,counts = globals()[name].count,First_page = globals()[name].text)


        else:
            # email_send_message = " یک مشکلی پیش اومد نتونستم ایمیل کنم برات :("
            email_send_message = "Something went wrong :("

        globals()[name].mail  = 0

        os.remove(path_to_file)
        globals()[name].history = globals()[name].history + 1
        date_time = str(datetime.datetime.now())
        try :
            print(user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        except:
            print(str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        update.message.reply_text(email_send_message) 
        globals()[name].PDF = 0
        globals()[name].mail  = 0
        Exit = 1
        
    if mail_boolian==0 and globals()[name].PDF == 0 and Exit !=1: 
        if globals()[name].text == 1 :
            text = update.message.text
            text = text.splitlines()
            filename = ""
            path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename)
            poem = 1
            text_put(path_to_file,text,poem)
            globals()[name].text = 2
            context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
            # gidence_message = "عکس‌هایی که می‌خوای اسکن کنم رو به ترتیب برام بفرست و بعدش که آپلود شدن، /end رو بزن." + "\n" + "پیشنهاد می‌کنم عکس‌هات رو کراپ کنی بعد بفرستی."
            gidence_message = "Send me the images and wait till they be uploaded then click on /end"+ "\n" +"I highly recommend crop them first"
            update.message.reply_text(gidence_message)
        else:
            context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
            # gidence_message = "لطفا برام عکس بفرست، نه متن :)"
            gidence_message = "Please send me image, not text"
            update.message.reply_text(gidence_message)
        

        
        
    if globals()[name].PDF and mail_boolian==0 and Exit !=1:
        text = update.message.text
        text = text.splitlines()
        globals()[name].PDF_name =text[0]
        send(update,context)
        
        
        
    if globals()[name].PDF==0 and mail_boolian and Exit !=1:  
        filename_main = ""
        path_to_file = pjoin(os.getcwd()+"/", str(chat_id), filename_main)
        receiver_email = update.message.text
        context.bot.send_chat_action(chat_id=update.message.chat_id , action = ChatAction.TYPING)
        if "@" in receiver_email:
            # email_send_message = "برات ایمیل کردمش !"
            email_send_message = "I emailed it to you!"
            email_send(path_to_file,receiver_email,1,globals()[name].count,First_page = globals()[name].text)

        else:
            # email_send_message =  " یک مشکلی پیش اومد نتونستم ایمیل کنم برات :("
            email_send_message = "Something went wrong :("
        
        globals()[name].count = 1
        globals()[name].mail  = 0
        globals()[name].text = 0
        
        context.bot.sendMessage(chat_id=chat_id, text=email_send_message)
        globals()[name].history = globals()[name].history + 1
        date_time = str(datetime.datetime.now())
        try :
            print(user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=user_name+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        except:
            print(str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
            context.bot.sendMessage(chat_id='@AL_Med_bot_logs_2821', text=str(chat_id)+" work number "+ str(globals()[name].history - 1) +" done at "+date_time)
        globals()[name].PDF = 0
        globals()[name].text = 0
        Exit = 1
        
        

def main():
    """Start the bot."""
    API = "" #MedAL

    updater = Updater(API, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("image", begin))
    dp.add_handler(CommandHandler("end", file_type))
    dp.add_handler(CommandHandler("text", text_boolian))
    dp.add_handler(CommandHandler("example", example))
    dp.add_handler(CommandHandler("privacy", privacy))

    dp.add_handler(MessageHandler(Filters.text , text_handler))
    dp.add_handler(MessageHandler(Filters.photo, image))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()