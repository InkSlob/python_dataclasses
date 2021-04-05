import requests
import json
from dataclasses import dataclass, field
import datetime
import pandas as pd

@dataclass
class EarthquakeClassEvent:
    mag: float
    place: str
    time: str 
    updated: int
    tz: str
    url: str
    detail: str
    felt: int
    cdi: float
    mmi: float
    alert: str
    status: str
    tsunami: int
    sig: int
    net: str
    code: str
    ids: str
    sources: str
    types: str
    nst: str
    dmin: float
    rms: float
    gap: int
    magType: str
    ttype: str
    title: str
    readable_time: datetime = field(init = False)


    def __post_init__(self):
        """Converts the raw timestamp input into a readable time format and saves to readable_time variable"""
        ts = int(self.time)/1000
        self.readable_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  

def get_api_earthquake_data(url, start_date, end_date):
    paramss = {"format": "geojson", "starttime": start_date, "endtime": end_date, "alertlevel": "yellow"}
    data = requests.get(url, params = paramss)
    data = json.loads(data.text)
    return data

def parse_data_to_dataclass(data):
    # declare list to store dataclass
    earthquake_list = []
    for j in (data['features']):
        i = j['properties']
        earthquake_list.append(EarthquakeClassEvent(i['mag'], i['place'], i['time'], i['updated'], i['tz'], i['url'], i['detail'], i['felt'], i['cdi'], i['mmi'], i['alert'], i['status'],
            i['tsunami'], i['sig'], i['net'], i['code'], i['ids'], i['sources'], i['types'], i['nst'], i['dmin'], i['rms'], i['gap'], i['magType'], i['type'], i['title']))
    return earthquake_list 

def main():
    # url to the USGS earthquake API
    # USGS counts your requests - you will get timed out if you hit it too often
    url = r"https://earthquake.usgs.`gov/fdsnws/event/1/query?"
    # start date for the api call
    start_date = "2019-01-01"
    # end date for the api call
    end_date = "2021-01-31"
    # use python requests to call url and get the earthquake data
    data = get_api_earthquake_data(url, start_date, end_date)
    # call function to load data into the dataclass
    earthquakes = parse_data_to_dataclass(data) 

    # print and demonstrate dataclass
    print('-------------')
    print(earthquakes[5])
    print('-------------')
    # load dataclass to the pandas dataframe
    df = pd.DataFrame(earthquakes)
    print(df.head(5))
    print('-------------')


if __name__ == "__main__":
    main()
