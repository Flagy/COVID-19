from pandas.io.json import json_normalize
import requests
import json
from datetime import datetime,timedelta
url="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json"
r = requests.get(url)
text=json.load(r.text)
df=json_normalize(text)
tod=datetime.today().strftime('%Y-%m-%d')
yest=(datetime.today()- timedelta(days=1)).strftime('%Y%m%d')

df=df[df["data"]==yest+" 18:00:00"]