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
            tvbox = json.dumps(response.json())
            spare = ''
            for j in tvbox.split('\n'):
                try:
                    if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1:
                        # 过滤重复的电影网站
                        if spare.find(j) > -1:
                            continue
                        spare += '\r\n' + j
                except Exception as ex:
                    LocalFile.write_LogFile(f"解析行时出错: {str(ex)} 行内容: {j}")
   
            content = spare
            #LocalFile.write_LocalFile('./out/10.txt', content)
            #print('读取并删除: ./out/10.txt 已更新。')
            with open("./out/10.txt","wb") as f:
                f.write(content,ensure_ascii=False)
    
    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")

# 脚本的主逻辑
if __name__ == "__main__":
    download_file()
