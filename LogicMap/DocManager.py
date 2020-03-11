import requests
from datetime import datetime,timedelta
from io import StringIO


class DocManager():
    def __init__(self):
        self.url= "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-{YYYYMMDD}.csv"
        
        
    def update(self):
        now = datetime.now()
        if datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S")>datetime.strptime("18:30:00","%H:%M:%S"):
            self.urlBuilder(self.url)
            r = requests.get(self.url)
        else:
            self.urlBuilder(self.url,True)
            r = requests.get(self.url)
        self.reset()
        return(StringIO(r.text))
            
            
            
    def urlBuilder(self,yesterday=False):
       if yesterday:
           self.url.replace("{YYYYMMDD}",(datetime.today()- timedelta(days=1)).strftime('%Y%m%d'))
       else:
           self.url.replace("{YYYYMMDD}",datetime.today().strftime('%Y%m%d'))

    def reset(self):
        self.url= "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-{YYYYMMDD}.csv"
        
       

