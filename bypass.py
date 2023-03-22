import time
import bs4
import undetected_chromedriver as uc
import datetime

start = datetime.datetime.now()
options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--proxy-server=190.61.88.147:8080')

driver = uc.Chrome(use_subprocess=True, version_main=111, options=options, driver_executable_path="/home/p.kuznetsov/chromedriver", browser_executable_path="/home/p.kuznetsov/chrome/opt/google/chrome/google-chrome")
driver.set_page_load_timeout(15)
driver.get('https://bina.az/items/2000000')

# Get the HTML source of the page using the driver
html = driver.page_source
# Print the HTML source
print(html)

# Close the driver
driver.quit()
print((datetime.datetime.now() - start).seconds)