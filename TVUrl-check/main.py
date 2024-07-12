from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

# 解密网站地址
decrypt_url = 'http://www.xn--sss604efuw.com/jm/'

# 需要解密的网址
target_url = 'http://tvbox.王二小放牛娃.xyz'

# 设置WebDriver
driver = webdriver.Chrome()  # 或使用其他浏览器驱动程序，如 Firefox、Edge 等
driver.get(decrypt_url)

# 等待页面加载
time.sleep(2)

# 找到输入框并输入网址
input_box = driver.find_element(By.ID, 'url_input')  # 假设输入框的ID是'url_input'
input_box.send_keys(target_url)
input_box.send_keys(Keys.RETURN)  # 提交表单

# 等待解密完成
time.sleep(5)  # 根据实际情况调整等待时间

# 获取解密结果
result_area = driver.find_element(By.ID, 'result')  # 假设结果区域的ID是'result'
result = result_area.text

# 确保保存目录存在
output_dir = 'out'
os.makedirs(output_dir, exist_ok=True)

# 将结果写入文件
output_file_path = os.path.join(output_dir, 'xy.txt')
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(result)

print(f"解密结果已保存到 {output_file_path}")

# 关闭浏览器
driver.quit()
