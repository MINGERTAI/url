from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
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

# 使用正则表达式提取包含"spider"和"sites"关键字的JSON数据
pattern = re.compile(r'{"key":"玩偶".*?}', re.DOTALL)  # 修改为实际的正则表达式模式
matches = pattern.findall(content)

if matches:
    json_data = matches[0]  # 假设匹配到的第一个是所需的JSON数据
    data = json.loads(json_data)  # 解析JSON数据
    print(data)

    # 保存到文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
else:
    print("没有找到包含指定关键字的JSON数据")

# 关闭浏览器
driver.quit()
