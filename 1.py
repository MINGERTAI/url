import requests
from bs4 import BeautifulSoup

url = "http://tvbox.王二小放牛娃.xyz"

# 设置请求头，模仿浏览器的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 根据需要提取的信息调整选择器
# 例如，提取所有的<a>标签
links = soup.find_all('a')

for link in links:
    print(link.get('href'))

# 注意：这里的选择器和提取逻辑需要根据实际的HTML结构进行调整
