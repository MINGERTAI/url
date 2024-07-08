import json
from cls import LocalFile
import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}


def get_dianshi():

    try:
        # 发送 HTTP GET 请求
        url = "https://raw.githubusercontent.com/ne7359/url/main/out/new_test.txt"
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
        LocalFile.write_LocalFile('./out/11new.txt', content)
        print('读取并删除:./out/new.txt已更新。')
    
    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")
get_dianshi()
