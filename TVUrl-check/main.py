import requests
from bs4 import BeautifulSoup

url = "http://tvbox.王二小放牛娃.xyz"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    json_data = response.json()
else:
    print(f"Failed to fetch data with status code {response.status_code}")
