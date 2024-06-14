from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# 初始化Chrome浏览器
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启用无头模式，不会显示浏览器界面
driver = webdriver.Chrome(service=service, options=options)

# 访问目标网址
url = "http://lige.unaux.com/?url=http://tvbox.王二小放牛娃.xyz&i=1"
driver.get(url)

# 等待页面加载完成
time.sleep(10)  # 等待10秒，具体时间可以根据页面加载情况调整

# 获取页面内容
content = driver.page_source

# 保存页面内容以便调试
with open('page_content.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 查找包含JSON数据的元素
try:
    # 假设JSON数据嵌入在某个元素的text或属性中
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//pre"))  # 修改为实际的XPath
    )
    json_data = element.text

    # 解析JSON数据
    data = json.loads(json_data)
    print(data)

    # 保存到文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("数据已以JSON格式保存到 data.json")
except Exception as e:
    print(f"发生错误：{str(e)}")

# 关闭浏览器
driver.quit()
