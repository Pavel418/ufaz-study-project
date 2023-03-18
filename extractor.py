import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp
import cloudscraper

import time

def pageDataExtract(id, session, wait_time):
        url = f'https://bina.az/items/{id}'
        try:
            r = session.get(url)
        except Exception as e:
            print("Connection reset. waiting ", wait_time, " seconds")
            time.sleep(5)
            return pageDataExtract(id, session, wait_time + 5)
        if "Tapılmadı" in r.text:
            print("empty ", id)
            return

        locations = ""
        info = {}
        fields = {"Kateqoriya", "Mərtəbə", "Sahə", "Otaq sayı","Çıxarış","Təmir", "İpoteka"}

        soup = BeautifulSoup(r.text, 'lxml')
        element = soup.find('div', {"class":"search-row__cell search-row__cell--leased"})
        if element is None:
            print("`no search ", id)
            #print(r.text)
            return
        element = element.find('option', {"selected": "selected"})
        if element is None:
            return
        if "Alış" != element.text:
            return
        
        element = soup.find("table", {"class": "parameters"})
        trs = element.find_all('tr')
        for i in trs:
            key = (i.find_all("td"))[0].text
            if key in fields:
                val = i.find_all("td")[1].text
                if key == "Kateqoriya":
                    if val != "Köhnə tikili" and val != "Yeni tikili":
                        return
                info.update({key: val})
                fields.remove(key)
        for i in fields:
            info.update({key: np.NaN})
        city = soup.find('div', {"class":"search-row__cell search-row__cell--city"}).find('option', {"selected": "selected"}).text
        price = int(soup.find('span', {"class":"price-val"}).text.replace(" ", ""))
        priceCur = soup.find('span', {"class":"price-cur"}).text
        date = soup.find('div', {"id": "js-item-show"}).find('div', {"class":"item_show_content"}).find('div',{"class":"item_info"}).find_all('p')[2].text.replace("Yeniləndi: ", "")

        try:
            latitude = soup.find('div', id='agency_map').get('data-lat')
            longitude = soup.find('div', id='agency_map').get('data-lng')
        except Exception as e:
            latitude = soup.find('div', id='item_map').get('data-lat')
            longitude = soup.find('div', id='item_map').get('data-lng')
            
        loclist = soup.find("ul",{"class":"locations"}).find_all("a")

        locations = ','.join([tag.text for tag in loclist])
        
        info.update({"price":price,"price-cur":priceCur,
                    "locations" : locations,"latitude": latitude,
                    "city":city, 'longtitude': longitude, "id": id, "date": date})
        return info

if __name__ == "__main__":
    session = cloudscraper.CloudScraper(debug=True)  
    rows= []
    begin = datetime.datetime.now()
    pageDataExtract(2000000, session, 5)
    end = datetime.datetime.now()
    print((end - begin).seconds)
    info_df = pd.DataFrame(rows)

    info_df.to_csv('test.csv')