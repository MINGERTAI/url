import requests
from bs4 import BeautifulSoup

url = 'http://tvbox.王二小放牛娃.xyz'
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print("Failed to get JSON data.")
