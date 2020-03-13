import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import requests


class ConfrontoManager(object):
    def __init__(self):
        urlRegionalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
        self.data = requests.get(urlRegionalData)
        self.regioniOggi = self.data.json()[-21:] 

    def getBarplot1param(self, param):
        # y-axis in bold
        rc('font', weight='bold')
        
        # Values of each group
        param = 'deceduti'
        bar = []
        pos = []
        names = []

        for region in self.regioniOggi:
            bar.append(region[param])
            pos.append(region["codice_regione"])
            names.append(region["denominazione_regione"])
        

        # Heights of bars1 + bars2
        barWidth = 1
        
        # Create green bars
        plt.bar(pos, bar, color='#557f2d', edgecolor='white', width=barWidth)

        # Custom X axis
        plt.xticks(pos, names, rotation='vertical')
        plt.xlabel("group")
        plt.ylabel(param)
        plt.legend() 
        # Show graphic
        return(plt)

    def getBarplot2param(self, param):
        # y-axis in bold
        rc('font', weight='bold')
        
        # Values of each group
        param1 = 'deceduti'
        param2 = ''
        bar1 = []
        bar2 = []
        pos = []
        names = []

        for region in self.regioniOggi:
            bar1.append(region[param1])
            bar2.append(region[param2])
            pos.append(region["codice_regione"])
            names.append(region["denominazione_regione"])
        
        # Heights of bars1 + bars2
        bars = np.add(bar1, bar2).tolist()
        barWidth = 1
        
        # Create  bars
        plt.bar(pos, bar1, color='#7f6d5f', edgecolor='white', width=barWidth)
        plt.bar(pos, bar2, bottom=bars, color='#557f2d', edgecolor='white', width=barWidth)

        # Custom X axis
        plt.xticks(pos, names, rotation='vertical')
        logo=plt.imread('./logobot.jpeg')
        plt.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
        plt.xlabel("group")
        plt.ylabel(param1 + '/' + param2)
        plt.legend() 
        plt.show()
        # Show graphic
        return(plt)

