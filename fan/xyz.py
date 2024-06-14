from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import re

# 初始化Chrome浏览器
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启用无头模式，不会显示浏览器界面
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

# 提取JSON数据
# 假设JSON数据在 <script> 标签或某个特定的标记中
pattern = re.compile(r'{\s*"spider".*?}', re.DOTALL)  # 修改为实际的正则表达式模式
matches = pattern.findall(content)

if matches:
    json_str = matches[0]  # 假设匹配到的第一个是所需的JSON数据
    try:
        data = json.loads(json_str)
        # 保存JSON数据到文件
        json_file_path = 'data.json'
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"数据已以JSON格式保存到 {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"无法解析JSON数据。错误信息：{str(e)}")
else:
    print("没有找到包含指定关键字的JSON数据")
