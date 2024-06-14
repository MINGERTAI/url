import requests
import json
import hashlib
import configparser
import re
import os

headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    config = configparser.ConfigParser()
    config.read(os.path.join("fan", "FatCat", "config.ini"))
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            new_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            old_md5 = config.get('DEFAULT', 'md5', fallback='')
            if new_md5 != old_md5:
                print("检测到更新。")
                config['DEFAULT']['md5'] = new_md5
                with open(os.path.join("fan", "FatCat", "config.ini"), 'w') as configfile:
                    config.write(configfile)

                # 检查并修改spider字段
                if 'spider' in data:
                    original_url = data['spider'].split(';md5;')[0]
                    data['spider'] = './fan/JAR/fan.txt;md5;5ee96d541532306c3acc8c0fc229acbf'
                
                # 保存修改后的JSON数据
                with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{file_name}.json")
            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

url = 'http://肥猫.com'
file_name = 'website_content'
save_website_content_as_json_and_check_updates(url, file_name)

def diy_conf(content):
    # 这里添加您需要的任何特定修改
    modified_content = content
    return modified_content

# 读取保存的JSON数据
with open(file_name + '.json', 'r', encoding='utf-8') as f:
    content = f.read()

# 修改内容
modified_content = diy_conf(content)

# 将修改后的内容写入C.json
with open('C.json', 'w', encoding='utf-8') as f:
    f.write(modified_content)
import json


# 将数据保存到文件，不使用缩进
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

# 或者，如果您想要得到字符串形式的 JSON 数据，可以使用 json.dumps()
json_string = json.dumps(data, ensure_ascii=False)
print(json_string)
