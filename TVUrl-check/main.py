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

    try:
        if os.path.exists('./out/123.json'):
            tvbox = LocalFile.read_LocalFile('./out/123.json') #.replace('\r', '').replace('\n\n', '\n')
        else:
            tvbox = LocalFile.read_LocalFile('./out/123.json') #.replace('\r', '').replace('\n\n', '\n')

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
                    #tv = json.loads(j)
                    # 过滤重复的电影网站
                    if (addtv + spare + nsfw).find(j) > -1:
                        continue
                    spare += '\r\n' + j + ','
                    content = addtv + '\r\n' + nsfw + '\r\n' + spare
                    LocalFile.write_LocalFile('./out/11.txt', content)
                    print('Line-96:./out/11.txt已更新。')
                    
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
                #LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)
        
        #content = addtv + '\r\n' + nsfw + '\r\n' + spare
        #LocalFile.write_LocalFile('./out/11.txt', content)
        #print('Line-96:./out/11.txt已更新。')

    #except Exception as ex:
        #LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
