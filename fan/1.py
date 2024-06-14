import requests
#import json
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
                
                # 从JSON数据中提取包含jar文件URL和md5值的"spider"字段
                spider = data.get('spider')
                if spider:
                    match = re.match(r'http://[^/]+/jar/(.+?);md5;([a-f0-9]{32})', spider)
                    if match:
                        jar_url, jar_md5 = match.groups()
                        full_jar_url = f"http://like.xn--z7x900a.com/jar/{jar_url}"
                        # 下载jar文件
                        jar_response = requests.get(full_jar_url)
                        if jar_response.status_code == 200:
                            jar_file_name = jar_url.split('/')[-1]  # 从URL提取文件名
                            with open(os.path.join("fan", "FatCat", jar_file_name), 'wb') as jar_file:
                                jar_file.write(jar_response.content)
                            print(f"jar文件已下载到：{jar_file_name}")
                            config['DEFAULT']['jar_md5'] = jar_md5
                            with open(os.path.join("fan", "FatCat", "config.ini"), 'w') as configfile:
                                config.write(configfile)
                            print("jar文件的md5值已更新。")
                        else:
                            print(f"jar文件下载失败，状态码：{jar_response.status_code}")
                    else:
                        print("spider字段格式不匹配。")
            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'website_content'

save_website_content_as_json_and_check_updates(url, file_name)
