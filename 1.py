import requests
import json

# 目标URL
url = "http://tvbox.王二小放牛娃.xyz"

headers = {
    'Accept': 'application/json',  # 明确指定希望接收JSON格式的响应
}

try:
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 检查响应内容是否为空
        if response.content:
            # 尝试解析JSON
            try:
                data = response.json()
                # 将获取到的JSON数据保存到test.json文件中
                with open('test.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                print("数据已成功保存到test.json文件中。")
            except json.JSONDecodeError as json_err:
                print("解析JSON时发生错误：", json_err)
                # 打印出响应内容的前500个字符，以帮助调试
                print("响应内容（前500字符）：", response.text[:500])
        else:
            print("响应内容为空。")
    else:
        print("无法访问网页，状态码：", response.status_code)
except Exception as e:
    print("请求过程中发生错误：", e)
