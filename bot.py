"""
SOURCE : https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
AIDE URL SOURCE : https://topsitestreaming.info/

install pip :
pip install python-telegram-bot

TODO: 

-Dire le nb de site OK dans la liste 
-Faire un filtre du user_input pour enelever les mots de liaisons et les accents
-Changer le msg d'erreur par un GIF de mec qui cherche (tu vois de quoi je parle chakal)

"""
import os
import requests
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.filters import Filters
from bs4 import BeautifulSoup
import requests
import re   

#Telegram token
updater = Updater("5909021258:AAHdZXGkJQjOlSE3T9g2oyvZXIDvEW78GhU",use_context=True)
token = str("5909021258:AAHdZXGkJQjOlSE3T9g2oyvZXIDvEW78GhU")


#def des fonctions du bot

def qr():#QR CODE Function
    import qrcode
    global qr_img
    qr_img = qrcode.make(link)
    qr_img.save('TEMP.png')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Ouaiiiiis !!! des nouveaux amis !")

global qrcode
def qrcode(update: Update, context: CallbackContext):
    global get_qrcode
    global link
    link = update.message.text.replace('/qrcode', '')
    def get_qrcode():
            global chat_id
            chat_id = str(update.effective_user.id)
            qr()
            path = 'TEMP.png'
            file = {'photo': open(path, 'rb')}

            print(f'le lien est : {link}') 
            message = ('https://api.telegram.org/bot'+ token + '/sendPhoto?chat_id=' + chat_id)
            requests.post(message, files = file)
            os.remove('TEMP.png')
    get_qrcode()



def moviesearch(update: Update, context: CallbackContext):#STREAMING function
    URL = ["https://www.megastream.lol/index.php", "https://www.cpasmieux.run/index.php", "https://wwvv.cpasmieux.one/", "https://www.cpasmieux.win/", "https://cpasmieux.ink/", "https://wwvv.cpasmieux.one/", "https://www.33seriestreaming.lol/", "https://www.hds-streaming.cam/", "https://www.french-stream.buzz/", "https://streamingseries.lol/", "https://www.juststream.lol/","https://www.lebonstream.vin/"  ]
    film = update.message.text.replace('/search', '')#User input - /search
    update.message.reply_text(f"Attend je vais chercher ça ! 🔎")
    search_lower = film.lower()
    search = search_lower.replace(' ', '+')#POST Payload convert
    data = {"do":"search", "subaction":"search", "story": {search}}

    result = search_lower.split()#fait une liste avec le nom du film si plusieurs mots pour chercher dans les URL

    for i in URL:
        error_url = i.replace('https://', '')
        page = requests.post(i, data=data)
        soup = BeautifulSoup(page.content, 'html.parser').find_all(lambda t: t.name == "a")
        url_list = [a["href"] for a in soup]#https://stackoverflow.com/questions/65168254/how-to-get-href-link-by-text-in-python
        for __ in result:
            links_temp = list(filter(lambda x: re.search(__, x), url_list))
            links = '\n\n'.join(links_temp)#saut de ligne entre chaque éléments

        #print(f'LA PTN DE LIST DURL DE SES MORTS :\n\n\n {links}')
        update.message.reply_text(f"Tiens c'est cadeau ! : \n{links}\n\n Status de la request :{error_url} {page.status_code}")
        #print(f'SITE : {page.url} \n {page}')
        

#reminder app

def main_menu(update,context):
    global reminder_input
    reminder_input = update.message.text.replace('/r', '')#User input - /r

    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())
    global chat_id_remind
    chat_id_remind = str(update.effective_user.id)

#def du clavier
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('5 mins', callback_data='m1')],
              [InlineKeyboardButton('10 mins', callback_data='m2')],
              [InlineKeyboardButton('15 mins', callback_data='m3')],
              [InlineKeyboardButton('30 mins', callback_data='m4')],
              [InlineKeyboardButton('45 mins', callback_data='m5')],
              [InlineKeyboardButton('1H', callback_data='m6')]]
  return InlineKeyboardMarkup(keyboard)

#message du menu
def main_menu_message():
  return 'Dans combien de temps ? :'


def m1(update: Update, context: CallbackContext):
    global wait
    wait = 5
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()

def m2(update: Update, context: CallbackContext):
    global wait
    wait = 10
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()

def m3(update: Update, context: CallbackContext):
    global wait
    wait = 15
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()

def m4(update: Update, context: CallbackContext):
    global wait
    wait = 30
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()

def m5(update: Update, context: CallbackContext):
    global wait
    wait = 45
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()

def m6(update: Update, context: CallbackContext):
    global wait
    wait = 60
    print("TEST 1H")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Ok c\'est fait !')
    remind()


def remind():
    import time
    global text
    text = str(reminder_input)
    print(f'Le message de remind est : {text}')
    local_time = wait * 60
    time.sleep(local_time)
    message = ('https://api.telegram.org/bot'+ token + '/sendMessage?chat_id=' + chat_id_remind + '&text=' + text)
    requests.post(message)
#Fin reminder app



def help(update: Update, context: CallbackContext):
    update.message.reply_text("/link : Permet d'avoir le lien du bot. \n\n/qrcode [Ce que tu veux] : Pour faire un QRCode sur ce que tu veux. \n\n/search [Nom du film / serie] : Pour rechercher un film ou une serie sur des sites pas hyper légaux... mais bon c'est gratuit !\nNOTE : Stp évite de mettre des mots de liaisons de type (et, le, du...) car ca peux te donner des résultats non attendu.\n\n/r [Ce que tu veux qu'il te rapelle]")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Mais qu'est ce qu'elle raconte la pute à crack ?!\n Va voir dans /help !")


def telegram_link(update: Update, context: CallbackContext):
    update.message.reply_text("t.me/Mehliug_bot")


#Trigger des fonctions

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(CommandHandler('link', telegram_link))

updater.dispatcher.add_handler(CommandHandler('search', moviesearch))

updater.dispatcher.add_handler(CommandHandler('qrcode', qrcode))

updater.dispatcher.add_handler(CommandHandler('r', main_menu))
updater.dispatcher.add_handler(CallbackQueryHandler(m1, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(m2, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(m3, pattern='m3'))
updater.dispatcher.add_handler(CallbackQueryHandler(m4, pattern='m4'))
updater.dispatcher.add_handler(CallbackQueryHandler(m5, pattern='m5'))
updater.dispatcher.add_handler(CallbackQueryHandler(m6, pattern='m6'))

updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))   


#Run the bot
updater.start_polling()
