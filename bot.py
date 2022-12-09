"""
SOURCE : https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/

install pip :
pip install python-telegram-bot

TODO: 

-Avec une commande /search il trouve des sites de streaming vf dispo 

"""
import os
import requests
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from bs4 import BeautifulSoup
import requests
import re   


updater = Updater("5852426917:AAHN44J2J_0sKRqmqde08qM34SC7n340pjI",use_context=True)#Telegram token
token = str("5852426917:AAHN44J2J_0sKRqmqde08qM34SC7n340pjI")


#def des fontions supp

def qr():#QR CODE Fonction
    import qrcode
    global qr_img
    qr_img = qrcode.make(link)
    qr_img.save('TEMP.png')

#def des fonctions du bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("MESSAGE DE START")

global qrcode
def qrcode(update: Update, context: CallbackContext):
    global get_qrcode
    global link
    link = update.message.text.replace('/qrcode', '')
    def get_qrcode():
            chat_id = str(update.effective_user.id)
            qr()
            path = 'TEMP.png'
            file = {'photo': open(path, 'rb')}

            print(f'le lien est : {link}') 
            message = ('https://api.telegram.org/bot'+ token + '/sendPhoto?chat_id=' + chat_id)
            requests.post(message, files = file)
            os.remove('TEMP.png')
    get_qrcode()



def moviesearch(update: Update, context: CallbackContext):
    URL = ["https://www.megastream.lol/index.php", "https://www.cpasmieux.run/index.php", "https://wiflix.studio/"]
    film = update.message.text.replace('/search', '')#User input - /search
    search_lower = film.lower()


    search = search_lower.replace(' ', '+')#POST Payload convert
    str_search = str(search)
    data = {"do":"search", "subaction":"search", "story": {search}}

    result = search_lower.split()#fait une liste avec le nom du film si plusieurs mots pour chercher dans les URL


    for i in URL:
        page = requests.post(i, data=data)
        soup = BeautifulSoup(page.content, 'html.parser').find_all(lambda t: t.name == "a")
        url_list = [a["href"] for a in soup]#https://stackoverflow.com/questions/65168254/how-to-get-href-link-by-text-in-python
        for __ in result:
            links = list(filter(lambda x: re.search(__, x), url_list))

        print(f'LA PTN DE LIST DURL DE SES MORTS :\n\n\n {links}')
        print(f'SITE : {page.url} \n {page}')





def help(update: Update, context: CallbackContext):
    update.message.reply_text("HELP MESSAGE, bah oui flemme la mtn")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Dsl frerot '%s' n'est pas une commande valide, regarde dans Help" % update.message.text)




#Trigger des fonctions

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(CommandHandler('search', moviesearch))

updater.dispatcher.add_handler(CommandHandler('qrcode', qrcode))


# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))   



#Run the bot
updater.start_polling()
