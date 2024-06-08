import requests
import json
import os

# 构建 urls.json 文件的完整路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, 'tv', 'urls.json')

# 用于存储有效链接的列表
valid_links = []

try:
    # 读取 JSON 数据
    with open(data_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)["urls"]  # 根据新的结构读取 urls

    # 遍历 JSON 数据中的每个链接
    for item in data:
        url = item["url"]
        name = item["name"]

        try:
            response = requests.get(url, timeout=10, verify=False)  # verify=False 跳过 SSL 验证，如有需要
            
            # 检查响应状态码，如果为 200 则认为链接有效
            if response.status_code == 200:
                print(f"链接 {name} 有效。")
                valid_links.append(item)
            else:
                print(f"链接 {name} 无效，状态码：{response.status_code}。")
        except Exception as e:
            # 请求出错（如超时或连接错误）也认为链接无效
            print(f"链接 {name} 无法访问，错误：{e}。")

    # 准备保存的新 JSON 结构，包含 "urls"
    new_data = {"urls": valid_links}

    # 保存所有有效链接到新的 JSON 文件
    valid_links_file_path = os.path.join(current_dir, 'tv', 'valid_links.json')
    with open(valid_links_file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

    print(f"所有有效链接已经保存到 {valid_links_file_path} 文件。")
except Exception as e:
    print(f"读取或处理 JSON 数据时发生错误：{e}")
