import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
from webdriver_manager.chrome import ChromeDriverManager

# 启动BrowserMob Proxy服务器
server = Server("/path/to/browsermob-proxy")  # 请下载并指定browsermob-proxy的路径
server.start()
proxy = server.create_proxy()

# 配置Selenium使用BrowserMob Proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy.proxy}')

# 初始化Chrome浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 设定要捕获的URL
proxy.new_har("tvbox", options={'captureHeaders': True, 'captureContent': True})

# 访问目标网址
url = "http://tvbox.王二小放牛娃.xyz"
driver.get(url)

# 等待页面加载完成
time.sleep(10)

# 获取网络请求
har = proxy.har

# 查找包含JSON数据的请求
for entry in har['log']['entries']:
    request_url = entry['request']['url']
    if "some_condition_to_identify_json_requests" in request_url:  # 修改为识别JSON请求的条件
        response_content = entry['response']['content']['text']
        try:
            data = json.loads(response_content)
            # 保存到文件
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("数据已以JSON格式保存到 data.json")
        except json.JSONDecodeError:
            print("无法解析JSON数据")

# 关闭浏览器和代理
driver.quit()
server.stop()
