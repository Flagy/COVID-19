import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
from pprint import pprint
from cryptography.fernet import Fernet
from LogicMap.MapManagementClass import MapManagementClass

mappe=MapManagementClass()
listOfRegions=['Abruzzo','Basilicata','Calabria','Campania','Emilia_Romagna','Friuli_Venezia_Giulia','Friuli_Venezia_Giulia','Lazio','Liguria',
               'Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino_Alto_Adige','Umbria','Valle_D_Aosta','Veneto']

mainKeyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = 'Testuali',callback_data = 'textualData')],
            [InlineKeyboardButton(text = 'Grafiche',callback_data = 'Images')]])


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
        
        bot.sendMessage(chat_id, "Ultime Informazioni:", reply_markup = mainKeyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor = 'callback_query')
    print('Callback query:',query_id, from_id, query_data)
    if query_data == "textualData":
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        bot.sendMessage(from_id, msg_str)
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup = mainKeyboard)
    elif query_data=="Images":
         keyboard = InlineKeyboardMarkup(inline_keyboard=[
             [InlineKeyboardButton(text = 'Abruzzo',callback_data = 'Abruzzo')],
             [InlineKeyboardButton(text = 'Basilicata',callback_data = 'Basilicata')],
            [InlineKeyboardButton(text = 'Calabria',callback_data = 'Calabria')],
            [InlineKeyboardButton(text = 'Campania',callback_data = 'Campania')],
            [InlineKeyboardButton(text = 'Emilia Romagna',callback_data = 'Emilia_Romagna')],
            [InlineKeyboardButton(text = 'Friuli Venezia Giulia',callback_data = 'Friuli_Venezia_Giulia')],
            [InlineKeyboardButton(text = 'Lazio',callback_data = 'Lazio')],
            [InlineKeyboardButton(text = 'Liguria',callback_data = 'Liguria')],
            [InlineKeyboardButton(text = 'Lombardia',callback_data = 'Lombardia')],
            [InlineKeyboardButton(text = 'Marche',callback_data = 'Marche')],
            [InlineKeyboardButton(text = 'Molise',callback_data = 'Molise')],
            [InlineKeyboardButton(text = 'Piemonte',callback_data = 'Piemonte')],
            [InlineKeyboardButton(text = 'Puglia',callback_data = 'Puglia')],
            [InlineKeyboardButton(text = 'Sardegna',callback_data = 'Sardegna')],
            [InlineKeyboardButton(text = 'Sicilia',callback_data = 'Sicilia')],
            [InlineKeyboardButton(text = 'Toscana',callback_data = 'Toscana')],
            [InlineKeyboardButton(text = 'Trentino Alto Adige',callback_data = 'Trentino_Alto_Adige')],
            [InlineKeyboardButton(text = 'Umbria',callback_data = 'Umbria')],
            [InlineKeyboardButton(text = "Valle D'Aosta",callback_data = 'Valle_D_Aosta')],
            [InlineKeyboardButton(text = 'Veneto',callback_data = 'Veneto')]
            ])
         bot.sendMessage(from_id, "Seleziona la regione:", reply_markup = keyboard)
    elif query_data in listOfRegions:
        path=mappe.getImage(query_data)
        bot.sendPhoto(from_id, open(path,'rb'))
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup = mainKeyboard)
        
        
    else:
        bot.sendMessage(from_id, "Scelta non valida")
        
        
  

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

