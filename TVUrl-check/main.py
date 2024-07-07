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
            # 转换响应的 JSON 数据为字符串
            tvbox = response.json()
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
   
            # 将处理后的内容转换为JSON字符串
            content = ',\n'.join(json.dumps(item, ensure_ascii=False) for item in spare)
            LocalFile.write_LocalFile('./out/10.txt', content)
            print('读取并删除: ./out/10.txt 已更新。')
    
    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")

# 脚本的主逻辑
if __name__ == "__main__":
    download_file()
