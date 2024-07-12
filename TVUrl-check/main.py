from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
input_box = driver.find_element(By.ID, "url")
input_box.send_keys("http://tvbox.王二小放牛娃.xyz")

# 点击解密按钮
decrypt_button = driver.find_element(By.XPATH, "//button[contains(text(),'解密')]")
decrypt_button.click()

# 等待解密完成
time.sleep(5)  # 根据实际情况调整等待时间

# 点击复制按钮
copy_button = driver.find_element(By.XPATH, "//button[contains(text(),'复制')]")
copy_button.click()

# 获取解密后的内容
decrypted_content = driver.find_element(By.ID, "result").get_attribute("value")

# 将内容保存到文件
with open("out/xy.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_content)

# 关闭浏览器
driver.quit()
