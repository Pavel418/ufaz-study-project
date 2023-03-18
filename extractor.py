import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp
import undetected_chromedriver as uc 

import time

def pageDataExtract(id, session, wait_time):
        url = f'https://bina.az/items/{id}'
        try:
            text = session.get(url).text
        except Exception as e:
            print("Connection reset. waiting ", wait_time, " seconds")
            time.sleep(5)
            return pageDataExtract(id, session, wait_time + 5)
        if "Tapılmadı" in text:
            print("empty ", id)
            return

        if "Checking if the site connection is secure" in text:
            print("bypassing security ", id)
            options = uc.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--headless')

            print("launch ", id)
            driver = uc.Chrome(use_subprocess=True,options=options)
            print("get ", id)
            driver.get(url)
            time.sleep(5)
            text = driver.page_source
            print("security bypassed ", id)
            driver.quit()

        locations = ""
        info = {}
        fields = {"Kateqoriya", "Mərtəbə", "Sahə", "Otaq sayı","Çıxarış","Təmir", "İpoteka"}

        soup = BeautifulSoup(text, 'lxml')
        element = soup.find('div', {"class":"search-row__cell search-row__cell--leased"})
        if element is None:
            print("`no search ", id)
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
    session = requests.Session() 
    rows= []
    begin = datetime.datetime.now()
    '''
    with mp.Pool() as pool:
        results = pool.starmap(pageDataExtract, [(i, session, 5) for i in range(3000000, 3100000)])
        for row in results:
            if row is not None:
                rows.append(row)'''
    pageDataExtract(3000000, session, 5)
    end = datetime.datetime.now()
    print((end - begin).seconds)
    info_df = pd.DataFrame(rows)

    info_df.to_csv('test.csv')