import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}
url = 'http://肥猫.com'
response = requests.get(url, headers=headers)
match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)
