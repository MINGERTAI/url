import requests
import json
import os

# 目标URL
url = "https://www.xn--4kq62z5rby2qupq9ub.xyz/"

# 发送GET请求
response = requests.get(url)

# 检查响应状态
if response.status_code == 200:
    # 解析JSON内容
    data = response.json()
    
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
    
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
