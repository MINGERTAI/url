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

# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if menu == 'tvbox':
    try:
        if os.path.exists('./c.json'):
            tvbox = LocalFile.read_LocalFile('./c.json')   #.replace('\r', '').replace('\n\n', '\n')
        else:
            tvbox = LocalFile.read_LocalFile('./c.json')  #.replace('\r', '').replace('\n\n', '\n')

        LocalFile.write_LocalFile('./out/123.txt', tvbox)
        print('Line-96:./out/123.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
