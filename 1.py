import requests
from bs4 import BeautifulSoup
import json  # 导入json模块

url = "http://tvbox.王二小放牛娃.xyz"

# 设置请求头，模仿浏览器的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 创建一个空列表来存储链接
links_list = []

# 提取所有的<a>标签，并将链接添加到列表中
for link in soup.find_all('a'):
    href = link.get('href')
    if href:  # 确保href不为空
        links_list.append(href)

# 将列表保存为JSON格式的文件
with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(links_list, f, ensure_ascii=False, indent=4)

print("已将链接保存到test.json文件中。")
