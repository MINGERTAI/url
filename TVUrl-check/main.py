import requests
import json
import os

# 目标URL
url = "https://www.xn--4kq62z5rby2qupq9ub.xyz/"

# 发送GET请求
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
except requests.exceptions.RequestException as e:
    print(f"HTTP请求失败: {e}")
    exit(1)

# 尝试解析JSON内容
try:
    data = response.json()
except json.JSONDecodeError as e:
    print(f"JSON解析失败: {e}")
    print(f"响应内容: {response.text}")
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
