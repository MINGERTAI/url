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
        tvbox = tvbox.replace('//{','\n{')
        new_string = tvbox.strip()
        spare = ''
        for j in new_string.split('\n'):
            try:
                if(j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 == -1):
                    j = j.strip(',')
                    if(len(j.split('}')) > len(j.split('{'))):
                        j = j.strip(',')[:-1].strip(',')
                    tv = json.loads(j)                     
                    # 过滤重复的电影网站
                    if((addtv + spare + nsfw).find(j) > -1):
                        continue
                    # 过滤重复Key的电影网站
                    if((addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1):
                        spare += '\r\n' + j + ','
                        continue
                    # 分类去重
                    id = tv['type']
                    if(id == 3):
                        if('ext' in tv.keys()):
                            ext = tv['ext']
                            if((addtv + nsfw).find(ext) > -1):
                                continue
                        else:
                            # 未配置Ext信息，让api值唯一
                            if((addtv + nsfw).find('"api":"' + tv['api'] + '"') > -1):
                                continue
                    else:
                        spare += '\r\n' + j
                else:
                    print('Main-Line-91-not-tvsite-url:' + j)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)


        LocalFile.write_LocalFile('./out/1121.txt', '\r\n' spare'\r\n],')
    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
