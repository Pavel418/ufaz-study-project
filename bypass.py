import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import datetime
import random

start = datetime.datetime.now()

count = 100
max_count = 100
static_proxies = []
driver_path = "C:\Program Files\Google\chromedriver.exe"
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

def getChrome(options):
    global driver_path, chrome_path
    return uc.Chrome(use_subprocess=True, version_main=111, options=options, driver_executable_path=driver_path, browser_executable_path=chrome_path)

def getProxies():
    global count, static_proxies, max_count
    ++count
    if(count >= max_count):
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')

        driver = getChrome(options)
        driver.get("https://www.sslproxies.org/")

        list_proxies = []

        text = driver.page_source
        soup = BeautifulSoup(text, 'lxml')
        proxies = soup.select('tr')
        proxies.pop(0)
        for p in proxies:
            if(len(p) == 8):
                result = p.select('td')
                if result[-2].text == "yes":
                    list_proxies.append(result[0].text+":"+result[1].text)

        driver.close()
        static_proxies = list_proxies
        count = 0
        return list_proxies
    else:
        return static_proxies

def getDriver():
    proxy = random.choice(getProxies())
    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument(f'--proxy-server={proxy}')

    return getChrome(options)

driver = getDriver()
driver.set_page_load_timeout(15)
driver.get('https://bina.az/items/2000000')

# Get the HTML source of the page using the driver
html = driver.page_source
# Print the HTML source
print(html)

# Close the driver
driver.quit()
print((datetime.datetime.now() - start).seconds)