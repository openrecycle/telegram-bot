from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
import os
import logging
import config
from text import start_answer, location_answer, text_answer, audio_answer, photo_answer
import sqlite3

telegram_token = config.telegram_token
db = config.database
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

connect = sqlite3.connect(db, check_same_thread=False)
cursor = connect.cursor()

def start(bot, update):
    bot.sendMessage(text=start_answer, chat_id=update.message.chat.id)

def save_location(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id=?)",(telegram_id,))
    if cursor.fetchone()[0] == 0
        insert_query = '''INSERT INTO users (telegram_id,username,first_name,last_name,latitude,longitude)
        values(?,?,?,?,?,?)'''
        cursor.execute(insert_query,(telegram_id, username, first_name, last_name, latitude,longitude))
        connect.commit()
    else:
        update_query='''UPDATE users SET latitude=?,longitude=? WHERE telegram_id=?'''
        cursor.execute(update_query, (latitude,longitude,telegram_id))
        connect.commit()
    bot.sendMessage(text=location_answer, chat_id=update.message.chat.id)

def check_query(id):
    query = '''SELECT * FROM users WHERE telegram_id - ?'''
    cursor.execute(query, (id,))
    if cursor.fetchone() == None:
        return True

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

