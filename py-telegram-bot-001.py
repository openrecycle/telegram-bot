# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
#import config
import csv


telegram_token = "342496596:AAGdzdiuSuNB7kcx4uDsqtNsEkghg0PXa58"
#telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(telegram_token)
dispatcher = updater.dispatcher

def find_address(district=None):
    if district!=None:
        with open('districts.csv') as csvfile:
             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
             for row in reader:
                 if district == row[0]:
                     return row[1]
    else:
        return ""


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Hello! This is Telegram Bot! I help you recycle your garbage.')

"""
/recycle
/where
/types
"""

def recycle_cmd(bot, update, **args):
    print (args)
    bot.sendMessage(chat_id=update.message.chat.id, text='recycle!!')
    recycle_args = args.get("args")
    bot.sendMessage(chat_id=update.message.chat.id, text=len(recycle_args).__str__())

def where_cmd(bot, update, **args):
    msgText = 'where!!'
    where_args = args.get("args")
    buttonsListFlg=False
    address = ""
    if len(where_args) > 0:
        print (where_args[0])
        address= find_address(where_args[0])
        if address!="":
            msgText=msgText+' '+address;
        else:
            buttonsListFlg=True
    else:
        buttonsListFlg=True
    if buttonsListFlg:
        msgText=msgText+'\n'+"Buttons lists with adresses"
    bot.sendMessage(chat_id=update.message.chat.id, text=msgText)
    bot.sendMessage(chat_id=update.message.chat.id, text="1")
    
    
def types_cmd(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='types!!')

def help_cmd(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Help:')
    
start_handler = CommandHandler('start', start)
recycle_handler = CommandHandler('recycle', recycle_cmd, pass_args=True)
where_handler = CommandHandler('where', where_cmd, pass_args=True)
types_handler = CommandHandler('types', types_cmd)
help_handler = CommandHandler('helpme', help_cmd)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(recycle_handler)
dispatcher.add_handler(where_handler)
dispatcher.add_handler(types_handler)
dispatcher.add_handler(help_handler)

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
    #updater.start_webhook(listen='127.0.0.1', port=5003, url_path=telegram_token)
    #updater.bot.setWebhook(webhook_url='https://95.85.37.72/'+telegram_token,
    #                       certificate=open('/home/deploy/it-volunteer-bot/cert.pem', 'rb'))
    print('hi')
