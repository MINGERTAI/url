import requests
import json

# 假设的目标URL
target_url = 'http://肥猫.com'  # 请确保这是一个返回JSON响应的有效URL

# 发起请求
response = requests.get(target_url)

# 检查请求是否成功
if response.status_code == 200:
    try:
        # 尝试解析JSON数据
        data = response.json()
        
        # 假设我们想要打印出解析后的JSON中的特定信息
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("响应的内容不是有效的JSON格式。")
else:
    print(f"请求失败，状态码：{response.status_code}")
    # 使用 response.text 而不是未定义的变量 content
    with open('1.json', 'w', encoding='utf-8') as f:
        f.write(response.text)  # 将响应正文写入文件
