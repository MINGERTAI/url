import requests
import json
import base64

# 目标URL
url = "http://tvbox.王二小放牛娃.xyz"

# 发送GET请求
response = requests.get(url)

# 检查响应状态码确保请求成功
if response.status_code == 200:
    # 尝试获取JSON数据
    try:
        data = response.json()
        
        # 将JSON对象转换为字符串
        json_string = json.dumps(data)
        
        # 将字符串转换为字节
        json_bytes = json_string.encode('utf-8')
        
        # 进行Base64编码
        encoded_bytes = base64.b64encode(json_bytes)
        
        # 进行Base64解码
        decoded_bytes = base64.b64decode(encoded_bytes)
        
        # 将解码后的字节转换为字符串
        decoded_json_string = decoded_bytes.decode('utf-8')
        
        # 将字符串转换回JSON对象
        decoded_data = json.loads(decoded_json_string)
        
        # 将解码后的JSON数据保存到test.json文件中
        with open('test.json', 'w', encoding='utf-8') as file:
            json.dump(decoded_data, file, ensure_ascii=False, indent=4)
        
        print("数据已成功保存到test.json文件中。")
    except json.JSONDecodeError as e:
        print("获取的数据不是有效的JSON格式：", e)
else:
    print("请求失败，状态码：", response.status_code)
