
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
 
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
self.driver = webdriver.Chrome(chrome_options=options)

try:
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

    # 删除原有的 ./out/new.txt 文件（如果存在）
    output_path = "./out/new.txt"
    if os.path.exists(output_path):
        os.remove(output_path)
        print('已删除原有的 ./out/new.txt 文件。')

    # 将内容保存到文件
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(decrypted_content)

    print(f'解密内容已保存到 {output_path}')

finally:
    # 关闭浏览器
    driver.quit()
