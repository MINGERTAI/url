import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    # config = configparser.ConfigParser()
    # config.read("fan/config.ini")

    url = 'https://raw.githubusercontent.com/ne7359/tvurl/main/dianshi.json'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

    if not match:
        return
    result = match.group(1)

    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5 = m.hexdigest()

    content = base64.b64decode(result).decode('utf-8')
    url = re.search(r'spider"\:"(.*);md5;', content).group(1)
    content = content.replace(url, './out/fan.txt')
    content = diy_conf(content)

    with open('out/11.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)

    # Update conf.md5
    config.set("md5", "conf", md5)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)

        response = requests.get(url)
        with open("./out/fan.txt", "wb") as f:
            f.write(response.content)
