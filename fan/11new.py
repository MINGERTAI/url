import datetime
import json
import os
import re
import sys
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}
from cls import LocalFile, NetFile

# 获取传递的参数
try:
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)
resurl = NetFile.url_stat('https://raw.githubusercontent.com/aliluya1977/TVBox/master/shg.json', 60, 60)
ustat = 'https://raw.githubusercontent.com/aliluya1977/TVBox/master/shg.json'
# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if menu == 'tvbox':
    try:
        tvbox = 'ustat'
        addtv = ''
        nsfw = ''
        spare = ''
        for j in tvbox.split('\n'):
            try:
                if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 == -1:
                    j = j.strip(',')
                    if len(j.split('}')) > len(j.split('{')):
                        j = j.strip(',')[:-1].strip(',')
                    tv = json.loads(j)
                    # 过滤重复的电影网站
                    if (addtv + spare + nsfw).find(j) > -1:
                        continue
                    # 过滤重复Key的电影网站
                    if (addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1:
                        spare += '\r\n' + j + ','
                        continue
                    else:
                        spare += '\r\n' + j + ','                
                    if tv['name'].find('*') > -1:
                        nsfw += '\r\n' + j + ','
                    elif j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1:
                        addtv += '\r\n' + j + ','
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)
        
        content = addtv + '\r\n' + nsfw + '\r\n' + spare
        LocalFile.write_LocalFile('./out/11.txt', content)
        print('Line-96:./out/11.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
