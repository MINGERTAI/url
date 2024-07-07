import datetime
from gettext import find
import json
import os
import requests
import hashlib
import sys
from cls import LocalFile
from cls import NetFile


def download_file():
    """
    从指定 URL 下载文件并保存到本地路径。
    """
    try:
        # 发送 HTTP GET 请求
        url = "https://raw.githubusercontent.com/aliluya1977/TVBox/master/shg.json"
        #response = request.get(url)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        # 检查请求是否成功
        response.raise_for_status()

        tvbox = response
        spare = ''
        for j in tvbox.split('\n'):
            try:
                if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 == -1:
                    # 过滤重复的电影网站
                    if (spare).find(j) > -1:
                        continue
                    spare += '\r\n' + j
                    
            except Exception as ex:
                LocalFile.write_LogFile(str(ex) + j)
        
        content =  spare
        LocalFile.write_LocalFile('./out/11.txt', content)
        print('读取并删除:./out/11.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile(str(ex))
