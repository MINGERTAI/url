import requests
from bs4 import BeautifulSoup
import pyautogui
import time

# 解密网站地址
decrypt_url = 'http://www.xn--sss604efuw.com/jm/'

# 需要解密的网址
target_url = 'http://tvbox.王二小放牛娃.xyz'

# 请求解密页面
response = requests.get(decrypt_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 提取解密表单中的隐藏字段或必要的数据
# 这里假设你需要提取的字段在表单中
hidden_inputs = soup.find_all('input', type='hidden')
form_data = {input.get('name'): input.get('value') for input in hidden_inputs}

# 添加目标网址到表单数据中
form_data['url'] = target_url

# 提交解密请求
response = requests.post(decrypt_url, data=form_data)

# 解析解密后的结果
soup = BeautifulSoup(response.text, 'html.parser')
result = soup.find('textarea', id='result').text

# 将结果写入文件
output_file_path = 'out/xy.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(result)

# 模拟点击复制操作
# 这里假设复制功能在浏览器上已经可以通过一些快捷键完成
pyautogui.hotkey('ctrl', 'a')  # 选择全部
time.sleep(1)
pyautogui.hotkey('ctrl', 'c')  # 复制到剪贴板
time.sleep(1)

# 确保复制完毕
print(f"解密结果已保存到 {output_file_path}")
