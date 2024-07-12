# 目标URL
# url = "https://www.xn--4kq62z5rby2qupq9ub.xyz/"  # 请确认此URL是否正确
#url = "https://www.王小牛放牛娃.xyz/"  # 请确认此URL是否正确
#url = "http://tvbox.王二小放牛娃.xyz/"  # 请确认此URL是否正确

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 设置解密网址和目标URL
decrypt_url = "https://www.xn--sss604efuw.com/jm/"
target_url = "http://tvbox.王二小放牛娃.xyz/"

# 配置 Chrome 启动选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--no-sandbox')  # 禁用沙箱
chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
chrome_options.add_argument('--disable-gpu')  # 禁用GPU

# 启动 Chrome 浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 打开解密网站
    driver.get(decrypt_url)
    time.sleep(2)  # 等待页面加载

    # 找到输入框并输入目标URL
    input_box = driver.find_element(By.TAG_NAME, "input")
    input_box.send_keys(target_url)

    # 找到解密按钮并点击
    decrypt_button = driver.find_element(By.XPATH, "//button[contains(text(), '一键解密')]")
    decrypt_button.click()
    time.sleep(5)  # 等待解密结果加载

    # 获取解密后的JSON内容
    result_area = driver.find_element(By.TAG_NAME, "textarea")
    decrypted_content = result_area.get_attribute('value')

    # 解析JSON内容
    try:
        data = json.loads(decrypted_content)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        print(f"解密内容: {decrypted_content[:1000]}")  # 打印内容的前1000个字符进行调试
        exit(1)

    # 创建输出目录
    output_dir = 'out'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 定义输出文件路径
    output_file = os.path.join(output_dir, 'xyz.json')

    # 将JSON内容写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON内容已保存到 {output_file}")

finally:
    # 关闭浏览器
    driver.quit()
