"""
SOURCE : https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/
AIDE URL SOURCE : https://topsitestreaming.info/

install pip :
pip install python-telegram-bot
pip install make-response

TODO: 

-Dire le nb de site OK dans la liste 
-Faire un filtre du user_input pour enelever les mots de liaisons et les accents
-Ajouter la recherche de jeux / Logiciel crack

"""
import requests
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.update import Update
from bs4 import BeautifulSoup
import re 
import os
import openai
import subprocess


openai.api_key = os.getenv('OPENAI_TOKEN')
#Telegram token
token = os.getenv('TELEGRAM_TOKEN')
updater = Updater(token,use_context=True)
rapidapi_key = os.getenv('RAPIDAPI_KEY')



def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_user.id)
    with open("chat_id.txt", "r+") as f:
        if chat_id not in f.read():
            f.write(f"{chat_id}\n")
            update.message.reply_text("TI-TIM-TIMMY !!")
        else:
            update.message.reply_text(f"TI-TIM-TIMMY !!\n\n{chat_id}")

"""
def msg_all(update: Update, context: CallbackContext):  
  chat_id_list = open("chat_id.txt", "r+")
  
  for _id in chat_id_list:
    msg = update.message.text.replace('/MsG__AlL', '')
    message = ('https://api.telegram.org/bot'+ token + '/sendMessage?chat_id=' + _id + '&text=' + msg)
    requests.post(message)
"""  
            

#def des fonctions du bot
   

def moviesearch(update: Update, context: CallbackContext):#STREAMING function
#USER INPUT      
        URL = ["https://www.megastream.lol/index.php", "https://www.cpasmieux.run/index.php", "https://wwvv.cpasmieux.one/", "https://www.cpasmieux.win/", "https://wwvv.cpasmieux.one/", "https://www.33seriestreaming.lol/", "https://www.hds-streaming.cam/", "https://www.french-stream.buzz/", "https://www.juststream.lol/","https://www.lebonstream.vin/"  ]
        film_old = update.message.text.replace('/search ', '')#User input - "/search"
        film = film_old.replace(' ', '-')
        update.message.reply_text(f"Timmy ! Timmy... 🔎")
        search_lower = film.lower()
        search = search_lower.replace(' ', '+')#POST Payload convert
        
#LEGAL SEARCH
        API = "https://streaming-availability.p.rapidapi.com/v2/search/title"
        querystring = {"title":search,"country":"fr","type":"all","output_language":"en"}
        headers = {
	        "X-RapidAPI-Key": rapidapi_key,
	        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
        }

      
        request = requests.request("GET", API, headers=headers, params=querystring)
        data_rep = request.json()
        if len(data_rep['result']) > 0:
            movie_title = data_rep['result'][0]['title']
            streaming_info = data_rep['result'][0]['streamingInfo']
            
            urls = re.findall('(http\S+)', str(streaming_info))#ICI FAIRE UNE REGEX QUI PREND PRIME VIDEO NETFLIX ETC
            urls_final = '\n\n'.join(urls)
            update.message.reply_text(f"SITES LEGAUX pour {movie_title} : \n\n{urls_final}")   
  
    
    
#NORMAL SEARCH 
        data = {"do":"search", "subaction":"search", "story": {search}}
        
        for i in URL:
            error_url = i.replace('https://', '')
            page = requests.post(i, data=data)
            soup = BeautifulSoup(page.content, 'html.parser')
            url_list = re.findall('(http\S+)', str(soup))
            print(url_list)
                  
            #pour rechercher le nom du film dans la liste d'url  
            for __ in search.split():
                links_temp = list(filter(lambda x: re.search(__, x), url_list))
                links = '\n\n'.join(links_temp)#saut de ligne entre chaque éléments
                links_final = links.replace('">','')
            update.message.reply_text(f"TIMMY !! : \n{links_final}\n\n Status de la request :{error_url} {page.status_code}")
            

            
 #QR CODE Function                  
def qr():
    import qrcode
    global qr_img
    qr_img = qrcode.make(link)
    qr_img.save('TEMP.png')

global qrcode
def qrcode(update: Update, context: CallbackContext):
    global get_qrcode
    global link
    link = update.message.text.replace('/qr', '')
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
              
            
            

def generate_code(update: Update, context: CallbackContext):
          q = update.message.text.replace('/g', '')
          response = openai.Completion.create(
            model="code-davinci-002",
            prompt=q,
            max_tokens=4000,
            temperature=0.7
          )
          code = response['choices'][0]['text']
          update.message.reply_text(code)
          
          
def gpt(update: Update, context: CallbackContext):
          q = update.message.text
          response = openai.Completion.create(
          model="text-davinci-003",
          prompt=q,
          temperature=0
        )
          rep = response['choices'][0]['text']
          update.message.reply_text(rep)
          
          
def DALLE(update: Update, context: CallbackContext):
  chat_id = str(update.effective_user.id)
  update.message.reply_text("Dall-E dessine... (5mins Max)")
  prompt = update.message.text.replace('/img', '')
  response = openai.Image.create(
  prompt=prompt,
  n=1,
  size="1024x1024"
)
  image_url = response['data'][0]['url']
  update.message.reply_text(image_url)
    
  #./nikto/program/nikto.pl -host {prompt} -Tuning 1 2 3 4 5 7 8 9 0  
def nikto(update: Update, context: CallbackContext):
  #GIF
  chat_id = str(update.effective_user.id)
  msg = "https://i.giphy.com/YQitE4YNQNahy.gif"
  message = ('https://api.telegram.org/bot'+ token + '/sendVideo?chat_id=' + chat_id + '&video=' + msg)
  requests.post(message)
  
  site = update.message.text.replace('/nikto', '')
  prompt = str(site)
  update.message.reply_text("Scan en cours... (15mins Max)")
  p = subprocess.Popen(f'./nikto/program/nikto.pl -host {prompt} -Tuning 1 2 3 4 5 7 8 9 0', stdout=subprocess.PIPE, shell=True)
  output, error = p.communicate()
  
  
  if error:
    update.message.reply_text(f'Erreur : {error.decode()}')
  else:
     # Divise l'output en plusieurs parties
    parts = output.decode().split('\n')
    
    # Envoie chaque partie de l'output au chat
    for part in parts:
      chat_id = str(update.effective_user.id)
      update.message.bot.send_message(
        chat_id = chat_id,
        text=part,
        disable_web_page_preview=True,
        parse_mode='HTML'
      )    
    
   
  
def games(update: Update, context: CallbackContext):#GAMES function
        URL = ["https://crohasit.net/", "https://gogunlocked.com/"]
        jeux = update.message.text.replace('/search', '')#User input - /search
      
        update.message.reply_text(f"Timmy ! Timmy... 🔎")
        update.message.reply_text(f"En cours de dev...")
        search_lower = jeux.lower()
        search = search_lower.replace(' ', '+')#POST Payload convert
        
        data = f"?/s={search}"
        result = search_lower.split()#fait une liste avec le nom du jeux si plusieurs mots pour chercher dans les URL
        
        for i in URL:
            error_url = i.replace('https://', '')
            page = requests.post(i + data)
            soup = BeautifulSoup(page.content, 'html.parser').find_all(lambda t: t.name == "a")
            url_list = [a["href"] for a in soup]#https://stackoverflow.com/questions/65168254/how-to-get-href-link-by-text-in-python
            
            for __ in result:
                links_temp = list(filter(lambda x: re.search(__, x), url_list))
                links = '\n\n'.join(links_temp)#saut de ligne entre chaque éléments
            update.message.reply_text(f"TIMMY !! : \n{links}\n\n Status de la request :{error_url} {page.status_code}")

            
def console(update: Update, context: CallbackContext):
  cmd = update.message.text.replace('/oulah', '')
  prompt = str(cmd)
  p = subprocess.Popen(f'{prompt}', stdout=subprocess.PIPE, shell=True)
  output, error = p.communicate()
  
  if error:
    update.message.reply_text(f'Erreur : {error.decode()}')
  else:
     # Divise l'output en plusieurs parties
    parts = output.decode().split('\n')
    
    # Envoie chaque partie de l'output au chat
    for part in parts:
      chat_id = str(update.effective_user.id)
      update.message.bot.send_message(
        chat_id = chat_id,
        text=part,
        disable_web_page_preview=True,
        parse_mode='HTML'
      )    
  
  

def help(update: Update, context: CallbackContext):
    update.message.reply_text("/link : Permet d'avoir le lien du bot. \n\n/search [Nom du film / serie] : Pour rechercher un film ou une serie sur des sites pas hyper légaux... mais bon c'est gratuit !\n\n/g [Ce que tu veux] Pour parler au chat GPT3 ! (Modèle pour le code)\nNe met pas de /g pour parler avec GPT3 texte !\n\n/qr [Mot ou URL] Permet de convertir en QRCODE tout ce que tu lui donne.\n\n/img [Le prompt que tu veux] Pour faire une image via Dall-E\n\n/crack [Nom du jeux] Pour chercher des jeux cracké")
def unknown(update: Update, context: CallbackContext):
    chat_id = str(update.effective_user.id)
    msg = "https://i.giphy.com/3o7aTskHEUdgCQAXde.gif"
    message = ('https://api.telegram.org/bot'+ token + '/sendVideo?chat_id=' + chat_id + '&video=' + msg)
    requests.post(message)
    update.message.reply_text("Timmy ? \n\n/help !")
                              
                              
def secret_help(update: Update, context: CallbackContext):
    chat_id = str(update.effective_user.id)
    msg = "https://i.giphy.com/B4dt6rXq6nABilHTYM.gif"
    message = ('https://api.telegram.org/bot'+ token + '/sendVideo?chat_id=' + chat_id + '&video=' + msg)
    requests.post(message)
    update.message.reply_text("U2kgdHUgdHJvdXZlIMOnYSBwYXIgaGF6YXJkIEdHICEgc2lub24gdnJhaW1lbnQgZmFpdCBnYWZmZSDDoCB0b3V0IMOnYSBjJ2VzdCBkYW5nZXJldXguCgovbmlrdG8gW1VSTCBzaXRlIGVuIEhUVFBdIFBvdXIgbGFuY2VyIHVuIHNjYW4gYXZlYyBOaWt0byBzdXIgdW4gc2l0ZSBXZWIuCgovb3VsYWggW1NIRUxMIGNvbW1hbmRdIFBvdXIgbGFuY2VyIGRlcyBjb21tYW5kZXMgc2hlbGw=\n\n/MsG__AlL")
  
  
    
def telegram_link(update: Update, context: CallbackContext):
    update.message.reply_text("t.me/Mehliug_bot")



#Trigger des fonctions
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
#updater.dispatcher.add_handler(CommandHandler('MsG__AlL', msg_all))  

updater.dispatcher.add_handler(CommandHandler('H4X0R', secret_help))
updater.dispatcher.add_handler(CommandHandler('nikto', nikto))
updater.dispatcher.add_handler(CommandHandler('oulah', console))

updater.dispatcher.add_handler(CommandHandler('link', telegram_link))
updater.dispatcher.add_handler(CommandHandler('search', moviesearch))
updater.dispatcher.add_handler(CommandHandler('crack', games))

updater.dispatcher.add_handler(CommandHandler('img', DALLE))
updater.dispatcher.add_handler(CommandHandler('g', generate_code))
updater.dispatcher.add_handler(CommandHandler('qr', qrcode))

updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, gpt))   
#Run the bot
updater.start_polling()