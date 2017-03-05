import logging

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from sasha2vec import mapping
import time


class Flags:
    model_dir = "."

FLAGS = Flags()
from classify import run_inference_on_image
from config import TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def get_describe_object_by_id(classid==None):
        if classid == None:
            return "Please, make more photo and "
    pass

def handle(bot, update):
    # import ipdb; ipdb.set_trace()
    f = bot.getFile(update.message.photo[-1].file_id)
    fn = "files/{}.jpg".format(time.time())
    f.download(fn)
    guess = run_inference_on_image(fn)
    guessed_class = mapping(guess)
    bot.sendMessage(chat_id=update.message.chat_id, text="I think it is a {}".format(guess))

handler = MessageHandler(Filters.photo, handle)
dispatcher.add_handler(handler)

def main():
    updater.start_polling()
    # updater.idle()


if __name__ == "__main__":
    main()
