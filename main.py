import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import requests
import json
from pprint import pprint
import os
from TextManagement.TxtManager import TxtManager
from ConfrontiTraRegioni.confronti import ConfrontoManager
from LogicMap.MapManagementClass import MapManagementClass
from LogicMap.DocManager import DocManager
from GraphManagement.GraphManager import GraphManager
from GraphManagement.AdvancedGraphManager import AdvancedGraphManager

import matplotlib.pyplot as plt

listOfRegions=['Abruzzo','Basilicata','Calabria','Campania','Emilia_Romagna','Friuli_Venezia_Giulia','Friuli_Venezia_Giulia','Lazio','Liguria',
               'Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino_Alto_Adige','Umbria','Valle_D_Aosta','Veneto']
listOfGraphs=["Ricoverati con sintomi","Terapia intensiva",'Totale ospedalizzati', "Isolamento domiciliare", 'Totale attualmente positivi', "Nuovi attualmente positivi",'Dimessi guariti',
              'Deceduti','Totale casi','Tamponi']
listOfStats = ["Percentuale guarigioni","Percentuale dimessi","Percentuale ricoverati","Percentuale decessi"]
listConfronts = ["tamponi","totale_attualmente_positivi", "deceduti", "nuovi_attualmente_positivi", "totale_ospedalizzati","totale_casi"]
mainKeyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = 'Testuali',callback_data = 'textualData')],
            [InlineKeyboardButton(text = 'Grafiche',callback_data = 'Images')],
            [InlineKeyboardButton(text = 'Infografiche',callback_data = 'Infografiche')],
            [InlineKeyboardButton(text = 'Andamenti',callback_data = 'Andamenti')],
            [InlineKeyboardButton(text = 'Confronto regioni',callback_data = 'Confronto')],
            [InlineKeyboardButton(text = 'Statistiche',callback_data = 'Statistiche')]])

"""data = DocManager().update()
mappe = MapManagementClass(data)
grafi = GraphManager()
confronto = ConfrontoManager()
rete = AdvancedGraphManager()"""
info = TxtManager()

def getDataFromJson(url):
    data = requests.get(url)
    jsonData = data.json()
    return jsonData

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        articles = [InlineQueryResultArticle(
                        id='txtITA',
                        title="Ultimi dati, testo",
                        input_message_content=InputTextMessageContent(
                            message_text="Informazioni CoronaVirus in Italia aggiornate:\n\n"+info.textualInfoItaly(jsonData),
                        ),
                   )]

        return articles

    answerer.answer(msg, compute)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)
    if content_type == 'text':    
        bot.sendMessage(chat_id, "Ultime Informazioni:", reply_markup = mainKeyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor = 'callback_query')
    print('Callback query:',query_id, from_id, query_data)
    if query_data == "textualData":
        msg_str = info.textualInfoItaly(jsonData)
        bot.sendMessage(from_id, msg_str)
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup = mainKeyboard)


if __name__ == "__main__":
    
    TOKEN = "1097804080:AAHCv4KgmI6fz1nZcRPzNoR0qO1yZEuiQ_8"
    print(TOKEN)
    
    
    urlNationalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    urlRegionalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    jsonData = getDataFromJson(urlNationalData)
    jsonRegionalData = getDataFromJson(urlRegionalData)
    bot = telepot.Bot(TOKEN)
    bot.urlNationalData = urlNationalData
    answerer = telepot.helper.Answerer(bot)

    MessageLoop(bot, {'chat':on_chat_message, 'callback_query':on_callback_query,
                        'inline_query': on_inline_query,
                        'chosen_inline_result': on_chosen_inline_result}).run_forever()

    print('Listening...')
