from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import sqlite3
import time
import requests
import json
from functions import text_search, make_text, make_variants_text, find_points,\
    get_user_location, get_google_points
from config import FILEDIR, DATABASE, TELEGRAM_TOKEN, API
from text import start_answer, location_answer, audio_answer, paper, plastik, tetrapak

telegram_token = TELEGRAM_TOKEN
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

connect = sqlite3.connect(DATABASE, check_same_thread=False)
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
    if cursor.fetchone()[0] == 0:
        insert_query = '''INSERT INTO users (telegram_id,username,first_name,last_name,latitude,longitude)
        values(?,?,?,?,?,?)'''
        cursor.execute(insert_query,(telegram_id, username, first_name, last_name, latitude,longitude))
        connect.commit()
    else:
        update_query='''UPDATE users SET latitude=?,longitude=? WHERE telegram_id=?'''
        cursor.execute(update_query, (latitude,longitude,telegram_id))
        connect.commit()
    bot.sendMessage(text=location_answer, chat_id=update.message.chat.id)

def process_text(bot,update):
    waste_item = update.message.text.lower()
    result = text_search(waste_item)
    print(result)

    if type(result) == tuple:
        waste_item = make_text(result)
        photopath = 'pics/' + result[2]
        bot.sendMessage(text=waste_item, chat_id=update.message.chat.id, parse_mode='HTML')
        try:
            bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'))
        except FileNotFoundError:
            pass
        geo = get_user_location(update.message.from_user.id)
        points = find_points(geo, result[0])
        get_google_points(points, geo)
    elif type(result) == list and len(result) > 0:
        waste_item = make_variants_text(result)
        geo = get_user_location(update.message.from_user.id)
        # approximate points calculated simply
        points = find_points(geo, result[0])
        # certain point calculated with google api
        true_points = get_google_points(points, geo)
        
        bot.sendMessage(text=waste_item, chat_id=update.message.chat.id, parse_mode='HTML')
    else:
        bot.sendMessage(text=result, chat_id=update.message.chat.id, parse_mode='HTML')


def process_audio(bot,update):

    bot.sendMessage(text=audio_answer, chat_id=update.message.chat.id)

def process_photo(bot, update):
    if not os.path.exists('files'):
        os.mkdir(FILEDIR)
    f = bot.getFile(update.message.photo[-1].file_id)
    fn = FILEDIR + '/' + "{}-{}.jpg".format( time.time(), 'test')
    f.download(fn)
    file = {'file': open(fn, 'rb')}
    r = requests.put(API, files=file)
    text = json.loads(r.text)
    text = text['Message']

    bot.sendMessage(text=text, chat_id=update.message.chat.id)

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

