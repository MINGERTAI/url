import requests
import json  # 确保导入json模块
import re
import base64
import hashlib
import configparser

#def save_website_content_as_json(url, file_name):
def save_website_content_as_json(url):
    headers = {'User-Agent': 'okhttp/3.15'}
    
    # 尝试发起GET请求
    try:
        response = requests.get(url, headers=headers)
        
        
        # 检查状态码，确认请求成功
        if response.status_code == 200:
            try:
                # 尝试将响应内容解析为JSON
                #match = response.text()
                match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)
                # 如果成功，以JSON格式保存
                #with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    #json.dump(data, file, indent=4, ensure_ascii=False)
                #print(f"数据已以JSON格式保存到{file_name}.json")
                content = content.replace(url, './fan/JAR/fan.txt')
                with open('1.json', 'w', newline='', encoding='utf-8') as f:
                    f.write(data)
            except ValueError:
                # 如果响应内容不是有效的JSON格式，保存为文本文件
                with open(file_name + '.txt', 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"网站内容已保存到{file_name}.txt")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
#file_name = 'website_content'

#save_website_content_as_json(url, file_name)
