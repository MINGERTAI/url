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
    # 0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)

resurl = NetFile.url_stat('https://github.com/qist/tvbox/blob/master/', 60, 60)

# 配置信息和同步本地需要更新的资源文件
resurl = 'https://github.com/qist/tvbox/blob/master/'

#对程序的基本信息进行下载更新，下载IPFS网关信息和过滤列表信息
if(menu == 'init'):
    tvboxlur = 'dianshi.json'
    tvbox = LocalFile.read_LocalFile('tvboxlur').replace('\r', '').replace('\n\n', '\n')
    addtv = ''
    nsfw = ''
    spare = ''
    tvbox = tvbox.replace('//{', '\n{')
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
    LocalFile.write_LocalFile('./out/123.txt', content)
    print('Line-96:./out/pull.txt已更新。')
    #content = remove_line(content)
    #LocalFile.write_LocalFile('./out/json.txt', content)
    #print('Line-96:./out/json.txt已更新。')

except Exception as ex:
    LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
