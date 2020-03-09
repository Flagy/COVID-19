import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



class MapManagementClass():
    def __init__(self):
        print("Launch Map Manager")
        self.data=self.loadData()
        
        
    def loadData(self):
        filepath="dati-province/dpc-covid19-ita-province-20200308.csv"
        data = pd.read_csv(filepath,encoding = "ISO-8859-1") 
        return data
    
    def purifyData(self,regione):
        self.data = self.data[self.data["lat"] > 0 ]
        self.data=self.data[self.data["casi_totali"]>0]
        self.data=self.data[self.data["denominazione_regione"]==regione]
       
        
        
    def getImage(self,param):
        self.purifyData(param)
        gdf = geopandas.GeoDataFrame(self.data, geometry=geopandas.points_from_xy(self.data.long, self.data.lat))
        legenda={}
        i=0
        for provincia in self.data["denominazione_provincia"]:
            legenda[i]=provincia
            i=i+1
        world = geopandas.read_file("LogicMap/geomappeRegioni/Lombardia.geojson")
        ax = world.plot(color='white', edgecolor='black')
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
        plt.show()
