import logging

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

import time

smapper = {
'001': ['plastic bag'],
'002': ['plastic bin'],
'003': ['CD DVD'],
'004': ['magazine'],
'005': ['toilet paper'],
'006': ['egg package'],
'007': ['paper package'],
'008': ['plastic container']
}

def mapping(rep):
    for k, v in smapper.items():
        if rep in v:
            return k
    return '009'

class Flags:
    model_dir = "."

FLAGS = Flags()
from classify import run_inference_on_image
from conf import TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def search_info_by_id(classid == None):
    if classid == None: return ("","","","")
    with codecs.open('recycle_db.csv', encoding='utf-8') as csvfile:
        for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
            if classid == row[0]: result = row
    return (row[1],row[2],row[3],row[4])
    pass

def handle(bot, update):
    # import ipdb; ipdb.set_trace()
    f = bot.getFile(update.message.photo[-1].file_id)
    fn = "files/{}.jpg".format(time.time())
    f.download(fn) 
    obj_info = search_info_by_id(mapping(run_inference_on_image(fn)))
    if obj_info[2]==1: obj_info[2] = "принием"
    else: obj_info[2] = "не принимаем"
    bot.sendMessage(chat_id=update.message.chat_id, text='Это {} и это мы {}'.format(obj_info[0],obj_info[1]))

handler = MessageHandler(Filters.photo, handle)
dispatcher.add_handler(handler)

def main():
    updater.start_polling()
    # updater.idle()


if __name__ == "__main__":
    main()
