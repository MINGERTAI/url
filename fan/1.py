import requests
import json
import hashlib
import configparser
import re
import os  # 导入os模块

headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    config = configparser.ConfigParser()
    config.read(os.path.join("fan", "FatCat", "config.ini"))  # 使用os.path.join确保路径正确
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # 假设响应内容是JSON格式

            # 计算返回数据的md5值来检查数据是否有更新
            new_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            old_md5 = config.get('DEFAULT', 'md5', fallback='')
            if new_md5 != old_md5:
                print("检测到更新。")
                # 更新配置文件中的md5值
                config['DEFAULT']['md5'] = new_md5
                with open(os.path.join("fan", "FatCat", "config.ini"), 'w') as configfile:
                    config.write(configfile)

                # 直接在data字典上修改spider字段的值
                if 'spider' in data:
                    original_url = data['spider'].split(';md5;')[0]  # 假设spider字段的格式为"URL;md5;MD5值"
                    data['spider'] = data['spider'].replace(original_url, './fan/FatCat/PandaQ240609.jar')

                # 将修改后的data保存为JSON文件
                with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{file_name}.json")
                
                # 从这里开始，代码逻辑保持不变...

    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'website_content'

save_website_content_as_json_and_check_updates(url, file_name)
