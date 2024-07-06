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

if menu == 'tvbox':
    url = "https://raw.githubusercontent.com/ne7359/tvurl/main/jsm.json"
    try:
        tvbox = requests.get(url)
        tvbox.raise_for_status()
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
