MedAl Document Scanner
==============================

What Is This?
-------------
This is a telegrom bot written in python using telegram-python library. This bot can scan images and make PDF files from those scanned images.

How To Use This
-------------
You need to first make a bot and take an API for it from [@BotFather](https://t.me/BotFather) and then change `API` in `EasyScanner.py` and run it!
Note that this bot doesn't use any databse for saving clients informations or logs, but there is a meta class which stores all the informations.

How to customize it?
-------------
First change `MainChannel` and `LogChannel` to your channels. `MainChannel` is the id of the channel wich all users must be its member in order to use the bot and `LogChannel` is the channel which all the logs are sended to it 
##### note that your bot must be an admin in both of the channels

- Change `text_puter.py` for changing font, color, and ... of the text.
- Change `RandD.py` for changing image scanning algorithm.
- add an email to `send_email.py`
