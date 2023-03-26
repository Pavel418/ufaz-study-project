import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import multiprocessing as mp
import undetected_chromedriver as uc
import os
import random
import warnings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
import time

timeout = urllib3.Timeout(connect=1.5, read=1.5)
lock = mp.Lock()
count = mp.Value("i", 20000)
max_count = 20000
manager = mp.Manager()
static_proxies = manager.list()
urlList = ["https://free-proxy-list.net/", "https://www.sslproxies.org/"]
websiteIndex = mp.Value('i', 0)

driver_path = "C:\Program Files\Google\chromedriver.exe"
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

if(os.name == 'nt'):
    driver_path = "C:\Program Files\Google\chromedriver.exe"
    chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
else:
    driver_path = "/home/p.kuznetsov/chromedriver"
    chrome_path = "/home/p.kuznetsov/chrome/opt/google/chrome/google-chrome"

def checkProxy(proxy):
    session = requests.Session()
    proxy = 'https://' + proxy
    session.proxies = {
        'https': proxy,
    }
    try:
        result = "banned" not in session.get("https://bina.az/items/2000000", timeout=timeout, verify=False).text
    except:
        return False
    return result 

def getChrome(options):
    global driver_path, chrome_path
    return uc.Chrome(use_subprocess=True, version_main=111, options=options, driver_executable_path=driver_path, browser_executable_path=chrome_path)

def scanUrlForProxies(url):
        session = requests.Session()
        text = session.get(url, verify=False).text

        soup = BeautifulSoup(text, 'lxml')
        proxies = soup.select('tr')
        proxies.pop(0)
        
        for p in proxies:
            if(len(p) == 8):
                result = p.select('td')
                if result[-2].text == "yes":
                    proxy = result[0].text+":"+result[1].text
                    if checkProxy(proxy):
                        static_proxies.append(proxy)

def getProxies():
    global count, static_proxies, max_count
    lock.acquire()
    print("count value ", count.value)
    count.value += 1
    if(count.value >= max_count or len(static_proxies) < 1):
        print("scan started")
        scanUrlForProxies(urlList[websiteIndex.value])
        websiteIndex.value += 1
        if websiteIndex.value >= len(urlList):
            websiteIndex.value = 0
        count.value = 0
        print("scan complete")
    lock.release()
    return static_proxies

def getDriver():
    proxy = random.choice(list(getProxies()))
    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(f'--proxy-server={proxy}')

    return getChrome(options)

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

def pageDataExtract(id):
    try:
        session = requests.Session()
        retry = Retry(connect=2, backoff_factor=0, raise_on_status=True)
        adapter = HTTPAdapter(max_retries=retry, pool_maxsize=30)
        session.mount('https://', adapter)
        proxy = random.choice(getProxies())
        session.proxies = {
        'https': proxy,
        }
        url = f'https://bina.az/items/{id}'
        try:
            startRequest = datetime.datetime.now()
            text = session.get(url, verify=False, timeout=timeout).text
        except Exception as e:
            print(e)
            lock.acquire()
            try:
                static_proxies.remove(proxy)
            except:
                pass
            lock.release()
            return pageDataExtract(id)
        endRequest = datetime.datetime.now()
        if (endRequest - startRequest).seconds > 6:
            lock.acquire()
            try:
                static_proxies.remove(proxy)
            except:
                pass
            lock.release()

        if "Tapılmadı" in text:
            return None

        if "Just a moment..." in text:
            driver = getDriver()
            print("security bypass")
            try:
                driver.set_page_load_timeout(10)
                driver.get(url)
                time.sleep(5)
                text = driver.page_source
                if "banned" in text:
                    raise Exception()
            except:
                print("failed")
                quit_driver_and_reap_children(driver)
                return pageDataExtract(id)
            quit_driver_and_reap_children(driver)
            print("success")
        locations = ""
        info = {}
        fields = {"Kateqoriya", "Mərtəbə", "Sahə", "Otaq sayı","Çıxarış","Təmir", "İpoteka"}
        soup = BeautifulSoup(text, 'lxml')
        element = soup.find('div', {"class":"search-row"})
        if element is None:
            return None
        element = element.find('div', {"class":"search-row__cell search-row__cell--leased"})
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
    rows= []
    begin = datetime.datetime.now()
    with mp.Pool() as pool:
        results = pool.map(pageDataExtract, [i for i in range(2600000, 2700000)])
        for row in results:
            if row is not None:
                rows.append(row)
    end = datetime.datetime.now()
    print((end - begin).seconds)
    info_df = pd.DataFrame(rows)

    info_df.to_csv('2.6-3.csv')