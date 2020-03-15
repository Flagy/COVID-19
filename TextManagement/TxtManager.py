import numpy as np

class TxtManager():

    def textualInfoItaly(self, jsonData):
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        return msg_str

    def textualInfoRegion(self, jsonData, region):
        jsonData = jsonData[-21:] # check
        for i in range(len(jsonData)):
            if jsonData[i].values() == region:
                idx = i
        
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        return msg_str