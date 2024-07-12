# 目标URL
# url = "https://www.xn--4kq62z5rby2qupq9ub.xyz/"  # 请确认此URL是否正确
#url = "https://www.王小牛放牛娃.xyz/"  # 请确认此URL是否正确
#url = "http://tvbox.王二小放牛娃.xyz/"  # 请确认此URL是否正确

import requests
import json
import os
import sys
import re
import base64
import hashlib
import configparser
from datetime import datetime

# 设置请求头，模拟浏览器请求
headers = {
    'User-Agent': 'okhttp/3.15'
}

# 目标URL
url = "http://tvbox.王二小放牛娃.xyz/"  # 更新为实际的 JSON 数据 URL

# 发送GET请求
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    print(f"响应头: {response.headers}")
    print(f"响应内容: {response.text[:1000]}")  # 打印响应内容的前1000个字符进行调试
except requests.exceptions.RequestException as e:
    print(f"HTTP请求失败: {e}")
    exit(1)

# 检查响应的Content-Type以确认是否为JSON
content_type = response.headers.get('Content-Type')
if 'application/json' not in content_type:
    print(f"响应的Content-Type不是JSON: {content_type}")
    exit(1)

# 尝试解析JSON内容
try:
    data = response.json()
except json.JSONDecodeError as e:
    print(f"JSON解析失败: {e}")
    print(f"响应内容: {response.text[:1000]}")  # 打印响应内容的前1000个字符进行调试
    exit(1)

# 创建输出目录
output_dir = 'out'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 定义输出文件路径
output_file = os.path.join(output_dir, 'xyz.json')

# 将JSON内容写入文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"JSON内容已保存到 {output_file}")
