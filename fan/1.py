import requests
import json
import hashlib
import configparser
import re
import os

def save_website_content_as_json(url, file_name):
    headers = {'User-Agent': 'okhttp/3.15'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            match = response.json()

    if not match:
        return
    result = match.group(1)

    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5 = m.hexdigest()

    try:
        old_md5 = config.get("md5", "conf")
        if md5 == old_md5:
            print("No update needed")
            return
    except:
        pass

    content = base64.b64decode(result).decode('utf-8')
    url = re.search(r'spider"\:"(.*);md5;', content).group(1)
    content = content.replace(url, './fan/JAR/fan.txt')
    content = diy_conf(content)             # 这里添加diy_conf
    content = modify_content(content)

    with open('1.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)

url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'website_content'

save_website_content_as_json(url, file_name)

  if __name__ == '__main__':
    get_fan_conf()
