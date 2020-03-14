class TxtManager():

    def textualInfoItaly(self, jsonData):
        msg_str = ""
        for key, value in jsonData[-1].items():
            msg_str += str(key) + ': ' + str(value) +'\n'
        return msg_str