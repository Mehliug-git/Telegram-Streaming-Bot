from flask import Flask, render_template
from flask_scss import Scss
import subprocess
import time


app = Flask(__name__)
scss = Scss(app)#Initialisation du SCSS

bot_process = subprocess.Popen(['python3' , 'bot.py'])



@app.route("/")
def page_web_de_mort():
    bot_process
    return render_template('index.php'), 200
    

app.run()
  
  
  
"""

if __name__ == "__main__":
    app.run()

"""