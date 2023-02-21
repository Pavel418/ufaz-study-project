import requests
from bs4 import BeautifulSoup
import pandas as pd


keys,vals,prices,priceCurs = list(),list(),list(),list()
locations = ""

def pageDataExtract(id):
    global locations

    url = f'https://bina.az/items/{id}'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')

    trs = soup.find("table", {"class": "parameters"}).findAll('tr')

    for i in trs:
        keys.append((i.findAll("td"))[0].text)
        vals.append((i.findAll("td"))[1].text)


    prices.append(int(soup.find('span', {"class":"price-val"}).text.replace(" ", "")))
    priceCurs.append(soup.find('span', {"class":"price-cur"}).text)


    loclist = soup.find("ul",{"class":"locations"}).findAll("a")

    for i in loclist:locations+=i.text+","


info = dict(zip(keys,vals))
info.update({"price":prices,"price-cur":priceCurs})
info.update({"locations" : locations})

info_df = pd.DataFrame(info)

info_df.to_csv('data.csv', sep=' ', index=False)
