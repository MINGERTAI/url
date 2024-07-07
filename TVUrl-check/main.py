#添加 headers：在请求头中添加 User-Agent 以避免某些服务器的拒绝访问。
#response.text：使用 response.text 获取响应内容。
#精确条件：确保只有完全匹配 "key":、"name": 和 "type": 的行才被处理。
#异常处理：在每行处理过程中添加异常处理，并记录日志。
#通过这些修改，脚本将从指定 URL 下载 shg.json 文件，提取包含 "key":、"name": 和 "type": 的行，并将结果写入到 ./out/11.txt 文件中
import datetime
import json
import os
import requests
import sys
from cls import LocalFile

import base64
import hashlib
import json
import hashlib
import configparser
import re

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
            data = response.json() 
            
            tvbox = json.dump(data, ensure_ascii=False)
            spare = ''
            for j in tvbox.split('\n'):
                try:
                    if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1:
                        if spare.find(j) > -1:
                            continue
                        spare += '\r\n' + j
                except Exception as ex:
                        LocalFile.write_LogFile(f"解析行时出错: {str(ex)} 行内容: {j}")
   
        content = spare
        LocalFile.write_LocalFile('./out/10.txt', content)
        print('读取并删除:./out/10.txt已更新。')
    
    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")
# 脚本的主逻辑
if __name__ == "__main__":
    download_file()
