from bot import token
import time
import requests
import os

chat_id = "5987971244"

file = open("text.txt", "r")
text_old = file.read()
file.close()

text = str(text_old)

wait_file = open("wait.txt","r")
wait_old = wait_file.read()
wait_file.close()

wait = int(wait_old)
print(wait)

local_time = wait * 60
time.sleep(local_time)
message = ('https://api.telegram.org/bot'+ token + '/sendMessage?chat_id=' + chat_id + '&text=' + text)
requests.get(message)




os.remove('text.txt')
os.remove('wait.txt')
