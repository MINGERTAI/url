import requests
from urllib.parse import quote

# 为了处理可能的URL编码问题，我们使用quote函数对URL进行编码
base_url = "http://tvbox.王二小放牛娃.xyz"
encoded_url = quote(base_url, safe=':/')

# 设置请求头，模仿浏览器的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

def get_website_content(url):
    try:
        response = requests.get(url, headers=headers)
        # 检查状态码是否为200，表明请求成功
        if response.status_code == 200:
            try:
                # 尝试将响应内容解析为JSON
                data = response.json()
                print("获取的JSON数据：", data)
            except ValueError:
                # 如果响应内容不是JSON格式，打印文本内容的前100个字符
                print("响应内容不是JSON格式，内容预览：", response.text[:100])
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"请求过程中发生错误：{str(e)}")

get_website_content(encoded_url)
