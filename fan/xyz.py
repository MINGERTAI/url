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
url = "http://tvbox.王二小放牛娃.xyz"
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

# 查找包含JSON数据的<script>标签（假设数据嵌入在<script>标签中）
script_tag = soup.find('script', {'type': 'application/json'})
if script_tag:
    json_data = script_tag.string  # 获取JSON字符串
    data = json.loads(json_data)  # 解析JSON数据
    print(data)

    # 保存到文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
else:
    print("没有找到包含JSON数据的<script>标签")

# 关闭浏览器
driver.quit()
