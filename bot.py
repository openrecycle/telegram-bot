import csv
import json
import logging
import os
import sqlite3
import time

import requests
from pydub import AudioSegment
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from wit import Wit

import functions
from functions import text_search, make_text, find_points, \
    get_user_location, get_google_points, make_text_by_id, make_text_for_point, \
    get_waste_type, record_current_item, record_0_answered, record_1_answered, get_declination, check_location, \
    get_id_by_name, get_pic_by_id, record_location_status, get_location_status, \
    change_location_status
from special.config import FILEDIR, DATABASE, TELEGRAM_TOKEN, API, WIT_TOKEN
from text import start_answer, location_answer, end_text, \
    help_answer, rate_answer, about_answer, location_command_answer

telegram_token = TELEGRAM_TOKEN
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

# PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

connect = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

general_types = ('бумага', 'стекло', 'пластик', 'метал', 'опасные отходы', 'батарейки',
                     'бытовая техника', 'одежда', 'тетрапак', 'лампочки')

def start(bot, update):
    # location_keyboard = KeyboardButton(text="Прислать местоположение", request_location=True)
    # keyboard = [[location_keyboard]]
    # reply_markup = ReplyKeyboardMarkup(keyboard)
    save_user(bot,update)
    bot.sendMessage(text=start_answer, chat_id=update.message.chat.id, parse_mode='HTML')


def save_user(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id=?)", (telegram_id,))
    if cursor.fetchone()[0] == 0:
        insert_query = '''INSERT INTO users (telegram_id,username,first_name,last_name)
            values(?,?,?,?)'''
        cursor.execute(insert_query, (telegram_id, username, first_name, last_name))
        connect.commit()

def save_location(bot, update, lat=1, lng=1):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    try:
        latitude = update.message.location.latitude
    except:
        latitude = lat
    try:
        longitude = update.message.location.longitude
    except:
        longitude = lng
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
    location = functions.get_user_location(update.message.from_user.id)
    checked_location = check_location(location)
    if (checked_location == True) and type(checked_location) != str:
        bot.sendMessage(text=location_answer, chat_id=update.message.chat.id, reply_markup=ReplyKeyboardRemove())
        answered = functions.get_answered(update.message.from_user.id)
        print(answered)
        if answered == 0:
            location = functions.get_user_location(update.message.from_user.id)
            current_item = functions.get_current_item(update.message.from_user.id)
            points = functions.find_points(location, current_item)
            google_points = functions.get_google_points(points, location)
            current_item = get_declination(current_item)
            caption_text = 'Сдать <b>' + current_item + '</b> можно здесь:'
            bot.sendMessage(text=caption_text, chat_id=update.message.chat.id, parse_mode='HTML')
            for point in google_points:
                point_text = make_text_for_point(point)
                print('pp',point)
                bot.sendMessage(text=point_text, chat_id=update.message.chat.id, parse_mode='HTML')
                bot.sendLocation(chat_id=update.message.chat.id, \
                                 latitude=point[2], longitude=point[3])
            record_1_answered(telegram_id)
            bot.sendMessage(text=end_text, chat_id=update.message.chat.id, parse_mode='HTML')
    else:
        bot.sendMessage(text=checked_location, chat_id=update.message.chat.id, parse_mode='HTML')

def process_text(bot,update):
    location_status = get_location_status(update.message.from_user.id)
    print(location_status)
    if location_status == 0:
        address = update.message.text
        API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
        API_TOKEN = 'AIzaSyAOLhmNwWfsNxmQwOuLl-anPN_caKbB1k0'
        query = API_URL + 'address=' + address + '&key=' + API_TOKEN + '&language=ru'
        response = requests.get(query)
        text = json.loads(response.text)
        lat = text['results'][0]['geometry']['location']['lat']
        lng = text['results'][0]['geometry']['location']['lng']
        city = text['results'][0]['address_components'][2]['long_name']
        street = text['results'][0]['address_components'][1]['short_name']
        number = text['results'][0]['address_components'][0]['long_name']
        address = city + ', ' + street + ', ' + number
        location_text = 'Ваш адрес: ' + address+'.'
        markup = ReplyKeyboardRemove(remove_keyboard=True)
        bot.sendMessage(text=location_text, chat_id=update.message.chat.id,
                                parse_mode='HTML', reply_markup=markup)
        save_location(bot,update, lat,lng)
        change_location_status(update.message.chat.id)
        return
    else:
        pass


    #get text and normalize it
    waste_item = update.message.text.lower()
    with open('logs.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([update.message.chat.id, 'text', waste_item])
    waste_item.lower().strip()
    if waste_item == 'металл':
        waste_item = 'метал'
    if waste_item == 'макулатура':
        waste_item = 'бумага'
    #search text in database
    result = text_search(waste_item)
    #if we have exact answer...
    if type(result) == tuple:
        waste_text = make_text(result)
        photopath = 'pics/' + result[3]
        general_type = result[1]
        record_current_item(update.message.from_user.id, general_type)
        record_0_answered(update.message.from_user.id)
        # print('answered recorded')
        bot.sendMessage(text=waste_text, chat_id=update.message.chat.id, parse_mode='HTML')
        if result[4] == 1:
            try:
                keyboard = [[InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=general_type)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'), \
                              reply_markup=reply_markup)
                bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                                parse_mode='HTML')
            except FileNotFoundError:
                print('no photo')
        else:
            try:
                bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'))
                bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                                parse_mode='HTML')
                record_1_answered(update.message.chat.id)
            except FileNotFoundError:
                print('no photo')
    elif result in general_types:
        record_current_item(update.message.from_user.id, waste_item)
        record_0_answered(update.message.from_user.id)
        try:
            location = get_user_location(update.message.chat.id)
            location_checked = check_location(location)
            if location_checked == True and type(location_checked) != str:
                points = find_points(location, waste_item)
                google_points = get_google_points(points, location)
                for point in google_points:
                    print('ppp', point)
                    point_text = make_text_for_point(point)
                    bot.sendMessage(text=point_text, chat_id=update.message.chat.id, parse_mode='HTML')
                    bot.sendLocation(chat_id=update.message.chat.id,\
                                     latitude=point[2], longitude=point[3])
                bot.sendMessage(text=end_text, chat_id=update.message.from_user.id,
                                parse_mode='HTML')
            else:
                bot.sendMessage(text=location_checked, chat_id=update.message.chat.id, parse_mode='HTML')

        except TypeError:
            location_keyboard = KeyboardButton(text="Прислать местоположение", request_location=True)
            keyboard = [[location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(keyboard)
            bot.sendMessage(text='''Пожалуйста, пришлите местоположение.\n\
Также вы можете просто написать свой адрес.''',
                            chat_id=update.message.from_user.id, parse_mode='HTML',
                            reply_markup=reply_markup)

    #we have variants...
    elif type(result) == list and len(result) > 0:
        keyboard = []
        for item in result:
            if len(item) > 34:
                item = item[:34]
            item_id = get_id_by_name(item)
            print('id',item_id)
            keyboard.append(InlineKeyboardButton(item, callback_data='text'+str(item_id)))
            print(item)
        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
        bot.sendMessage(text='Выберите', chat_id=update.message.chat.id, parse_mode='HTML',
                        reply_markup=reply_markup)
    else:
        bot.sendMessage(text=result, chat_id=update.message.chat.id, parse_mode='HTML')


def process_audio(bot,update):
    print(132)
    audio_file = bot.getFile(update.message.voice.file_id)
    if not os.path.exists('files'):
        os.mkdir('files')
    text = ''

    fn = "files/{}-{}-{}-{}.ogg".format(update.message.from_user.id, text, time.time(), '001')
    audio_file.download(fn)

    print("converting ogg to wav")
    sound = AudioSegment.from_ogg(fn)
    sound.export("audio.wav", format="wav")
    print("wit.ai")

    def send(request, response):
        print('Sending to user...', response['text'])

    def my_action(request):
        print('Received from user...', request['text'])

    actions = {
        'send': send,
        'my_action': my_action,
    }

    client = Wit(access_token=WIT_TOKEN, actions=actions)

    resp = None
    with open('audio.wav', 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})

    print(type(resp))
    print(resp['_text'])

    try:
        result = text_search(resp['_text'].lower())
        with open('logs.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([update.message.chat.id, 'audio', resp['_text'].lower()])
        print(result)
        voice_text = '<b>Вы спросили: </b>'+resp['_text'].lower()
        bot.sendMessage(chat_id=update.message.chat.id, text=voice_text, parse_mode='HTML')
        if type(result) == tuple:
            waste_item = make_text(result)
            photopath = 'pics/' + result[3]
            print(photopath)
            data = result[1]
            print(data)
            item_id = get_id_by_name(result[1])
            print('item_id', item_id)
            keyboard = [[InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=str(item_id))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(text=waste_item, chat_id=update.message.chat.id, parse_mode='HTML')
            print('audio')
            if result[4] == 1:
                #todo убрать лишнее
                try:
                    bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'), \
                                  reply_markup=reply_markup)
                    bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                                    parse_mode='HTML')
                except FileNotFoundError:
                    print('no photo')
            else:
                try:
                    bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'))
                    bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                                    parse_mode='HTML')
                except FileNotFoundError:
                    print('no photo')

        # we have variants...
        elif type(result) == list and len(result) > 0:
            keyboard = []
            for item in result:
                if len(item) > 34:
                    item = item[:34]
                item_id = get_id_by_name(item)
                print('id', item_id)
                keyboard.append(InlineKeyboardButton(item, callback_data='text' + str(item_id)))
                print(item)
            reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
            bot.sendMessage(text='Выберите', chat_id=update.message.chat.id, parse_mode='HTML',
                            reply_markup=reply_markup)
        else:
            bot.sendMessage(text=result, chat_id=update.message.chat.id, parse_mode='HTML')

    except AttributeError:
        voice_text = 'Простите, не удалось распознать заданное слово. Попробуйте еще.\n\U00002328 \U0001F4F7 \U0001F399'
        bot.sendMessage(chat_id=update.message.chat.id, text=voice_text, parse_mode='HTML')
    # if we have exact answer...


def process_photo(bot, update):
    print('photo')
    # create directory for files
    if not os.path.exists('files'):
        os.mkdir(FILEDIR)
    # get file from user
    file = bot.getFile(update.message.photo[-1].file_id)
    filename = FILEDIR + '/' + "{}-{}.jpg".format( time.time(), 'test')
    print(filename)
    file.download(filename)
    # send file to API
    USER_ID = update.message.chat.id
    file = {'file': ('image.jpg', open(filename, 'rb'), 'image/jpg', {'Expires': '0'})}
    data = {
        'user_id': USER_ID,
        'filename': filename
    }
    r = requests.put(API, files=file, data=data)
    # read response, get waste_item id
    text = json.loads(r.text)
    print(text)
    waste_item_id = text['Id']
    with open('logs.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([update.message.chat.id, 'photo', waste_item_id])
    print(waste_item_id)
    # make text
    text = make_text_by_id(waste_item_id)
    # get waste_type
    if 'Простите' in text:
        bot.sendMessage(text=text, chat_id=update.message.chat.id, parse_mode='HTML')
    else:
        general_type = get_waste_type(waste_item_id)
        record_current_item(update.message.from_user.id, general_type)
        record_0_answered(update.message.from_user.id)
        # if recycable
        if 'Не принимается' not in text:
            keyboard = [[InlineKeyboardButton('\U00002705Согласен с ответом', callback_data='yes'+filename)],
                            [InlineKeyboardButton('\U0000274CНе согласен с ответом', callback_data='nope'+filename)],
                        [InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=general_type)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(keyboard)
            bot.sendMessage(text=text, chat_id=update.message.chat.id, parse_mode='HTML',\
                            reply_markup=reply_markup)
            bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                        parse_mode='HTML')
        #if not (without "where" button)
        else:
            keyboard = [[InlineKeyboardButton('\U00002705Согласен с ответом', callback_data='yes'+filename)],
                            [InlineKeyboardButton('\U0000274CНе согласен с ответом', callback_data='nope'+filename)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.sendMessage(text=text, chat_id=update.message.chat.id, parse_mode='HTML',\
                            reply_markup=reply_markup)
            bot.sendMessage(text=end_text, chat_id=update.message.chat.id,
                            parse_mode='HTML')

def button(bot, update):
    query = update.callback_query
    waste = query.data
    if 'nope' in waste or 'yes' in waste:
        thanx_text = '''Спасибо за обратную связь, \
ваш отзыв будет использован для улучшения распознающего алгоритма.'''
        with open('logs.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([update.callback_query.from_user.id, 'photo', waste])
        bot.sendMessage(chat_id=update.callback_query.from_user.id,text=thanx_text)
        bot.sendMessage(text=end_text, chat_id=update.callback_query.from_user.id,
                        parse_mode='HTML')
    elif waste in general_types:
        try:
            location = get_user_location(update.callback_query.from_user.id)
            checked_location = check_location(location)
            # print(location)
            if checked_location == True and type(checked_location) != 1:
                points = find_points(location, waste)
                google_points = get_google_points(points, location)
                # print(google_points)
                for point in google_points:
                    print('ppp', point)
                    point_text = make_text_for_point(point)
                    bot.sendMessage(text=point_text, chat_id=update.callback_query.from_user.id, \
                                    parse_mode='HTML')
                    bot.sendLocation(chat_id=update.callback_query.from_user.id,\
                                     latitude=point[2], longitude=point[3])
                bot.sendMessage(text=end_text, chat_id=update.callback_query.from_user.id,
                                parse_mode='HTML')
            else:
                bot.sendMessage(text=checked_location, chat_id=update.message.chat.id, parse_mode='HTML')
        # if there is no location...
        except TypeError:
            location_keyboard = KeyboardButton(text="Прислать местоположение", request_location=True)
            keyboard = [[location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(keyboard)
            bot.sendMessage(text='''Пожалуйста, пришлите местоположение. \n\
Также вы можете просто написать свой адрес.''',
                            chat_id=update.callback_query.from_user.id, parse_mode='HTML',
                            reply_markup=reply_markup)
            # location = get_user_location(update.callback_query.from_user.id)
            #
            # print(location)
            # print('location got')
            record_location_status(update.callback_query.from_user.id)
    elif 'text' in waste:
        text = make_text_by_id(waste[4:])
        photopath = 'pics/' + get_pic_by_id(waste[4:])
        general_type = get_waste_type(waste[4:])
        record_current_item(update.callback_query.from_user.id, general_type)
        record_0_answered(update.callback_query.from_user.id)
        # print(photopath)
        if 'Простите' in text:
            bot.sendMessage(text=text, chat_id=update.message.chat.id, parse_mode='HTML')
        else:
            general_type = get_waste_type(waste[4:])
            # if recycable
            if 'Не принимается' not in text:
                keyboard = [[InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=general_type)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.sendPhoto(chat_id=update.callback_query.from_user.id, photo=open(photopath, 'rb'))
                bot.sendMessage(text=text, chat_id=update.callback_query.from_user.id, parse_mode='HTML', \
                                reply_markup=reply_markup)

                bot.sendMessage(text=end_text, chat_id=update.callback_query.from_user.id,
                            parse_mode='HTML')
            # if not (without "where" button)
            else:
                # keyboard = [[InlineKeyboardButton('\U00002705 Согласен с ответом', callback_data='yes')],
                #             [InlineKeyboardButton('\U0000274C Не согласен с ответом', callback_data='nope')]]
                # reply_markup = InlineKeyboardMarkup(keyboard)
                bot.sendPhoto(chat_id=update.callback_query.from_user.id, photo=open(photopath, 'rb'))
                bot.sendMessage(text=text, chat_id=update.callback_query.from_user.id, parse_mode='HTML')
                bot.sendMessage(text=end_text, chat_id=update.callback_query.from_user.id,
                                parse_mode='HTML')
    elif type(int(waste)) == int:
        text = make_text_by_id(waste)
        if 'Простите' in text:
            bot.sendMessage(text=text, chat_id=update.message.chat.id, parse_mode='HTML')
        else:
            general_type = get_waste_type(waste)
            # if recycable
            if 'Не принимается' not in text:
                keyboard = [[InlineKeyboardButton('\U00002705Согласен с ответом', callback_data='yes')],
                            [InlineKeyboardButton('\U0000274CНе согласен с ответом', callback_data='nope')],
                            [InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=general_type)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                print(keyboard)
                bot.sendMessage(text=text, chat_id=update.callback_query.from_user.id, parse_mode='HTML', \
                                reply_markup=reply_markup)
                bot.sendMessage(text=end_text, chat_id=update.callback_query.from_user.id,
                                parse_mode='HTML')
            # if not (without "where" button)
            else:
                # keyboard = [[InlineKeyboardButton('\U00002705 Согласен с ответом', callback_data='yes')],
                #             [InlineKeyboardButton('\U0000274C Не согласен с ответом', callback_data='nope')]]
                # reply_markup = InlineKeyboardMarkup(keyboard)
                bot.sendMessage(text=text, chat_id=update.callback_query.from_user.id, parse_mode='HTML')
    else:
        print('else '+waste)
        result = text_search(waste)
        print('!!', result)
        # if we have exact answer...
        if type(result) == tuple:

            waste_item = make_text(result)
            print(waste_item)
            photopath = 'pics/' + result[3]
            data = result[1]
            record_current_item(update.callback_query.from_user.id, data)
            keyboard = [[InlineKeyboardButton('\U0001F4CDГде сдать', callback_data=data)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(text=waste_item, chat_id=update.callback_query.from_user.id, parse_mode='HTML')
            if result[4] == 1:
                try:
                    bot.sendPhoto(chat_id=update.callback_query.from_user.id, photo=open(photopath, 'rb'), \
                                  reply_markup=reply_markup)
                except FileNotFoundError:
                    print('no photo')
            else:
                try:
                    bot.sendPhoto(chat_id=update.message.chat.id, photo=open(photopath, 'rb'))
                except FileNotFoundError:
                    print('no photo')

def build_menu(buttons: list,
               n_cols: int,
               header_buttons: list = None,
               footer_buttons: list = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def help_command(bot, update):
    bot.sendMessage(text=help_answer, chat_id=update.message.chat.id, parse_mode='HTML')

def rate_command(bot,update):
    bot.sendMessage(text=rate_answer, chat_id=update.message.chat.id, parse_mode='HTML')

def about_command(bot, update):
    bot.sendMessage(text=about_answer, chat_id=update.message.chat.id, parse_mode='HTML')

def location_command(bot, update):
    record_location_status(update.message.chat.id)
    bot.sendMessage(text=location_command_answer, chat_id=update.message.chat.id, parse_mode='HTML')


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
rate_handler = CommandHandler('rate', rate_command)
about_handler = CommandHandler('about', about_command)
location_command_handler = CommandHandler('location', location_command)
location_handler = MessageHandler(Filters.location, save_location)
text_handler = MessageHandler(Filters.text, process_text)
audio_handler = MessageHandler(Filters.voice, process_audio)
photo_handler = MessageHandler(Filters.photo|Filters.document, process_photo)
button_handler = CallbackQueryHandler(button)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(rate_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(audio_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(location_command_handler)

if __name__ == '__main__':
    # updater.start_polling()
    updater.start_webhook(listen='127.0.0.1', port=5000, url_path='TOKEN1')
    updater.bot.set_webhook(webhook_url='https://example.com/TOKEN1',
                            certificate=open('cert.pem', 'rb'))
