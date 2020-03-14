
import requests
import json
from pandas.io.json import json_normalize
import geopandas
import matplotlib.pyplot as plt
import codecs
import sys
from PIL import Image
class AdvancedGraphManager():
    def __init__(self):
        url="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
        r = requests.get(url)
        decoded_data = codecs.decode(r.text.encode(), 'utf-8-sig')
        self.data=json_normalize(json.loads(decoded_data))
        self.paramsFirst={"ricoverati_con_sintomi":"#ebd534","terapia_intensiva":"#28de9e","totale_ospedalizzati":"#177b99","isolamento_domiciliare":"#997917"}
        self.paramsSecond={"totale_attualmente_positivi":"#a86b32","nuovi_attualmente_positivi":"#245e69","dimessi_guariti":"#2bcf0e","deceduti":"#7e877c"}
        self.paramsThird={"totale_casi":"#d0f0c9","tamponi":"#555a70"}
        dataLast=self.data["data"].iloc[-1]
        self.actData=self.data[self.data['data']==dataLast]
        self.createImageData()
    def createImageData(self):
    
        for i in self.paramsFirst:
            world = geopandas.read_file("regioni"+".geojson")
            ax = world.plot(color='white', edgecolor='black', figsize=(12, 8))
            ax.set_axis_off()
            ax.set_title(i, fontsize=15)
            gdf = geopandas.GeoDataFrame(self.actData, geometry=geopandas.points_from_xy(self.actData.long, self.actData.lat))
            gdf.plot(ax=ax, color=self.paramsFirst[i], markersize=self.actData[i])
            plt.savefig('GraphManagement/ImagesToCombine/paramsFirst/'+i+'.png', bbox_inches='tight')
        images = [Image.open('GraphManagement/ImagesToCombine/paramsFirst/'+x+".png") for x in self.paramsFirst ]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]
        new_im.save('GraphManagement/ImagesToCombine/ImageToSend/'+"first"+'.jpg')
        for i in self.paramsSecond:
            world = geopandas.read_file("regioni"+".geojson")
            ax = world.plot(color='white', edgecolor='black', figsize=(12, 8))
            ax.set_axis_off()
            ax.set_title(i, fontsize=15)
            gdf = geopandas.GeoDataFrame(self.actData, geometry=geopandas.points_from_xy(self.actData.long, self.actData.lat))
            gdf.plot(ax=ax, color=self.paramsSecond[i], markersize=self.actData[i])
            plt.savefig('GraphManagement/ImagesToCombine/paramsSecond/'+i+'.png', bbox_inches='tight')
        images = [Image.open('GraphManagement/ImagesToCombine/paramsSecond/'+x+".png") for x in self.paramsSecond ]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]
        new_im.save('GraphManagement/ImagesToCombine/ImageToSend/'+"second"+'.jpg')
        for i in self.paramsThird:
            world = geopandas.read_file("regioni"+".geojson")
            ax = world.plot(color='white', edgecolor='black', figsize=(12, 8))
            ax.set_axis_off()
            ax.set_title(i, fontsize=15)
            gdf = geopandas.GeoDataFrame(self.actData, geometry=geopandas.points_from_xy(self.actData.long, self.actData.lat))
            gdf.plot(ax=ax, color=self.paramsThird[i], markersize=self.actData[i])
            plt.savefig('GraphManagement/ImagesToCombine/paramsThird/'+i+'.png', bbox_inches='tight')
        images = [Image.open('GraphManagement/ImagesToCombine/paramsThird/'+x+".png") for x in self.paramsThird ]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]
        new_im.save('GraphManagement/ImagesToCombine/ImageToSend/'+"third"+'.jpg')
    def getPath(self):
        listOfPath=['GraphManagement/ImagesToCombine/ImageToSend/'+"first"+'.jpg','GraphManagement/ImagesToCombine/ImageToSend/'+"second"+'.jpg','GraphManagement/ImagesToCombine/ImageToSend/'+"third"+'.jpg']
        return (listOfPath)