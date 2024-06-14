from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from bs4 import BeautifulSoup
import time

# 使用webdriver-manager自动下载并管理ChromeDriver
service = Service(ChromeDriverManager().install())

# 初始化Chrome浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启用无头模式，不会显示浏览器界面
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=service, options=options)

# 访问目标网址
url = "http://肥猫.com"
driver.get(url)

# 等待页面加载完成
time.sleep(10)  # 等待10秒，具体时间可以根据页面加载情况调整

# 获取页面内容
content = driver.page_source

# 打印页面内容以便调试
with open('page_content.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 解析HTML内容
soup = BeautifulSoup(content, 'html.parser')

# 查找包含所需数据的标签（根据实际情况修改）
data = {}
items = soup.find_all('div', class_='item-class')  # 修改为实际的HTML标签和类名
if not items:
    print("没有找到匹配的元素，请检查选择器")
for item in items:
    title = item.find('h2').text if item.find('h2') else '无标题'  # 修改为实际的标签
    description = item.find('p').text if item.find('p') else '无描述'  # 修改为实际的标签
    data[title] = description

# 将数据转换为JSON格式
json_data = json.dumps(data, ensure_ascii=False, indent=4)
print(json_data)

# 保存到文件
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

# 关闭浏览器
driver.quit()
