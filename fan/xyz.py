import requests
from bs4 import BeautifulSoup
import json

# 定义要爬取的URL
url = "http://tvbox.王二小放牛娃.xyz"

# 发送HTTP请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 查找包含所需数据的标签（根据实际情况修改）
    data = {}
    for item in soup.find_all('div', class_='item-class'):  # 修改为实际的HTML标签和类名
        title = item.find('h2').text  # 修改为实际的标签
        description = item.find('p').text  # 修改为实际的标签
        data[title] = description

    # 将数据转换为JSON格式
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    print(json_data)
else:
    print("Failed to retrieve the webpage")

# 保存到文件
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
