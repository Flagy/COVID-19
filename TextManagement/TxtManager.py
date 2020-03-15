import numpy as np

class TxtManager():

    def textualInfoItaly(self, jsonData):
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        return msg_str

    def textualInfoRegion(self, jsonData, region):
        jsonData = jsonData[-21:] # check
        print(region)
        msg_str = ""
        if region == "Trentino Alto Adige":
            region = "P.A. Bolzano"
            for i in range(len(jsonData)):
                if jsonData[i]["denominazione_regione"] == region:
                    idx1 = i
            region = "P.A. Trento"
            for i in range(len(jsonData)):
                if jsonData[i]["denominazione_regione"] == region:
                    idx2 = i
            uniamoIlTrentino = {
                "denominazione_regione" : "Trentino Alto Adige",
                "ricoverati_con_sintomi" : jsonData[idx1]["ricoverati_con_sintomi"] + jsonData[idx2]["ricoverati_con_sintomi"],
                "terapia_intensiva" : jsonData[idx1]["terapia_intensiva"] + jsonData[idx2]["terapia_intensiva"],
                "totale_ospedalizzati": jsonData[idx1]["totale_ospedalizzati"] + jsonData[idx2]["totale_ospedalizzati"],
                "isolamento_domiciliare" : jsonData[idx1]["isolamento_domiciliare"] + jsonData[idx2]["isolamento_domiciliare"],
                "totale_attualmente_positivi": jsonData[idx1]["totale_attualmente_positivi"] + jsonData[idx2]["totale_attualmente_positivi"],
                "nuovi_attualmente_positivi": jsonData[idx1]["nuovi_attualmente_positivi"] + jsonData[idx2]["nuovi_attualmente_positivi"],
                "dimessi_guariti": jsonData[idx1]["dimessi_guariti"] + jsonData[idx2]["dimessi_guariti"],
                "deceduti": jsonData[idx1]["deceduti"] + jsonData[idx2]["deceduti"],
                "totale_casi": jsonData[idx1]["totale_casi"] + jsonData[idx2]["totale_casi"],
                "tamponi": jsonData[idx1]["tamponi"] + jsonData[idx2]["tamponi"]
            }
            jsonData.append(uniamoIlTrentino)
            idx = -1

        else:
            for i in range(len(jsonData)):
                if jsonData[i]["denominazione_regione"] == region:
                    idx = i

        for key, value in jsonData[idx].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        return msg_str