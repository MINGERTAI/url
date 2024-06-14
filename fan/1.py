import re
import json
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # 假设响应内容是JSON格式


    if not data:
        return
    result = data.group(1)

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
    content = content.replace(url, './fan/FatCat/PandaQ240609.jar')
    content = diy_conf(content)             # 从这里diy_conf添加自己的
    content = modify_content(content)
    with open(file_name + '.json', 'w', encoding='utf-8') as file:
    #with open('1.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)


    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("./fan/FatCat/config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)
        with open("./fan/FatCat/config.ini", "w") as f:
            config.write(f)

        response = requests.get(url)
        with open("./fan/FatCat/PandaQ240609.jar", "wb") as f:
            f.write(response.content)


if __name__ == '__main__':
    get_fan_conf()
