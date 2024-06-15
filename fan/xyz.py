import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 设置浏览器选项
options = Options()
options.add_argument('--headless')  # 启用无头模式，不会显示浏览器界面
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 初始化Chrome浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 访问目标网址
url = "http://tvbox.王二小放牛娃.xyz"
driver.get(url)

# 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body")))

# 获取页面内容
content = driver.page_source

# 保存页面内容以便调试
with open('page_content.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 关闭浏览器
driver.quit()

# 使用正则表达式提取匹配项
pattern = re.compile(r'[A-Za-z0]{8}\*\*(.*)', re.DOTALL)
match = pattern.search(content)

if match:
    result = match.group(1)
    print(f"匹配的内容: {result}")
else:
    print("没有找到匹配项")
