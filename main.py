import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
from pprint import pprint
from cryptography.fernet import Fernet

def getDataFromJson(url):
    data = requests.get(url)
    jsonData = data.json()
    return jsonData

def json2dict(jsonData):
    pass

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)
    if content_type == 'text':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = 'Testuali',callback_data = 'textualData')],
            [InlineKeyboardButton(text = 'Grafiche',callback_data = 'Images')]])
        bot.sendMessage(chat_id, "ultime informazioni:", reply_markup = keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor = 'callback_query')
    print('Callback query:',query_id, from_id, query_data)
    if query_data == "textualData":
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        bot.sendMessage(from_id, msg_str)
  

if __name__ == "__main__":
    with open("../key.key", "rb") as fd:
        key = fd.read()
        f = Fernet(key)
        TOKEN_ENCR = b"gAAAAABeZsv_JTc8gL4T9WOPQsjZtspep-ZckE-QoU3jr1i7PHAr_hxcYPqmvz8bw3jbCGLiY6F16hNNYQk2o5AN-Cs4IYcoEEm8Yb4VBEOA92a00EzGxXS1miwJJajoDymIeh8TeA2j"
        TOKEN = f.decrypt(TOKEN_ENCR).decode()

    urlNationalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    jsonData = getDataFromJson(urlNationalData)
    bot = telepot.Bot(TOKEN)
    bot.urlNationalData = urlNationalData
    MessageLoop(bot, {'chat':on_chat_message,'callback_query':on_callback_query}).run_as_thread()
    print('Listening...')

    # Keep the program running.
    while 1:
        time.sleep(10)
