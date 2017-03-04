# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import base
import os
import logging
import config
import codecs
import csv


#telegram_token = "342496596:AAGdzdiuSuNB7kcx4uDsqtNsEkghg0PXa58"
telegram_token = config.TOKEN
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(telegram_token)
dispatcher = updater.dispatcher

spb_adm=u'адмиралтейский'
spb_vas=u'василеостровский'
spb_vyb=u'выборгский'
spb_kln=u'калининский'
spb_kir=u'кировский'
spb_krg=u'красногвардейский'
spb_krs=u'красносельский'
spb_krd=u'кронштадский'
spb_msk=u'московский'
spb_nev=u'невский'
spb_prd=u'петроградский'
spb_pdv=u'петродворцовый'
spb_prm=u'приморский'
spb_frz=u'фрунзенский'
spb_cnt=u'центральный'

keyboard = [[InlineKeyboardButton(spb_adm, callback_data='spb_adm')], # адмиралтейский
            [InlineKeyboardButton(spb_vas, callback_data='spb_vas')], # василеостровский
            [InlineKeyboardButton(spb_vyb, callback_data='spb_vyb')], # выборгский
            [InlineKeyboardButton(spb_kln, callback_data='spb_kln')], # калининский
            [InlineKeyboardButton(spb_kir, callback_data='spb_kir')], # кировский
            [InlineKeyboardButton(spb_krg, callback_data='spb_krg')], # красногвардейский
            [InlineKeyboardButton(spb_krs, callback_data='spb_krs')], # красносельский
            [InlineKeyboardButton(spb_krd, callback_data='spb_krd')], # кронштадский
            [InlineKeyboardButton(spb_msk, callback_data='spb_msk')], # московский
            [InlineKeyboardButton(spb_nev, callback_data='spb_nev')], # невский
            [InlineKeyboardButton(spb_prd, callback_data='spb_prd')], # петроградский
            [InlineKeyboardButton(spb_pdv, callback_data='spb_pdv')], # петродворцовый
            [InlineKeyboardButton(spb_prm, callback_data='spb_prm')], # приморский
            [InlineKeyboardButton(spb_frz, callback_data='spb_frz')], # фрунзенский
            [InlineKeyboardButton(spb_cnt, callback_data='spb_cnt')]  # центральны                
            ]

metro_button_list = [
    InlineKeyboardButton("ст.м. Автово",                           callback_data='spb_01'),
    InlineKeyboardButton("ст.м. Адмиралтейская",                   callback_data='spb_02'),
    InlineKeyboardButton("ст.м. Академическая",                    callback_data='spb_03'),
    InlineKeyboardButton("ст.м. Балтийская",                       callback_data='spb_04'),
    InlineKeyboardButton("ст.м. Бухарестская",                     callback_data='spb_05'),
    InlineKeyboardButton("ст.м. Василеостровская",                 callback_data='spb_06'),
    InlineKeyboardButton("ст.м. Владимирская",                     callback_data='spb_07'),
    InlineKeyboardButton("ст.м. Волковская",                       callback_data='spb_08'),
    InlineKeyboardButton("ст.м. Выборгская",                       callback_data='spb_09'),
    InlineKeyboardButton("ст.м. Горьковская",                      callback_data='spb_10'),
    InlineKeyboardButton("ст.м. Гостиный двор",                    callback_data='spb_11'),
    InlineKeyboardButton("ст.м. Гражданский проспект",             callback_data='spb_12'),
    InlineKeyboardButton("ст.м. Девяткино",                        callback_data='spb_13'),
    InlineKeyboardButton("ст.м. Достоевская",                      callback_data='spb_14'),
    InlineKeyboardButton("ст.м. Елизаровская",                     callback_data='spb_15'),
    InlineKeyboardButton("ст.м. Звёздная",                         callback_data='spb_16'),
    InlineKeyboardButton("ст.м. Звенигородская",                   callback_data='spb_17'),
    InlineKeyboardButton("ст.м. Кировский завод",                  callback_data='spb_18'),
    InlineKeyboardButton("ст.м. Комендантский проспект",           callback_data='spb_19'),
    InlineKeyboardButton("ст.м. Крестовский остров",               callback_data='spb_20'),
    InlineKeyboardButton("ст.м. Купчино",                          callback_data='spb_21'),
    InlineKeyboardButton("ст.м. Ладожская",                        callback_data='spb_22'),
    InlineKeyboardButton("ст.м. Ленинский проспект",               callback_data='spb_23'),
    InlineKeyboardButton("ст.м. Лесная",                           callback_data='spb_24'),
    InlineKeyboardButton("ст.м. Лиговский проспект",               callback_data='spb_25'),
    InlineKeyboardButton("ст.м. Ломоносовская",                    callback_data='spb_26'),
    InlineKeyboardButton("ст.м. Маяковская",                       callback_data='spb_27'),
    InlineKeyboardButton("ст.м. Международная",                    callback_data='spb_28'),
    InlineKeyboardButton("ст.м. Московская",                       callback_data='spb_29'),
    InlineKeyboardButton("ст.м. Московские ворота",                callback_data='spb_30'),
    InlineKeyboardButton("ст.м. Нарвская",                         callback_data='spb_31'),
    InlineKeyboardButton("ст.м. Невский проспект",                 callback_data='spb_32'),
    InlineKeyboardButton("ст.м. Новочеркасская",                   callback_data='spb_33'),
    InlineKeyboardButton("ст.м. Обводный канал",                   callback_data='spb_34'),
    InlineKeyboardButton("ст.м. Обухово",                          callback_data='spb_35'),
    InlineKeyboardButton("ст.м. Озерки",                           callback_data='spb_36'),
    InlineKeyboardButton("ст.м. Парк Победы",                      callback_data='spb_37'),
    InlineKeyboardButton("ст.м. Парнас",                           callback_data='spb_38'),
    InlineKeyboardButton("ст.м. Петроградская",                    callback_data='spb_39'),
    InlineKeyboardButton("ст.м. Пионерская",                       callback_data='spb_40'),
    InlineKeyboardButton("ст.м. Площадь Александра Невского 1",    callback_data='spb_41'),
    InlineKeyboardButton("ст.м. Площадь Александра Невского 2",    callback_data='spb_42'),
    InlineKeyboardButton("ст.м. Площадь Восстания",                callback_data='spb_43'),
    InlineKeyboardButton("ст.м. Площадь Ленина",                   callback_data='spb_44'),
    InlineKeyboardButton("ст.м. Площадь Мужества",                 callback_data='spb_45'),
    InlineKeyboardButton("ст.м. Политехническая",                  callback_data='spb_46'),
    InlineKeyboardButton("ст.м. Приморская",                       callback_data='spb_47'),
    InlineKeyboardButton("ст.м. Пролетарская",                     callback_data='spb_48'),
    InlineKeyboardButton("ст.м. Проспект Большевиков",             callback_data='spb_49'),
    InlineKeyboardButton("ст.м. Проспект Ветеранов",               callback_data='spb_50'),
    InlineKeyboardButton("ст.м. Проспект Просвещения",             callback_data='spb_51'),
    InlineKeyboardButton("ст.м. Пушкинская",                       callback_data='spb_52'),
    InlineKeyboardButton("ст.м. Рыбацкое",                         callback_data='spb_53'),
    InlineKeyboardButton("ст.м. Садовая",                          callback_data='spb_54'),
    InlineKeyboardButton("ст.м. Сенная площадь",                   callback_data='spb_55'),
    InlineKeyboardButton("ст.м. Спасская",                         callback_data='spb_56'),
    InlineKeyboardButton("ст.м. Спортивная",                       callback_data='spb_57'),
    InlineKeyboardButton("ст.м. Старая Деревня",                   callback_data='spb_58'),
    InlineKeyboardButton("ст.м. Технологический институт 1",       callback_data='spb_59'),
    InlineKeyboardButton("ст.м. Технологический институт 2",       callback_data='spb_60'),
    InlineKeyboardButton("ст.м. Удельная",                         callback_data='spb_61'),
    InlineKeyboardButton("ст.м. Улица Дыбенко",                    callback_data='spb_62'),
    InlineKeyboardButton("ст.м. Фрунзенская",                      callback_data='spb_63'),
    InlineKeyboardButton("ст.м. Чёрная речка",                     callback_data='spb_64'),
    InlineKeyboardButton("ст.м. Чернышевская",                     callback_data='spb_65'),
    InlineKeyboardButton("ст.м. Чкаловская",                       callback_data='spb_66'),
    InlineKeyboardButton("ст.м. Электросила",                      callback_data='spb_67')
]

def build_menu(buttons: list,
               n_cols: int,
               header_buttons: list = None,
               footer_buttons: list = None):
    menu = list()
    for i in range(0, len(buttons)):
        item = buttons[i]
        if i % n_cols == 0:
            menu.append([item])
        else:
            menu[int(i / n_cols)].append(item)
    if header_buttons:
        menu.insert(0, header_buttons)
    if header_buttons:
        menu.append(footer_buttons)
    return menu

metro_reply_markup = InlineKeyboardMarkup(build_menu(metro_button_list, n_cols=3))

def find_address(district=None):
    result = ""
    if district!=None:
        #with open('D:\\Projects\\Py-Telegram-Bot\\districts.csv') as csvfile:
        with codecs.open('D:\\Projects\\Py-Telegram-Bot\\districts.csv', encoding='utf-8') as csvfile:
             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
             for row in reader:
                 if result != "":
                     result += "\n"
                 if district.lower() == row[0].lower().encode('utf-8') or district.lower() == row[0].lower()[:len(district)]:
                     result += row[1]
    return result

def find_address_by_metro(metro_name=None):
    result = ""
    if metro_name!=None:
        #with open('D:\\Projects\\Py-Telegram-Bot\\districts.csv') as csvfile:
        with codecs.open('D:\\Projects\\Py-Telegram-Bot\\districts.csv', encoding='utf-8') as csvfile:
             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
             for row in reader:
                 if result != "":
                     result += "\n"
                 if metro_name.lower() == row[1].lower().encode('utf-8') or metro_name.lower() == row[1].lower()[:len(metro_name)] or metro_name.lower() in row[1].lower():
                     result += row[1]
    return result

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Привет! Я помогу Вам правильно рассортировать Ваши отходы.'\
                    'Доступные команды:'\
                    '/start - начало работы со мой'\
                    '/helpme - помощь по командам и как мной пользоваться'\
                    '/recycle или /recycle <наименование> - введите ключевое слово, к примеру "пластиковая бутылка" и я помогу определить можно ее утилизировать или нет'\
                    '/where или /where <район города> - подскажу, где пункт сбора в вашем районе'\
                    '/types - подскажу какие отходы бывают'\
                    '/metro или /metro <станция метро> - подскажу, где пункт сбора отностельно метро')
"""
/recycle
/where
/types
/metro
"""

def recycle_cmd(bot, update, **args):
    recycle_args = args.get("args")
    if len(recycle_args) == 0:
        None
        bot.sendMessage(chat_id=update.message.chat.id, text='Допустимые классы отходов пригодные к переработке: \n')
    else:
        bot.sendMessage(chat_id=update.message.chat.id, text='Вы указали: '+ recycle_args.__str__())

def where_cmd(bot, update, **args):
    msgText = 'where!! '
    query = update.callback_query
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
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, text='Выберите пожалуйста район города:')
    else:
        bot.sendMessage(chat_id=update.message.chat.id, text=msgText)    
    
def types_cmd(bot, update, pass_args=True):
    bot.sendMessage(chat_id=update.message.chat.id, text='Допустимые классы отходов пригодные к переработке: \n')

def help_cmd(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Привет!\n'\
                    'Доступные команды:\n'\
                    '/recycle или /recycle <наименование> - введите ключевое слово, к примеру "пластиковая бутылка" и я помогу определить можно ее утилизировать или нет\n'\
                    '/where или /where <район города> - подскажу, где пункт сбора в вашем районе\n'\
                    '/types - подскажу какие отходы бывают\n'\
                    '/metro или /metro <станция метро> - подскажу, где пункт сбора отностельно метро')

def metro_cmd(bot, update, **args):
    bot.sendMessage(chat_id=update.message.chat.id, text='Метро:',reply_markup=metro_reply_markup)

def button(bot, update):
    query = update.callback_query
    city_place_code = query.data
    metro_place_code = query.data
    keyboard_back = [[InlineKeyboardButton(" «< ", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard_back)
    city_place = ""
    metro_name = ""
    if city_place_code == 'back':
        text = 'Пожалуйста, выберите, район города:'
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,message_id=query.message.message_id)
    elif city_place_code == 'spb_adm': city_place = spb_adm
    elif city_place_code == 'spb_vas': city_place = spb_vas
    elif city_place_code == 'spb_vyb': city_place = spb_vyb
    elif city_place_code == 'spb_kln': city_place = spb_kln
    elif city_place_code == 'spb_kir': city_place = spb_kir
    elif city_place_code == 'spb_krg': city_place = spb_krg
    elif city_place_code == 'spb_krs': city_place = spb_krs
    elif city_place_code == 'spb_krd': city_place = spb_krd
    elif city_place_code == 'spb_msk': city_place = spb_msk
    elif city_place_code == 'spb_nev': city_place = spb_nev
    elif city_place_code == 'spb_prd': city_place = spb_prd
    elif city_place_code == 'spb_pdv': city_place = spb_pdv
    elif city_place_code == 'spb_prm': city_place = spb_prm
    elif city_place_code == 'spb_frz': city_place = spb_frz
    elif city_place_code == 'spb_cnt': city_place = spb_cnt
    elif metro_place_code == 'spb_01': metro_name = 'ст.м. Автово'
    elif metro_place_code == 'spb_02': metro_name = 'ст.м. Адмиралтейская'               
    elif metro_place_code == 'spb_03': metro_name = 'ст.м. Академическая'                
    elif metro_place_code == 'spb_04': metro_name = 'ст.м. Балтийская'                   
    elif metro_place_code == 'spb_05': metro_name = 'ст.м. Бухарестская'                 
    elif metro_place_code == 'spb_06': metro_name = 'ст.м. Василеостровская'             
    elif metro_place_code == 'spb_07': metro_name = 'ст.м. Владимирская'                 
    elif metro_place_code == 'spb_08': metro_name = 'ст.м. Волковская'                   
    elif metro_place_code == 'spb_09': metro_name = 'ст.м. Выборгская'                   
    elif metro_place_code == 'spb_10': metro_name = 'ст.м. Горьковская'                  
    elif metro_place_code == 'spb_11': metro_name = 'ст.м. Гостиный двор'                
    elif metro_place_code == 'spb_12': metro_name = 'ст.м. Гражданский проспект'         
    elif metro_place_code == 'spb_13': metro_name = 'ст.м. Девяткино'                    
    elif metro_place_code == 'spb_14': metro_name = 'ст.м. Достоевская'                  
    elif metro_place_code == 'spb_15': metro_name = 'ст.м. Елизаровская'                 
    elif metro_place_code == 'spb_16': metro_name = 'ст.м. Звёздная'                     
    elif metro_place_code == 'spb_17': metro_name = 'ст.м. Звенигородская'               
    elif metro_place_code == 'spb_18': metro_name = 'ст.м. Кировский завод'              
    elif metro_place_code == 'spb_19': metro_name = 'ст.м. Комендантский проспект'       
    elif metro_place_code == 'spb_20': metro_name = 'ст.м. Крестовский остров'           
    elif metro_place_code == 'spb_21': metro_name = 'ст.м. Купчино'                      
    elif metro_place_code == 'spb_22': metro_name = 'ст.м. Ладожская'                    
    elif metro_place_code == 'spb_23': metro_name = 'ст.м. Ленинский проспект'           
    elif metro_place_code == 'spb_24': metro_name = 'ст.м. Лесная'                       
    elif metro_place_code == 'spb_25': metro_name = 'ст.м. Лиговский проспект'           
    elif metro_place_code == 'spb_26': metro_name = 'ст.м. Ломоносовская'                
    elif metro_place_code == 'spb_27': metro_name = 'ст.м. Маяковская'                   
    elif metro_place_code == 'spb_28': metro_name = 'ст.м. Международная'                
    elif metro_place_code == 'spb_29': metro_name = 'ст.м. Московская'                   
    elif metro_place_code == 'spb_30': metro_name = 'ст.м. Московские ворота'            
    elif metro_place_code == 'spb_31': metro_name = 'ст.м. Нарвская'                     
    elif metro_place_code == 'spb_32': metro_name = 'ст.м. Невский проспект'             
    elif metro_place_code == 'spb_33': metro_name = 'ст.м. Новочеркасская'               
    elif metro_place_code == 'spb_34': metro_name = 'ст.м. Обводный канал'               
    elif metro_place_code == 'spb_35': metro_name = 'ст.м. Обухово'                      
    elif metro_place_code == 'spb_36': metro_name = 'ст.м. Озерки'                       
    elif metro_place_code == 'spb_37': metro_name = 'ст.м. Парк Победы'                  
    elif metro_place_code == 'spb_38': metro_name = 'ст.м. Парнас'                       
    elif metro_place_code == 'spb_39': metro_name = 'ст.м. Петроградская'                
    elif metro_place_code == 'spb_40': metro_name = 'ст.м. Пионерская'                   
    elif metro_place_code == 'spb_41': metro_name = 'ст.м. Площадь Александра Невского 1'
    elif metro_place_code == 'spb_42': metro_name = 'ст.м. Площадь Александра Невского 2'
    elif metro_place_code == 'spb_43': metro_name = 'ст.м. Площадь Восстания'            
    elif metro_place_code == 'spb_44': metro_name = 'ст.м. Площадь Ленина'               
    elif metro_place_code == 'spb_45': metro_name = 'ст.м. Площадь Мужества'             
    elif metro_place_code == 'spb_46': metro_name = 'ст.м. Политехническая'              
    elif metro_place_code == 'spb_47': metro_name = 'ст.м. Приморская'                   
    elif metro_place_code == 'spb_48': metro_name = 'ст.м. Пролетарская'                 
    elif metro_place_code == 'spb_49': metro_name = 'ст.м. Проспект Большевиков'         
    elif metro_place_code == 'spb_50': metro_name = 'ст.м. Проспект Ветеранов'           
    elif metro_place_code == 'spb_51': metro_name = 'ст.м. Проспект Просвещения'         
    elif metro_place_code == 'spb_52': metro_name = 'ст.м. Пушкинская'                   
    elif metro_place_code == 'spb_53': metro_name = 'ст.м. Рыбацкое'                     
    elif metro_place_code == 'spb_54': metro_name = 'ст.м. Садовая'                      
    elif metro_place_code == 'spb_55': metro_name = 'ст.м. Сенная площадь'               
    elif metro_place_code == 'spb_56': metro_name = 'ст.м. Спасская'                     
    elif metro_place_code == 'spb_57': metro_name = 'ст.м. Спортивная'                   
    elif metro_place_code == 'spb_58': metro_name = 'ст.м. Старая Деревня'               
    elif metro_place_code == 'spb_59': metro_name = 'ст.м. Технологический институт 1'   
    elif metro_place_code == 'spb_60': metro_name = 'ст.м. Технологический институт 2'   
    elif metro_place_code == 'spb_61': metro_name = 'ст.м. Удельная'                     
    elif metro_place_code == 'spb_62': metro_name = 'ст.м. Улица Дыбенко'                
    elif metro_place_code == 'spb_63': metro_name = 'ст.м. Фрунзенская'                  
    elif metro_place_code == 'spb_64': metro_name = 'ст.м. Чёрная речка'                 
    elif metro_place_code == 'spb_65': metro_name = 'ст.м. Чернышевская'                 
    elif metro_place_code == 'spb_66': metro_name = 'ст.м. Чкаловская'                   
    elif metro_place_code == 'spb_67': metro_name = 'ст.м. Электросила'
    print (city_place)
    print (metro_name)
    if city_place != "":
        address= find_address(city_place)
    elif metro_name != "":
        address= find_address_by_metro(metro_name.replace('ст.м. ','')) 
    if address == "":
        address = "В данном районе|станции метро нет пункта сбора. Просьба выборать ближайший район/станцию метро города к вашему"
    bot.sendMessage(chat_id=query.message.chat.id, text=address)

start_handler = CommandHandler('start', start)
recycle_handler = CommandHandler('recycle', recycle_cmd, pass_args=True)
where_handler = CommandHandler('where', where_cmd, pass_args=True)
types_handler = CommandHandler('types', types_cmd, pass_args=True)
help_handler = CommandHandler('help', help_cmd)
metro_handler = CommandHandler('metro', metro_cmd, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(recycle_handler)
dispatcher.add_handler(where_handler)
dispatcher.add_handler(types_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(metro_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
    #updater.start_webhook(listen='127.0.0.1', port=5003, url_path=telegram_token)
    #updater.bot.setWebhook(webhook_url='https://95.85.37.72/'+telegram_token,
    #                       certificate=open('/home/deploy/it-volunteer-bot/cert.pem', 'rb'))
    print('hi')
