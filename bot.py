from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import config
from text import start_answer, location_answer, text_answer, audio_answer, photo_answer

telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(text=start_answer, chat_id=update.message.chat.id)

def save_location(bot, update):
    bot.sendMessage(text=location_answer, chat_id=update.message.chat.id)

def process_text(bot,update):
    bot.sendMessage(text=text_answer, chat_id=update.message.chat.id)

def process_audio(bot,update):
    bot.sendMessage(text=audio_answer, chat_id=update.message.chat.id)

def process_photo(bot, update):
    bot.sendMessage(text=photo_answer, chat_id=update.message.chat.id)


start_handler = CommandHandler('start', start)
location_handler = MessageHandler(Filters.location, save_location)
text_handler = MessageHandler(Filters.text, process_text)
audio_handler = MessageHandler(Filters.audio, process_audio)
photo_handler = MessageHandler(Filters.photo, process_photo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(audio_handler)
dispatcher.add_handler(photo_handler)

if __name__ == '__main__':
    updater.start_polling()

