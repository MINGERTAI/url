import datetime
import json
import os
import requests
import sys
from cls import LocalFile

def download_file():
    """
    从指定 URL 下载文件并保存到本地路径。
    """
    try:
        # 发送 HTTP GET 请求
        url = "https://raw.githubusercontent.com/aliluya1977/TVBox/master/shg.json"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # 检查请求是否成功
        response.raise_for_status()

        # 解析 JSON 内容
        tvbox = response.text
        spare = ''
        
        # 分行处理 JSON 内容
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
        LocalFile.write_LocalFile('./out/12.txt', content)
        print('读取并删除:./out/12.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")

if __name__ == "__main__":
    download_file()
