import datetime
from gettext import find
import json
import os
import requests
import sys
from cls import LocalFile
from cls import NetFile

# 获取传递的参数
try:
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)

def download_file(url, save_path):
    """
    从指定 URL 下载文件并保存到本地路径。
    """
    try:
        # 发送 HTTP GET 请求
        response = request.get(url)
        
        # 检查请求是否成功
        response.raise_for_status()
        
        # 创建保存路径的目录（如果不存在）
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    except request.exceptions.HTTPError as http_err:
        print(f"HTTP 错误: {http_err}")
    except Exception as err:
        print(f"其他错误: {err}")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/aliluya1977/TVBox/master/shg.json"
    
    download_file(url, save_path)
    
if menu == 'tvbox':
    try:
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
