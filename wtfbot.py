import logging

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

import time


class Flags:
    model_dir = "."

FLAGS = Flags()
from classify import run_inference_on_image
from conf import TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def handle(bot, update):
    # import ipdb; ipdb.set_trace()
    f = bot.getFile(update.message.photo[-1].file_id)
    fn = "files/{}.jpg".format(time.time())
    f.download(fn)
    guess = run_inference_on_image(fn) 
    bot.sendMessage(chat_id=update.message.chat_id, text="I think it is a {}".format(guess))

handler = MessageHandler(Filters.photo, handle)
dispatcher.add_handler(handler)

def main():
    updater.start_polling()
    # updater.idle()


if __name__ == "__main__":
    main()
