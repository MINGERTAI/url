import json
import requests
from cls import LocalFile  # 假设这是你自定义的本地文件操作类

headers = {'User-Agent': 'okhttp/3.15'}

def download_file():
    """
    从指定 URL 下载文件并保存到本地路径。
    """
    try:
        # 发送 HTTP GET 请求
        url = "http://肥猫.com"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 尝试解析 JSON 数据
            try:
                tvbox = response.json()
            except json.JSONDecodeError:
                LocalFile.write_LogFile("响应数据不是有效的 JSON 格式")
                return

            # 检查 tvbox 是否为列表
            if not isinstance(tvbox, list):
                LocalFile.write_LogFile("响应数据不是列表格式")
                return

            print(f"原始数据：{tvbox}")

            spare = []
            for item in tvbox:
                try:
                    if 'key' in item and 'name' in item and 'type' in item:
                        # 过滤重复的电影网站
                        if any(existing_item['key'] == item['key'] for existing_item in spare):
                            continue
                        spare.append(item)
                except Exception as ex:
                    LocalFile.write_LogFile(f"解析项目时出错: {str(ex)} 项目内容: {item}")

            # 检查 spare 列表的内容
            print(f"过滤后的数据：{spare}")

            # 将处理后的内容转换为 JSON 字符串
            content = ',\n'.join(json.dumps(item, ensure_ascii=False) for item in spare)
            LocalFile.write_LocalFile('./out/10.txt', content)
            print(f'读取并删除: ./out/10.txt 已更新。内容：{content}')
    
    except requests.exceptions.RequestException as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")

# 脚本的主逻辑
if __name__ == "__main__":
    download_file()
