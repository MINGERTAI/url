import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("fan/config.ini")

    url = 'http://肥猫.com'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

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
    content = modify_content(content)

    with open('xoX.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
        
    # DIY添加自定义接口，写入b.json
    local_content = local_myconf(content)
    with open('C.json', 'w', encoding='utf-8') as f:
        for line in local_content.split('\n'):  # 将内容按行分割
            if line.strip():  # 如果该行非空（移除空白字符后有内容）
                f.write(line + '\n')  # 将非空行写入到文件中，记得在最后加上 '\n' 以保持原有的行分割

    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("fan/config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)
        with open("fan/config.ini", "w") as f:
            config.write(f)

        response = requests.get(url)
        with open("./fan/JAR/fan.txt", "wb") as f:
            f.write(response.content)

def modify_content(content):   # 更改自定义
    # Replace specified key and name  替换"key":"drpy_js_豆瓣","name":"🐼┃公众号┃肥猫宝贝" 为"key":"豆瓣","name":"智能AI广告过滤"
    content = re.sub(r'{"key":"drpy_js_豆瓣","name":"🐼┃公众号┃肥猫宝贝",', r'{"key":"豆瓣","name":"智能AI广告过滤",', content)
    
    # 删除 //{"key":  整行
    content = re.sub(r'^\s*//\{"key":.*\n', '', content, flags=re.MULTILINE)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)

    return content


if __name__ == '__main__':
    get_fan_conf()
