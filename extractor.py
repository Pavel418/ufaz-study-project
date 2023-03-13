import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


keys,vals,area,cixaris, ipoteka,rooms,repairs,prices,priceCurs, latitudes, longitudes = list(),list(),list(),list(), list(),list(),list(),list(),list(),list(),list()
locations = ""

def pageDataExtract(id):
    global locations

    url = f'https://bina.az/items/{id}'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')
    try:
        trs = soup.find("table", {"class": "parameters"}).findAll('tr')
    except Exception as e:
        return
    for i in trs:
        keys.append((i.findAll("td"))[0].text)
        vals.append((i.findAll("td"))[1].text)
        print((i.findAll("td"))[0].text)
    prices.append(int(soup.find('span', {"class":"price-val"}).text.replace(" ", "")))
    priceCurs.append(soup.find('span', {"class":"price-cur"}).text)
    try:
        latitudes.append(soup.find('div', id='agency_map').get('data-lat'))
        longitudes.append(soup.find('div', id='agency_map').get('data-lng'))
    except Exception as e:
        latitudes.append(soup.find('div', id='item_map').get('data-lat'))
        longitudes.append(soup.find('div', id='item_map').get('data-lng'))
        
    loclist = soup.find("ul",{"class":"locations"}).findAll("a")

    for i in loclist:locations+=i.text+","
for i in range(3279157, 3279157 + 1000, 100):
    pageDataExtract(i)
#pageDataExtract(3142195)
info = dict(zip(keys,vals))
info.update({"price":prices,"price-cur":priceCurs})
info.update({"locations" : locations})
info.update({"latitude": latitudes, 'longtitude': longitudes})

info_df = pd.DataFrame(info)

info_df.to_csv('data.csv')
