import telegram
import sys
import os

TOKEN = os.getenv('APIKEY')
print(TOKEN)
CHAT_ID = os.getenv('CHAT_ID')
msg = 'test'
def send_message():
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = msg)

send_message()