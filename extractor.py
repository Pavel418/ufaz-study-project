import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp
import undetected_chromedriver as uc
import os

import time

def quit_driver_and_reap_children(driver):
    driver.quit()
    try:
        pid = True
        while pid:
            pid = os.waitpid(-1, os.WNOHANG)
            
            try:
                if pid[0] == 0:
                    pid = False
            except:
                pass
    except ChildProcessError:
        pass

def pageDataExtract(id, session, wait_time):
    try:
        url = f'https://bina.az/items/{id}'
        try:
            text = session.get(url).text
        except Exception as e:
            print("Connection reset. waiting ", wait_time, " seconds")
            time.sleep(5)
            return pageDataExtract(id, session, wait_time + 5)
        if "Tapılmadı" in text:
            return None

        if "Checking if the site connection is secure" in text:
            options = uc.ChromeOptions()
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')

            driver = uc.Chrome(use_subprocess=True, version_main=111, options=options, driver_executable_path="/home/p.kuznetsov/chromedriver", browser_executable_path="/home/p.kuznetsov/chrome/opt/google/chrome/google-chrome")
            driver.get(url)
            time.sleep(5)
            text = driver.page_source
            quit_driver_and_reap_children(driver)
        locations = ""
        info = {}
        fields = {"Kateqoriya", "Mərtəbə", "Sahə", "Otaq sayı","Çıxarış","Təmir", "İpoteka"}

        soup = BeautifulSoup(text, 'lxml')
        element = soup.find('div', {"class":"search-row__cell search-row__cell--leased"})
        if element is None:
            return None
        element = element.find('option', {"selected": "selected"})
        if element is None:
            return None
        if "Alış" != element.text:
            return None
        
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
    except Exception as e:
        print(e, id)
        return

if __name__ == "__main__":
    session = requests.Session() 
    rows= []
    begin = datetime.datetime.now()
    with mp.Pool() as pool:
        results = pool.starmap(pageDataExtract, [(i, session, 5) for i in range(3100006, 3100007)])
        for row in results:
            if row is not None:
                rows.append(row)
    end = datetime.datetime.now()
    print((end - begin).seconds)
    info_df = pd.DataFrame(rows)

    info_df.to_csv('test.csv')