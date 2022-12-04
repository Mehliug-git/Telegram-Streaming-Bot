import os
import requests
import sys
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

updater = Updater("5852426917:AAHN44J2J_0sKRqmqde08qM34SC7n340pjI",
                  use_context=True)#Telegram token
token = str("5852426917:AAHN44J2J_0sKRqmqde08qM34SC7n340pjI")


def test(update: Update, context: CallbackContext):
    print(update.message.text)
    data = update.message.text.replace('/qrcode', '')
    print(data)

updater.dispatcher.add_handler(MessageHandler(Filters.text, test))




updater.start_polling()