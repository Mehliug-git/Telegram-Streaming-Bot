from flask import Flask, render_template
import subprocess

app = Flask(__name__)
 
subprocess.Popen(['python3' , 'bot.py'])

@app.route("/")
def hello_world():

  return render_template("index.php", title="Hello")


app.run()
"""

if __name__ == "__main__":
    app.run()

"""