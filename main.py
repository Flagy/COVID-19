import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
from pprint import pprint
import os
from LogicMap.MapManagementClass import MapManagementClass
from LogicMap.DocManager import DocManager
from GraphManagement.GraphManager import GraphManager


listOfRegions=['Abruzzo','Basilicata','Calabria','Campania','Emilia_Romagna','Friuli_Venezia_Giulia','Friuli_Venezia_Giulia','Lazio','Liguria',
               'Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino_Alto_Adige','Umbria','Valle_D_Aosta','Veneto']
listOfGraphs=["Ricoverati con sintomi","Terapia intensiva",'Totale ospedalizzati', "Isolamento domiciliare", 'Totale attualmente positivi', "Nuovi attualmente positivi",'Dismessi guariti',
              'Deceduti','Totale casi','Tamponi']
mainKeyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = 'Testuali',callback_data = 'textualData')],
            [InlineKeyboardButton(text = 'Grafiche',callback_data = 'Images')],
[InlineKeyboardButton(text = 'Andamenti',callback_data = 'Andamenti')],])
data=DocManager().update()
mappe=MapManagementClass(data)
grafi=GraphManager()

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
    elif query_data=="Andamenti":
        keyboardGraph = InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="Ricoverati con sintomi", callback_data="Ricoverati con sintomi")],
            [InlineKeyboardButton(text="Terapia intensiva", callback_data="Terapia intensiva")],
            [InlineKeyboardButton(text='Totale ospedalizzati', callback_data='Totale ospedalizzati')],
            [InlineKeyboardButton(text='Isolamento domiciliare', callback_data='Isolamento domiciliare')],
            [InlineKeyboardButton(text='Totale attualmente positivi', callback_data='Totale attualmente positivi')],
            [InlineKeyboardButton(text='Nuovi attualmente positivi', callback_data='Nuovi attualmente positivi')],
            [InlineKeyboardButton(text='Dismessi guariti', callback_data='Dismessi guariti')],
            [InlineKeyboardButton(text='Deceduti', callback_data="Deceduti")],
            [InlineKeyboardButton(text="Totale casi", callback_data="Totale casi")],
            [InlineKeyboardButton(text='Tamponi', callback_data='Tamponi')]
        ])
        bot.sendMessage(from_id, "Quale grafico vuoi visualizzare:", reply_markup=keyboardGraph)
    elif query_data in listOfGraphs:
        path=grafi.printData(query_data)
        if path!='Not Valid Param':
            bot.sendPhoto(from_id, open(path, 'rb'))
            bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup=mainKeyboard)
        else:
            bot.sendMessage(from_id, "Scelta non valida")
            bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup=mainKeyboard)



    elif query_data in listOfRegions:
        path=mappe.getImage(query_data)
        bot.sendPhoto(from_id, open(path,'rb'))
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup = mainKeyboard)

    else:
        bot.sendMessage(from_id, "Scelta non valida")


if __name__ == "__main__":

    TOKEN =
    #os.environ.get('API_TOKEN', None)

    print(TOKEN)

    urlNationalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    jsonData = getDataFromJson(urlNationalData)
    bot = telepot.Bot(TOKEN)
    bot.urlNationalData = urlNationalData

    MessageLoop(bot, {'chat':on_chat_message,'callback_query':on_callback_query}).run_forever()
    print('Listening...')
