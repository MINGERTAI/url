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
                
                spider = data.get('spider')
                if spider:
                    jar_match = re.match(r'http://[^/]+/jar/(.+?);md5;([a-f0-9]{32})', spider)
                    if jar_match:
                        jar_url, jar_md5 = jar_match.groups()
                        full_jar_url = f"http://like.xn--z7x900a.com/jar/{jar_url}"
                        jar_response = requests.get(full_jar_url)
                        if jar_response.status_code == 200:
                            jar_file_name = jar_url.split('/')[-1]
                            # 构建jar文件的完整保存路径
                            jar_file_path = os.path.join(config_directory, jar_file_name)
                            with open(jar_file_path, 'wb') as jar_file:
                                jar_file.write(jar_response.content)
                            print(f"jar文件已下载到：{jar_file_path}")
                            # 更新配置文件
                            config['DEFAULT']['jar_md5'] = jar_md5
                            with open(config_path, 'w') as configfile:
                                config.write(configfile)
                            print("jar文件的md5值已更新。")
                        else:
                            print(f"jar文件下载失败，状态码：{jar_response.status_code}")

                if 'spider' in data:
                    original_url = data['spider'].split(';md5;')[0]
                    data['spider'] = data['spider'].replace(original_url, f'./fan/FatCat/{jar_file_name}')
                
                # 将修改后的data保存为JSON文件
                with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到 {file_name}.json")

                # 假定这是要保存的数据示例
                new_data = [
                    {"key": "短剧", "name": "🌈上头┃短剧", "type": 3, "api": "csp_Djuu", "searchable": 1, "quickSearch": 1, "changeable": 1},
                    {"key": "酷看", "name": "💡酷看┃秒播", "type": 3, "api": "csp_Kkys", "timeout": 15, "searchable": 1, "quickSearch": 1, "changeable": 1},
                    {"key": "原创", "name": "☀原创┃不卡", "type": 3, "api": "csp_YCyz", "timeout": 15, "playerType": 1, "searchable": 1, "quickSearch": 1, "changeable": 1}
                ]

                # 生成JSON字符串并保存到文件
                save_json_compact('1.json', new_data)
                
            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

def save_json_compact(file_path, data):
    """将JSON数据保存为紧凑的一行格式"""
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_str)
    print(f"数据已以紧凑的JSON格式保存到 {file_path}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'FatCat'

save_website_content_as_json_and_check_updates(url, file_name)
