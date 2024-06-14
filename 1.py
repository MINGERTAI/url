import requests
import json

# 目标URL
url = "http://tvbox.王二小放牛娃.xyz"

try:
    # 发起GET请求
    response = requests.get(url)

    # 检查响应状态码，200表示成功
    if response.status_code == 200:
        # 解析响应内容为JSON
        data = response.json()

        # 将获取到的JSON数据保存到test.json文件中
        with open('test.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print("数据已成功保存到test.json文件中。")
    else:
        print("无法访问网页，状态码：", response.status_code)
except Exception as e:
    print("发生错误：", e)
