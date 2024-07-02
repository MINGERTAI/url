import requests
import json
import hashlib
import configparser
import re
import os

headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    # 定义配置文件和jar文件的保存路径
    config_directory = os.path.join("fan", "FatCat")
    config_path = os.path.join(config_directory, "config.ini")
    
    # 确保目标目录存在
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)

    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
                with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{file_name}")
                
            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'FatCat'

save_website_content_as_json_and_check_updates(url, file_name)

#def diy_conf(content):
    # 这里添加您需要的任何特定修改
    #modified_content = content
    #return modified_content

# 读取保存的JSON数据
#with open(file_name + '.json', 'r', encoding='utf-8') as f:
   # content = f.read()

# 修改内容
#modified_content = diy_conf(content)
