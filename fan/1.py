import re
import json
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("./fan/FatCat/config.ini")

    url = 'http://肥猫.com'
try:
    response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # 假设响应内容是JSON格式
                # 将响应内容保存为JSON文件
                with open(response + '.text', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{file_name}.json")


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
    content = content.replace(url, './fan/FatCat/PandaQ240609.jar')
    content = diy_conf(content)             # 从这里diy_conf添加自己的
    content = modify_content(content)

    with open('1.json', 'w', newline='', encoding='utf-8') as f:
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
