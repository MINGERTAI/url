from selenium import webdriver

# 指定WebDriver的路径（以ChromeDriver为例）
driver_path = 'path/to/your/chromedriver'

# 创建WebDriver实例
driver = webdriver.Chrome(driver_path)

# 打开URL
driver.get("http://tvbox.王二小放牛娃.xyz")

# 等待页面加载完成（根据实际情况，可能需要等待一段时间或等待某个元素出现）
driver.implicitly_wait(10)  # 示例：等待10秒

# 获取页面源代码
page_source = driver.page_source

# 在此处，您可以使用page_source进行进一步处理，比如解析HTML，提取数据等

# 关闭浏览器
driver.quit()
