import requests
import json
import hashlib
import configparser
import re
import os

headers = {'User-Agent': 'okhttp/3.15'}

# 自定义格式化函数
def custom_format(data):
    formatted = json.dumps(data, ensure_ascii=False, indent=4)
    formatted = formatted.replace('",', '",\n').replace('},', '},\n')
    formatted = formatted.replace('":[', '":[\n').replace('":"', '":"\n').replace('":{', '":{\n')
    return formatted

def save_website_content_as_json_and_check_updates(url, file_name):
    # 定义配置文件和jar文件的保存路径
    config_directory = os.path.join("fan", "FatCat")
    config_path = os.path.join(config_directory, "config.ini")
    
    # 确保目标目录存在
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            new_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            old_md5 = config.get('DEFAULT', 'md5', fallback='')
            if new_md5 != old_md5:
                print("检测到更新。")
                # 更新配置文件中的md5值
                config['DEFAULT']['md5'] = new_md5
                with open(config_path, 'w') as configfile:
                    config.write(configfile)
                
                # 替换data字典中的特定字符串
                for key in data:
                    if isinstance(data[key], str):
                        data[key] = data[key].replace('http://js.xn--z7x900a.com/', './fan/FatCat/')
                
                # 使用自定义格式化函数格式化data
                custom_formatted_data = custom_format(data)
                
                # 保存自定义格式化后的数据到JSON文件
                json_file_path = os.path.join(config_directory, file_name + '.json')
                with open(json_file_path, 'w', encoding='utf-8') as file:
                    file.write(custom_formatted_data)
                print(f"数据已以自定义格式保存到 {json_file_path}")
                
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
