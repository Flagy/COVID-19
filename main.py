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
from ConfrontiTraRegioni.confronti import ConfrontoManager
from TextManagement.TxtManager import TxtManager
from LogicMap.MapManagementClass import MapManagementClass
from LogicMap.DocManager import DocManager
from GraphManagement.GraphManager import GraphManager
from GraphManagement.AdvancedGraphManager import AdvancedGraphManager
import json
import codecs
import matplotlib.pyplot as plt

listOfRegions=['Abruzzo','Basilicata','Calabria','Campania','Emilia_Romagna','Friuli_Venezia_Giulia','Lazio','Liguria',
               'Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino_Alto_Adige','Umbria','Valle_D_Aosta','Veneto']
listOfRegions2=['Abruzzo','Basilicata','Calabria','Campania','Emilia Romagna','Friuli Venezia Giulia','Lazio','Liguria',
               'Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino Alto Adige','Umbria',"Valle d'Aosta",'Veneto']
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

data = DocManager().update()
mappe = MapManagementClass(data)
grafi = GraphManager()
confronto = ConfrontoManager()
rete = AdvancedGraphManager()
info = TxtManager()

def getDataFromJson(url):
    data = requests.get(url)
    decoded_data = json.loads(codecs.decode(data.text.encode(), 'utf-8-sig'))
    return decoded_data


def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)
        
        articles = []
        articles.append(InlineQueryResultArticle(id="idItaly", title="ITALIA",
                        input_message_content=InputTextMessageContent(
                            message_text="Informazioni CoronaVirus in ITALIA aggiornate:\n\n" + info.textualInfoItaly(jsonData))))
        for el in listOfRegions2:
            articles.append(InlineQueryResultArticle(id="id"+el, title=el,
                        input_message_content=InputTextMessageContent(
                            message_text="Informazioni CoronaVirus in "+el+" aggiornate:\n\n" + info.textualInfoRegion(getDataFromJson(urlRegionalData), el))))
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
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        bot.sendMessage(from_id, msg_str)
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup = mainKeyboard)

    elif query_data=="Infografiche":
        paths=rete.getPath()
        for path in paths:
            bot.sendPhoto(from_id, open(path, 'rb'))
        bot.sendMessage(from_id, "Ultime Informazioni:", reply_markup=mainKeyboard)
             
    elif query_data=="Confronto":
        confrontoKeyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = 'Tamponi',callback_data = 'tamponi')],
            [InlineKeyboardButton(text = 'Positivi totali',callback_data = 'totale_attualmente_positivi')],
            [InlineKeyboardButton(text = 'Decessi',callback_data = 'deceduti')],
            [InlineKeyboardButton(text = 'Nuovi positivi',callback_data = 'nuovi_attualmente_positivi')],
            [InlineKeyboardButton(text = 'Ospedalizzati',callback_data = 'totale_ospedalizzati')],
            [InlineKeyboardButton(text = 'Totale casi',callback_data = 'totale_casi')]])
        bot.sendMessage(from_id, text="Cosa vuoi visualizzare?", reply_markup = confrontoKeyboard)

    elif query_data in listConfronts:
        bot.sendPhoto(from_id, open(confronto.getBarplot1param(query_data), 'rb'))
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
            [InlineKeyboardButton(text='Dimessi guariti', callback_data='Dimessi guariti')],
            [InlineKeyboardButton(text='Deceduti', callback_data="Deceduti")],
            [InlineKeyboardButton(text="Totale casi", callback_data="Totale casi")],
            [InlineKeyboardButton(text='Tamponi', callback_data='Tamponi')]
        ])
        bot.sendMessage(from_id, "Quale grafico vuoi visualizzare:", reply_markup=keyboardGraph)
    
    elif query_data == "Statistiche":
        pguar = "Percentuale guarigioni: " + str("{0:.2f}".format(jsonData[-1]["dimessi_guariti"]/jsonData[-1]["totale_casi"]*100)) + "%\n"
        pint = "Percentuale terapia intensiva: " + str("{0:.2f}".format(jsonData[-1]["terapia_intensiva"]/jsonData[-1]["totale_casi"]*100)) + "%\n"
        pric = "Percentuale ricoverati: " + str("{0:.2f}".format(jsonData[-1]["ricoverati_con_sintomi"]/jsonData[-1]["totale_casi"]*100)) + "%\n"
        pdec = "Percentuale decessi: " + str("{0:.2f}".format(jsonData[-1]["deceduti"]/jsonData[-1]["totale_casi"]*100)) + "%\n"
        bot.sendMessage(from_id, pguar + pint + pric + pdec, reply_markup=mainKeyboard)

    elif query_data in listOfGraphs:
        path = grafi.printData(query_data)
        if path != "Not Valid Param":
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
