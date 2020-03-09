# -*- coding: utf-8 -*-

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, ColumnDataSource,LinearColorMapper, ColorBar
from bokeh.palettes import brewer
import json
from bokeh.tile_providers import get_provider, Vendors
import matplotlib.patches as mpatches




def loadData():
    filepath="dati-province/dpc-covid19-ita-province-20200308.csv"
    data = pd.read_csv(filepath,encoding = "ISO-8859-1") 
    return data
dat=loadData()
dat = dat[dat["lat"] > 0 ]
dat=dat[dat["casi_totali"]>0]
dat=dat[dat["denominazione_regione"]=="Lombardia"]
    
    

gdf = geopandas.GeoDataFrame(
    dat, geometry=geopandas.points_from_xy(dat.long, dat.lat))    
legenda={}
i=0
for provincia in dat["denominazione_provincia"]:
    legenda[i]=provincia
    i=i+1
print(legenda)


world = geopandas.read_file("LogicMap/geomappeRegioni/Lombardia.geojson")
#Non deve essere il geopanda points from xy
# We restrict to South America.
ax = world.plot(
    color='white', edgecolor='black')
ax.set_axis_off()
list_of_province=[]
k=0
for i in dat['casi_totali']:
    
    patch=mpatches.Patch( edgecolor="w", facecolor="w", color="w",label=str(i)+ " : "+legenda[k])
    k=k+1
    list_of_province.append(patch)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])


ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handles=list_of_province)

lista_indici= pd.DataFrame(list(legenda.keys()))
for x, y, label,num_casi in zip(dat["long"],dat["lat"] ,lista_indici[0],dat['casi_totali'].apply(str)):
    ax.annotate(num_casi, xy=(x, y), xytext=(-10, 0), textcoords="offset points",weight='bold',fontsize=10)
#"["+str(label)+"]\n"+

# We can now plot our ``GeoDataFrame``.
gdf.plot(ax=ax, color='#f97d77', markersize=dat['casi_totali'])

plt.show()

def load_geoJsonData():
    filepath="LogicMap/geomappeRegioni/Lombardia.geojson"
    with open(filepath) as f:
        data=f.read()
   
    data=json.loads(data)
    data=json.dumps(data)
    return data
data=load_geoJsonData()


print(data)
geosource = GeoJSONDataSource(geojson = data)

#Create figure object.
p = figure()
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,
          line_color = 'black', line_width = 0.4, )#Specify figure layout.

show(p)

def load_data():
    filepath="dati-province/dpc-covid19-ita-province-20200308.csv"
    data = pd.read_csv(filepath,encoding = "ISO-8859-1") 
    return data
dat=load_data()
dat=dat[dat["denominazione_regione"]=="Basilicata"]
dat = dat[dat["lat"] > 0 ]
dat=dat[dat["casi_totali"]>0]

source = ColumnDataSource(
    data=dict(long=dat["long"],lat=dat["lat"])
)
    
p.circle(x="long", y="lat", size=30, fill_color="blue", fill_alpha=0.8, source=source)
show(p)
   
    
 








class MapManagement():
    