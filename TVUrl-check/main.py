import requests
from bs4 import BeautifulSoup

def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        json_data = soup.find_all('script', type='application/json')[0].text.strip()
        with open('./out/tvbox.json', 'w') as file:
            file.write(json_data)
        print("JSON文件已下载到当前目录下的'tvbox/tvbox.json'")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 网页URL
url = "http://tvbox.王二小放牛娃.xyz"

download_json(url)
