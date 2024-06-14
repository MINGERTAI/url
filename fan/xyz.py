import requests
import json

# 目标网址
url = "http://lige.unaux.com/?url=http://tvbox.王二小放牛娃.xyz&i=1"

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_json_data(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text  # 获取响应内容
            # 打印内容以调试
            with open('response_content.txt', 'w', encoding='utf-8') as file:
                file.write(content)
            
            # 从内容中解析JSON数据
            try:
                data = json.loads(content)
                # 保存JSON数据到文件
                json_file_path = 'data.json'
                with open(json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到 {json_file_path}")
            except json.JSONDecodeError:
                print("无法解析JSON数据。请检查响应内容。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 调用函数
get_json_data(url)
