import requests
import json

# 假设的目标URL
target_url = 'http://肥猫.com'

# 发起请求
response = requests.get(target_url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析JSON数据
    data = response.json()
    
    # 假设我们想要打印出解析后的JSON中的特定信息
    print(json.dumps(data, indent=4, ensure_ascii=False))
else:
    print(f"请求失败，状态码：{response.status_code}")

    with open('1.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
