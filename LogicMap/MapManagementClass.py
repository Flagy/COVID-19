import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from DocManager import DocManager



class MapManagementClass():
    def __init__(self):
        print("Launch Map Manager")
        self.data=[]
        self.getUrl=DocManager()
        
        

    
    def purifyData(self,regione):
        
        den_corretta=""
        if regione=="Valle_D_Aosta":
            den_corretta="Valle d'Aosta"
        elif regione=="Emilia_Romagna":
            den_corretta="Emilia Romagna"
        elif regione=="Trentino_Alto_Adige":
            den_corretta="Trentino Alto Adige"
        elif regione=="Friuli_Venezia_Giulia":
            den_corretta="Friuli Venezia Giulia"
        else:
            den_corretta=regione
        self.data = pd.read_csv(self.getUrl.update()) 
        self.data = self.data[self.data["lat"] > 0 ]
        self.data=self.data[self.data["casi_totali"]>0]
        self.data=self.data[self.data["denominazione_regione"]==den_corretta]
       
        
        
    def getImage(self,param):
        self.purifyData(param)
        gdf = geopandas.GeoDataFrame(self.data, geometry=geopandas.points_from_xy(self.data.long, self.data.lat))
        legenda={}
        i=0
        for provincia in self.data["denominazione_provincia"]:
            legenda[i]=provincia
            i=i+1
        world = geopandas.read_file("LogicMap/geomappeRegioni/"+param+".geojson")
        ax = world.plot(color='white', edgecolor='black', figsize=(8, 4))
        
        ax.set_axis_off()
        list_of_province=[]
        k=0
        for i in self.data['casi_totali']:
            patch=mpatches.Patch( edgecolor="w", facecolor="w", color="w",label=str(i)+ " : "+legenda[k])
            k=k+1
            list_of_province.append(patch)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handles=list_of_province)
        lista_indici= pd.DataFrame(list(legenda.keys()))
        for x, y, label,num_casi in zip(self.data["long"],self.data["lat"] ,lista_indici[0],self.data['casi_totali'].apply(str)):
            ax.annotate(num_casi, xy=(x, y), xytext=(-10, 0), textcoords="offset points",weight='bold',fontsize=10)
        gdf.plot(ax=ax, color='#f97d77', markersize=self.data['casi_totali'])
        plt.savefig('LogicMap/temp/temp_1.png', dpi=199)
        return('./LogicMap/temp/temp_1.png')
