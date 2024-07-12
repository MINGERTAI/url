from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# 配置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# 启动 Chrome 浏览器
driver = webdriver.Chrome(options=chrome_options)

# 打开解密网站
driver.get("http://www.xn--sss604efuw.com/jm/")

# 找到输入框，输入目标 URL
input_box = driver.find_element(By.ID, "url")  # 需要根据实际的 HTML 元素属性修改
input_box.send_keys("http://tvbox.王二小放牛娃.xyz")

# 点击解密按钮
decrypt_button = driver.find_element(By.ID, "placeholder")  # 需要根据实际的 HTML 元素属性修改
decrypt_button.click()

# 等待解密完成
time.sleep(3)  # 根据实际情况调整等待时间

# 点击复制按钮
copy_button = driver.find_element(By.ID, "copy-button")  # 需要根据实际的 HTML 元素属性修改
copy_button.click()

# 获取剪贴板内容
# 在无头浏览器中无法直接获取剪贴板内容，这里假设解密后的内容显示在页面上的某个元素中
decrypted_content = driver.find_element(By.ID, "decrypted-content").text  # 需要根据实际的 HTML 元素属性修改

# 将内容保存到文件
with open("out/xy.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_content)

# 关闭浏览器
driver.quit()
