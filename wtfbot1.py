import logging

from telegram.ext import Filters, MessageHandler, Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import codecs
import csv

import requests

from config import TOKEN
from interface import metro_button_list
from handlers import recycle_cmd, where_cmd, types_cmd, help_cmd, metro_cmd, start, button, image_rec

class Flags:
    model_dir = "."
FLAGS = Flags()

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
logger = logging.getLogger(__name__)

"""
/recycle
/where
/types
/metro
"""

start_handler = CommandHandler('start', start)
recycle_handler = CommandHandler('recycle', recycle_cmd, pass_args=True)
where_handler = CommandHandler('where', where_cmd, pass_args=True)
# types_handler = CommandHandler('types', types_cmd, pass_args=True)
help_handler = CommandHandler('help', help_cmd)
metro_handler = CommandHandler('metro', metro_cmd, pass_args=True)
image_handler = MessageHandler(Filters.photo, image_rec)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(recycle_handler)
dispatcher.add_handler(where_handler)
# dispatcher.add_handler(types_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(metro_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(image_handler)

#telegram_token = "342496596:AAGdzdiuSuNB7kcx4uDsqtNsEkghg0PXa58"

# metro_reply_markup = InlineKeyboardMarkup(build_menu(metro_button_list, n_cols=3))

def main():
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

'''
Row numers:
0-id
1-class
2-eng
3-take
4-tags
5-url
6-
7-Комментарий
'''
