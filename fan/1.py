import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    # config = configparser.ConfigParser()
    # config.read("fan/config.ini")

    url = 'https://github.com/ne7359/tvurl/blob/main/dianshi.json'
    response = requests.get(url, headers=headers)

        response = requests.get(url)
        with open("./out/fan.txt", "wb") as f:
            f.write(response.content)
if __name__ == '__main__':
    get_fan_conf()
