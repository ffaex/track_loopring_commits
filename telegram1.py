import telegram
import sys
import os

TOKEN = os.getenv('APIKEY')
print(TOKEN)
CHAT_ID = os.getenv('CHAT_ID')
<<<<<<< HEAD
msg = 'test'
=======
#msg = 'test'
>>>>>>> 4b5de0085cdcb3c34a9c16f2eadb7056ba09d235
def send_message(msg):
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = msg)

#send_message()
