import requests
from bs4 import BeautifulSoup

id = 3030965
url = f'https://bina.az/items/{id}'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')

trs = soup.find("table", {"class": "parameters"}).findAll('tr')
keys,vals = list(),list()
for i in trs:
    keys.append((i.findAll("td"))[0].text)
    vals.append((i.findAll("td"))[1].text)

info = dict(zip(keys,vals))

price = {'price' : int(soup.find('span', {"class":"price-val"}).text.replace(" ", "")) , "price-cur" : soup.find('span', {"class":"price-cur"}).text}
info.update(price)

loclist = soup.find("ul",{"class":"locations"}).findAll("a")
locations =[i.text for i in loclist]
info.update({"locations" : locations})

print(info)
