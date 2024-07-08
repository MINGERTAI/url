#!/usr/bin/env python3

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
    menu = 'check'
print('menu: ' + menu)

# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if(menu == 'check'):
    try:
        if(os.path.exists('./fatcat.json')):
            tvbox = LocalFile.read_LocalFile('./fatcat.json').replace('\r','').replace('\n\n','\n')
        spare = ''
        new_string = tvbox.strip()
        new1_string = new_string.replace('//{','\n{')
        for j in new1_string.split('\n'):
            try:
                if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 == -1:
                    # 过滤重复的电影网站
                    if (spare).find(j) > -1:
                        continue
                    spare += '\r\n' + j
                    
            except Exception as ex:
                LocalFile.write_LogFile(str(ex) + j)
        
        content = spare
        LocalFile.write_LocalFile('./out/1102.txt', content)
        print('读取并删除&写入到:./out/1102.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile(str(ex))
