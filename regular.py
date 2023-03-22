import requests

session = requests.Session()
proxy = 'https://' + '103.252.117.131:25345'
session.proxies = {
    'https': proxy,
}

print(session.get("https://bina.az/items/3159176", verify=False).text)
