import requests
import json

def fetch_and_save_json(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers)

  if 'application/json' in response.headers.get('Content-Type'):
      try:
          data = response.json()
          # 后续处理...
      except json.JSONDecodeError:
          print("获取的数据无法解析为JSON。")
  else:
      print("响应的内容类型不是application/json。")

        # 检查状态码
        if response.status_code == 200:
            try:
                # 尝试解析JSON数据
                data = response.json()
                # 保存到文件
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                print(f"数据已成功保存到{output_file}")
            except json.JSONDecodeError:
                print("获取的数据不是有效的JSON格式。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except requests.exceptions.RequestException as e:
        # 处理请求错误（如连接问题）
        print(f"请求错误：{e}")

# 替换成您的目标URL
url = "http://tvbox.王二小放牛娃.xyz"
output_file = "test.json"

fetch_and_save_json(url, output_file)
