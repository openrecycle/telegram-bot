import time
import os
try:
    from classify import run_inference_on_image
except:
    None
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from interface import districts_button_list, types_button_list, metro_button_list
from sasha2vec import mapping
import codecs
import csv

def build_menu(buttons: list, n_cols: int, header_buttons: list = None, footer_buttons: list = None):
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


def search_info_by_id(classid = None):
    if classid == None: return ("","","","")
    with codecs.open('recycle_db.csv', encoding='utf-8') as csvfile:
        for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
            if classid == row[0]:
                return (row[1], row[2], row[3], row[4])

def find_address(district=None):
    result = ""
    if district!=None:
        #with open('D:\\Projects\\Py-Telegram-Bot\\districts.csv') as csvfile:
        with codecs.open('districts.csv', encoding='utf-8') as csvfile:
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
        with codecs.open('districts.csv', encoding='utf-8') as csvfile:
             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
             for row in reader:
                 if result != "":
                     result += "\n"
                 if metro_name.lower() == row[1].lower().encode('utf-8') or metro_name.lower() == row[1].lower()[:len(metro_name)] or metro_name.lower() in row[1].lower():
                     result += row[1]
    return result

def find_types(type=None):
    result = ""
    if type == None:  # Если нет параметра, то выводится список типов (чтобы было, на будущее)
        with codecs.open('recycle_db.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0].isdigit():  # Таким образом отсеиваются те записи, которые не участвуют в демонстрации
                    if result != "":
                        result += "\n"
                    result += row[1]
    else:
        with codecs.open('recycle_db.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0].isdigit():  # Таким образом отсеиваются те записи, которые не участвуют в демонстрации
                    if result != "":
                        result += "\n"
                    if type.lower() in row[4].split(','):
                        if (row[3] == '1'):
                            result += " - Утилизируется\n"
                        else:
                            result += " - НЕ утилизируется\n"
                        # result += row[6] + "\n"
                        result += row[7] + "\n"
                        return result

def recycle_cmd(bot, update, **args):
    try:
        recycle_args = args.get("args")[0]
    except:
        recycle_args = []
    if len(recycle_args) == 0:
        bot.sendMessage(chat_id=update.message.chat.id, text='Допустимые классы отходов пригодные к переработке: \n')
    else:
        print(recycle_args)
        text = 'Вы указали: ' + recycle_args + find_types(recycle_args)
        bot.sendMessage(chat_id=update.message.chat.id, text=text)    #recycle_args.__str__()

def where_cmd(bot, update, **args):
    msgText = 'where!! '
    query = update.callback_query
    where_args = args.get("args")
    buttonsListFlg = False
    address = ""
    if len(where_args) > 0:
        print(where_args[0])
        address = find_address(where_args[0])
        if address != "":
            msgText = msgText + ' ' + address;
        else:
            buttonsListFlg = True
    else:
        buttonsListFlg = True
    if buttonsListFlg:
        reply_markup = InlineKeyboardMarkup(districts_button_list)
        bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup,
                        text='Выберите пожалуйста район города:')
    else:
        bot.sendMessage(chat_id=update.message.chat.id, text=msgText)

def types_cmd(bot, update, **args):
    reply_markup = InlineKeyboardMarkup(types_button_list)
    text = 'Перед вами список известных классов вторсырья.\n' \
           'Вы можете выбрать любой из них для получения дополнительной информации:'
    bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, text=text)
    # bot.sendMessage(chat_id=update.message.chat.id, text=u'Допустимые классы отходов пригодные к переработке: \n' + find_types())

def help_cmd(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Привет!\n' \
                                                         'Доступные команды:\n' \
                                                         '/recycle или /recycle <наименование> - введите ключевое слово, к примеру "пластиковая бутылка" и я помогу определить можно ее утилизировать или нет\n' \
                                                         '/where или /where <район города> - подскажу, где пункт сбора в вашем районе\n' \
                                                         '/types - подскажу какие отходы бывают\n' \
                                                         '/metro или /metro <станция метро> - подскажу, где пункт сбора отностельно метро')

def metro_cmd(bot, update, **args):
    bot.sendMessage(chat_id=update.message.chat.id, text='Метро:', reply_markup=metro_reply_markup)



spb_adm=u'адмиралтейский'
spb_vas=u'василеостровский'
spb_vyb=u'выборгский'
spb_kln=u'калининский'
spb_kir=u'кировский'
spb_krg=u'красногвардейский'
spb_krs=u'красносельский'
spb_krd=u'кронштадтский'
spb_msk=u'московский'
spb_nev=u'невский'
spb_prd=u'петроградский'
spb_pdv=u'петродворцовый'
spb_prm=u'приморский'
spb_frz=u'фрунзенский'
spb_cnt=u'центральный'




def button(bot, update):
    query = update.callback_query
    city_place_code = query.data
    metro_place_code = query.data
    types_code = query.data
    keyboard_back = [[InlineKeyboardButton(" «< ", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard_back)
    city_place = ""
    metro_name = ""
    type = ""
    if city_place_code == 'back':
        text = 'Пожалуйста, выберите, район города:'
        reply_markup = InlineKeyboardMarkup(districts_button_list)
        bot.sendMessage(chat_id=query.message.chat.id, text=text, reply_markup=reply_markup,
                        message_id=query.message.message_id)
    elif city_place_code == 'spb_adm':
        city_place = spb_adm
    elif city_place_code == 'spb_vas':
        city_place = spb_vas
    elif city_place_code == 'spb_vyb':
        city_place = spb_vyb
    elif city_place_code == 'spb_kln':
        city_place = spb_kln
    elif city_place_code == 'spb_kir':
        city_place = spb_kir
    elif city_place_code == 'spb_krg':
        city_place = spb_krg
    elif city_place_code == 'spb_krs':
        city_place = spb_krs
    elif city_place_code == 'spb_krd':
        city_place = spb_krd
    elif city_place_code == 'spb_msk':
        city_place = spb_msk
    elif city_place_code == 'spb_nev':
        city_place = spb_nev
    elif city_place_code == 'spb_prd':
        city_place = spb_prd
    elif city_place_code == 'spb_pdv':
        city_place = spb_pdv
    elif city_place_code == 'spb_prm':
        city_place = spb_prm
    elif city_place_code == 'spb_frz':
        city_place = spb_frz
    elif city_place_code == 'spb_cnt':
        city_place = spb_cnt
    elif metro_place_code == 'spb_01':
        metro_name = 'ст.м. Автово'
    elif metro_place_code == 'spb_02':
        metro_name = 'ст.м. Адмиралтейская'
    elif metro_place_code == 'spb_03':
        metro_name = 'ст.м. Академическая'
    elif metro_place_code == 'spb_04':
        metro_name = 'ст.м. Балтийская'
    elif metro_place_code == 'spb_05':
        metro_name = 'ст.м. Бухарестская'
    elif metro_place_code == 'spb_06':
        metro_name = 'ст.м. Василеостровская'
    elif metro_place_code == 'spb_07':
        metro_name = 'ст.м. Владимирская'
    elif metro_place_code == 'spb_08':
        metro_name = 'ст.м. Волковская'
    elif metro_place_code == 'spb_09':
        metro_name = 'ст.м. Выборгская'
    elif metro_place_code == 'spb_10':
        metro_name = 'ст.м. Горьковская'
    elif metro_place_code == 'spb_11':
        metro_name = 'ст.м. Гостиный двор'
    elif metro_place_code == 'spb_12':
        metro_name = 'ст.м. Гражданский проспект'
    elif metro_place_code == 'spb_13':
        metro_name = 'ст.м. Девяткино'
    elif metro_place_code == 'spb_14':
        metro_name = 'ст.м. Достоевская'
    elif metro_place_code == 'spb_15':
        metro_name = 'ст.м. Елизаровская'
    elif metro_place_code == 'spb_16':
        metro_name = 'ст.м. Звёздная'
    elif metro_place_code == 'spb_17':
        metro_name = 'ст.м. Звенигородская'
    elif metro_place_code == 'spb_18':
        metro_name = 'ст.м. Кировский завод'
    elif metro_place_code == 'spb_19':
        metro_name = 'ст.м. Комендантский проспект'
    elif metro_place_code == 'spb_20':
        metro_name = 'ст.м. Крестовский остров'
    elif metro_place_code == 'spb_21':
        metro_name = 'ст.м. Купчино'
    elif metro_place_code == 'spb_22':
        metro_name = 'ст.м. Ладожская'
    elif metro_place_code == 'spb_23':
        metro_name = 'ст.м. Ленинский проспект'
    elif metro_place_code == 'spb_24':
        metro_name = 'ст.м. Лесная'
    elif metro_place_code == 'spb_25':
        metro_name = 'ст.м. Лиговский проспект'
    elif metro_place_code == 'spb_26':
        metro_name = 'ст.м. Ломоносовская'
    elif metro_place_code == 'spb_27':
        metro_name = 'ст.м. Маяковская'
    elif metro_place_code == 'spb_28':
        metro_name = 'ст.м. Международная'
    elif metro_place_code == 'spb_29':
        metro_name = 'ст.м. Московская'
    elif metro_place_code == 'spb_30':
        metro_name = 'ст.м. Московские ворота'
    elif metro_place_code == 'spb_31':
        metro_name = 'ст.м. Нарвская'
    elif metro_place_code == 'spb_32':
        metro_name = 'ст.м. Невский проспект'
    elif metro_place_code == 'spb_33':
        metro_name = 'ст.м. Новочеркасская'
    elif metro_place_code == 'spb_34':
        metro_name = 'ст.м. Обводный канал'
    elif metro_place_code == 'spb_35':
        metro_name = 'ст.м. Обухово'
    elif metro_place_code == 'spb_36':
        metro_name = 'ст.м. Озерки'
    elif metro_place_code == 'spb_37':
        metro_name = 'ст.м. Парк Победы'
    elif metro_place_code == 'spb_38':
        metro_name = 'ст.м. Парнас'
    elif metro_place_code == 'spb_39':
        metro_name = 'ст.м. Петроградская'
    elif metro_place_code == 'spb_40':
        metro_name = 'ст.м. Пионерская'
    elif metro_place_code == 'spb_41':
        metro_name = 'ст.м. Площадь Александра Невского 1'
    elif metro_place_code == 'spb_42':
        metro_name = 'ст.м. Площадь Александра Невского 2'
    elif metro_place_code == 'spb_43':
        metro_name = 'ст.м. Площадь Восстания'
    elif metro_place_code == 'spb_44':
        metro_name = 'ст.м. Площадь Ленина'
    elif metro_place_code == 'spb_45':
        metro_name = 'ст.м. Площадь Мужества'
    elif metro_place_code == 'spb_46':
        metro_name = 'ст.м. Политехническая'
    elif metro_place_code == 'spb_47':
        metro_name = 'ст.м. Приморская'
    elif metro_place_code == 'spb_48':
        metro_name = 'ст.м. Пролетарская'
    elif metro_place_code == 'spb_49':
        metro_name = 'ст.м. Проспект Большевиков'
    elif metro_place_code == 'spb_50':
        metro_name = 'ст.м. Проспект Ветеранов'
    elif metro_place_code == 'spb_51':
        metro_name = 'ст.м. Проспект Просвещения'
    elif metro_place_code == 'spb_52':
        metro_name = 'ст.м. Пушкинская'
    elif metro_place_code == 'spb_53':
        metro_name = 'ст.м. Рыбацкое'
    elif metro_place_code == 'spb_54':
        metro_name = 'ст.м. Садовая'
    elif metro_place_code == 'spb_55':
        metro_name = 'ст.м. Сенная площадь'
    elif metro_place_code == 'spb_56':
        metro_name = 'ст.м. Спасская'
    elif metro_place_code == 'spb_57':
        metro_name = 'ст.м. Спортивная'
    elif metro_place_code == 'spb_58':
        metro_name = 'ст.м. Старая Деревня'
    elif metro_place_code == 'spb_59':
        metro_name = 'ст.м. Технологический институт 1'
    elif metro_place_code == 'spb_60':
        metro_name = 'ст.м. Технологический институт 2'
    elif metro_place_code == 'spb_61':
        metro_name = 'ст.м. Удельная'
    elif metro_place_code == 'spb_62':
        metro_name = 'ст.м. Улица Дыбенко'
    elif metro_place_code == 'spb_63':
        metro_name = 'ст.м. Фрунзенская'
    elif metro_place_code == 'spb_64':
        metro_name = 'ст.м. Чёрная речка'
    elif metro_place_code == 'spb_65':
        metro_name = 'ст.м. Чернышевская'
    elif metro_place_code == 'spb_66':
        metro_name = 'ст.м. Чкаловская'
    elif metro_place_code == 'spb_67':
        metro_name = 'ст.м. Электросила'
    elif types_code == 'type_1':
        type = 'Пластиковый пакет'
    elif types_code == 'type_2':
        type = 'Пластиковое ведерко'
    elif types_code == 'type_3':
        type = 'CD/DVD диски'
    elif types_code == 'type_4':
        type = 'Бумага'
    elif types_code == 'type_5':
        type = 'Втулка'
    elif types_code == 'type_6':
        type = 'Упаковка от яиц'
    elif types_code == 'type_7':
        type = 'Упаковка от масла, маргарина'
    elif types_code == 'type_8':
        type = 'Пластиковый контейнер'
    # print (city_place)
    # print (metro_name)
    # print(type)
    if city_place != "":
        address = find_address(city_place)
    elif metro_name != "":
        address = find_address_by_metro(metro_name.replace('ст.м. ', ''))
    elif type != "":
        address = find_types(type)
    if address == "":
        address = "В данном районе|станции метро нет пункта сбора. Просьба выборать ближайший район/станцию метро города к вашему"
    bot.sendMessage(chat_id=query.message.chat.id, text=address)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text='Привет! Я помогу Вам правильно рассортировать Ваши отходы.\n' \
                                                         'Доступные команды:\n' \
                                                         '/start - начало работы со мой\n' \
                                                         '/help - помощь по командам и как мной пользоваться\n' \
                                                         '/recycle <наименование> - введите ключевое слово, к примеру "пластиковая бутылка" и я помогу определить можно ее утилизировать или нет\n' \
                                                         '/where <район города> - подскажу, где пункт сбора в вашем районе \n' \
                                                         '/metro <станция метро> - подскажу, где пункт сбора отностельно метро')

def image_rec(bot, update):
    # import ipdb; ipdb.set_trace()
    f = bot.getFile(update.message.photo[-1].file_id)
    if not os.path.exists('files'):
        os.makedirs('files')
    fn = "files/{}.jpg".format(time.time())
    f.download(fn)
    try:
        resp = run_inference_on_image(fn)
        obj_info = search_info_by_id(mapping(resp))
    except:
        resp = None
        obj_info = mapping('009')
        None
    print(obj_info)
    if obj_info[2]=='1':
        obj_inf = "принимаем"
    else:
        obj_inf = "не принимаем"
    bot.sendMessage(chat_id=update.message.chat_id, text='Это {} и это мы {}'.format(obj_info[0],obj_inf))
    if resp != None:
        bot.sendMessage(chat_id=update.message.chat_id, text=resp)
