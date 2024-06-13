import requests
from bs4 import BeautifulSoup
import json

def fetch_and_parse_url(url):
    try:
        # 发起请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取网页标题
            title = soup.title.string if soup.title else '无标题'
            
            # 将数据转换为JSON格式
            data_json = json.dumps({'title': title}, ensure_ascii=False)
            
            return data_json
        else:
            return f"请求失败，状态码：{response.status_code}"
    except Exception as e:
        return f"发生错误：{str(e)}"

# 假设的目标URL
target_url = 'http://肥猫.com'

# 调用函数，打印结果
print(fetch_and_parse_url(target_url))

# 发起请求
response = requests.get(target_url)

# 检查请求是否成功
if response.status_code == 200:
    try:
        # 尝试解析JSON数据
        data = response.json()
        
        # 假设我们想要打印出解析后的JSON中的特定信息
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("响应的内容不是有效的JSON格式。")
else:
    print(f"请求失败，状态码：{response.status_code}")
    # 使用 response.text 而不是未定义的变量 content
    with open('1.json', 'w', encoding='utf-8') as f:
        f.write(response.text)  # 将响应正文写入文件
