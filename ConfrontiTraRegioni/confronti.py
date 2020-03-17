import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
import requests
import codecs
import json


class ConfrontoManager(object):
    def __init__(self):
        urlRegionalData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
        self.data = requests.get(urlRegionalData)
        decoded_data = codecs.decode(self.data.text.encode(), 'utf-8-sig')
        self.regioniOggi = json.loads(decoded_data)[-21:]

    def getBarplot1param(self, param):
        
        # Values of each group
        bar = []
        pos = []
        names = []

        for region in self.regioniOggi:
            bar.append(region[param])
            pos.append(region["codice_regione"])
            names.append(region["denominazione_regione"])
        
        # Name correction
        for i in range(len(names)):
            if names[i] == "Friuli Venezia Giulia":
                names[i] = "Friuli"
            elif names[i] == "Emilia Romagna":
                names[i] = "Emilia"
            elif names[i] == "P.A. Bolzano":
                posblz = i
            elif names[i] == "P.A. Trento":
                postrnt = i
        names[posblz] = "Trentino"
        names[postrnt] = "Trentino"
        bar[posblz] = bar[posblz] + bar[postrnt]
        bar[postrnt] = 0

        # Heights of bars1 + bars2
        barWidth = 1
        
        # Create green bars
        fig, ax = plt.subplots()
        logo = image.imread('./logobot.jpeg')
        ax.yaxis.tick_left()
        ax.tick_params(axis='y', colors='black')
        ax.tick_params(axis='x', colors='black')
        plt.xticks(pos, names, rotation='vertical')
        plt.gcf().subplots_adjust(bottom=0.2)
        ax.bar(pos, bar, color=np.random.rand(3,), edgecolor='white', width=barWidth)

        # Custom X axis
        plt.xlabel("Regioni")
        plt.ylabel(param)
        plt.title(self.regioniOggi[-1]['data'],fontweight='light')
        ax.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
        plt.savefig("./ConfrontiTraRegioni/tmp/img.png", bbox_inches = "tight", dpi=199)
        # Show graphic
        return("./ConfrontiTraRegioni/tmp/img.png")

    def getBarplot2param(self, param1, param2):

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
        fig, ax = plt.subplots()
        logo = image.imread('./logobot.jpeg')
        ax.imshow(logo, aspect='auto', extent=(0.4, 0.6, .5, .7), zorder=-1)
        ax.yaxis.tick_left()
        ax.tick_params(axis='y', colors='black', labelsize=15)
        ax.tick_params(axis='x', colors='black', labelsize=15)
        plt.xticks(pos, names, rotation = 45)
        ax.bar(pos, bar1, color='#7f6d5f', edgecolor='white', width=barWidth)
        ax.bar(pos, bar2, bottom=bars, color='#557f2d', edgecolor='white', width=barWidth)

        # Custom X axis
        
        plt.xlabel("group")
        plt.ylabel(param1 + '/' + param2)
        plt.show()
        plt.savefig("./ConfrontiTraRegioni/tmp/img.png", bbox_inches = "tight", dpi=199)
        # Show graphic
        return(plt)

