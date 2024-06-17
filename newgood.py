import requests
import json  # 确保导入json模块
import re
import base64
import hashlib
import configparser

def save_website_content_as_json(url):
    headers = {'User-Agent': 'okhttp/3.15'}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                # 尝试将响应内容解析为JSON
                match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

                if match:
                    content = match.group(1)

                    # 确保内容是JSON格式，然后加载它
                    data = json.loads(content)

                    # 替换指定内容
                    content = content.replace(url, './fan/JAR/fan.txt')

                    # 生成JSON字符串并保存到文件
                    #with open('1.json', 'w', newline='', encoding='utf-8') as f:
                        #json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                    with open('1.json', 'w', newline='', encoding='utf-8') as f:
                        f.write(data, f, ensure_ascii=False, separators=(',', ':'))
                    
                    print("数据已保存到 1.json")
                else:
                    raise ValueError("匹配失败，未找到有效内容")
            except ValueError as e:
                with open('1.txt', 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"网站内容已保存到1.txt，因为响应不是有效的JSON格式: {str(e)}")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'

save_website_content_as_json(url)
# 文件名，不包括扩展名
#file_name = 'website_content'

#save_website_content_as_json(url, file_name)
