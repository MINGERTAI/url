import requests
import json  # 导入json模块

def save_response_as_json(url, file_name):
    headers = {'User-Agent': 'okhttp/3.15'}
    
    # 发起GET请求
    response = requests.get(url, headers=headers)
    
    # 检查状态码，确认请求成功
    if response.status_code == 200:
        try:
            # 尝试将响应内容解析为JSON
            data = response.json()
            
            # 将解析后的JSON数据保存到文件
            with open(file_name, 'w', encoding='utf-8') as file:
                # ensure_ascii=False用于确保中文等非ASCII字符在文件中正确显示
                file.write(json.dumps(data, indent=4, ensure_ascii=False))
                
            print(f"数据已保存到{file_name}")
        except ValueError:
            # 如果响应内容不是有效的JSON格式
            print("响应的内容不是有效的JSON格式。")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 目标URL
url = 'http://肥猫.com'
# 保存的文件名
file_name = '1.json'

save_response_as_json(url, file_name)
