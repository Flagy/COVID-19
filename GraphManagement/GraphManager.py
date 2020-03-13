import requests
from pandas.io.json import json_normalize
import json
import matplotlib.pyplot as plt
import pandas as pd

class GraphManager():
    def __init__(self):
        self.url="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
        r = requests.get(self.url)
        self.data=json_normalize(json.loads(r.text))
        self.data["data"] = self.data["data"].replace(to_replace=r'\s(.*)', value='', regex=True)
        self.conversionDict={"Ricoverati con sintomi":"ricoverati_con_sintomi","Terapia intensiva":"terapia_intensiva","Totale ospedalizzati":"totale_ospedalizzati",
                "Isolamento domiciliare":"isolamento_domiciliare" , "Totale attualmente positivi":"totale_attualmente_positivi",
                             "Nuovi attualmente positivi":"nuovi_attualmente_positivi","Dimessi guariti":"dimessi_guariti",
                             "Deceduti":"deceduti","Totale casi":"totale_casi","Tamponi":"tamponi"}
    def printData(self,param):
        try:
            print(self.conversionDict[param])
            ax=self.data.plot(kind='line',x='data',y=self.conversionDict[param],color='red')

            plt.title("Andamento "+param)
            logo=plt.imread('./logobot.jpeg')
            ax.figure.figimage(logo, 3, 3, alpha=0.7, zorder=1)
            plt.xticks(rotation=90)
            plt.savefig('./GraphManagement/tempGraph/temp_1.png', bbox_inches = "tight",dpi=199)
            return('./GraphManagement/tempGraph/temp_1.png')
        except Exception as e:
            print(e)            
            return('Not Valid Param')
