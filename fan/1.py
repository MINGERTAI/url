import requests
import json
import hashlib
import configparser
import re
import os

headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    config = configparser.ConfigParser()
    config_directory = os.path.join("fan", "FatCat")
    config_path = os.path.join(config_directory, "config.ini")
    config.read(config_path)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            new_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            old_md5 = config.get('DEFAULT', 'md5', fallback='')
            if new_md5 != old_md5:
                print("检测到更新。")
                config['DEFAULT']['md5'] = new_md5
                with open(config_path, 'w') as configfile:
                    config.write(configfile)
                
                if 'spider' in data:
                    original_url = data['spider'].split(';md5;')[0]
                    data['spider'] = data['spider'].replace(original_url, './fan/FatCat/PandaQ240609.jar')

                # 确保目标目录存在
                if not os.path.exists(config_directory):
                    os.makedirs(config_directory)

                # 保存修改后的data为JSON文件
                json_file_path = os.path.join(config_directory, file_name + '.json')
                with open(json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{json_file_path}")

            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

url = 'http://肥猫.com'
file_name = 'website_content'
save_website_content_as_json_and_check_updates(url, file_name)
