import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp

def pageDataExtract(id, session):
    try:
        url = f'https://bina.az/items/{id}'
        r = session.get(url)
        if "Tapılmadı" in r.text:
            return

        locations = ""
        info = {}
        fields = {"Kateqoriya", "Mərtəbə", "Sahə", "Otaq sayı","Çıxarış","Təmir", "İpoteka"}

        soup = BeautifulSoup(r.text, 'lxml')
        if "Alış" != soup.find('div', {"class":"search-row__cell search-row__cell--leased"}).find('option', {"selected": "selected"}).text:
            return
        trs = soup.find("table", {"class": "parameters"}).find_all('tr')
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
                    "city":city, 'longtitude': longitude, "id": id})
        return info
    except Exception as e:
        return

if __name__ == "__main__":
    session = requests.Session()
    rows= []
    begin = datetime.datetime.now()
    with mp.Pool() as pool:
        results = pool.starmap(pageDataExtract, [(i, session) for i in range(2000000, 3500000, 868)])
        for row in results:
            if row is not None:
                rows.append(row)
    #rows.append(pageDataExtract(3142195, session))
    end = datetime.datetime.now()
    print((end - begin).seconds)
    info_df = pd.DataFrame(rows)

    info_df.to_csv('data.csv')