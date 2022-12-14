import time
from test_bot import reminder_input
from test_bot import time
from test_bot import chat_id
import requests

token = str("5861522005:AAGVYNFK_t7gZGaVz9XRhNpB_oVh1Zfe6Bk")

global text
text = str(reminder_input)
print(text)
local_time = float(time)
print(time)
local_time = local_time * 60
print(local_time)
#time.sleep(local_time)
print(text)

#message = ('https://api.telegram.org/bot'+ token + '/sendPhoto?chat_id=' + chat_id)
#requests.post(message, 'TESTlkjlihugyuftysqdyguihijok')