import base64
import datetime
from gettext import find
import hashlib
import json
import os
import requests
import sys
from cls import IsValid
from cls import LocalFile
from cls import ListFile
from cls import NetFile
from cls import PingIP
from cls import StrText

# 获取传递的参数
try:
    # 0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)

resurl = NetFile.url_stat('https://raw.githubusercontent.com/qist/tvbox/master/dianshi.json', 60, 60)

# 配置信息和同步本地需要更新的资源文件
resurl = 'https://raw.githubusercontent.com/qist/tvbox/master/dianshi.json'

#对程序的基本信息进行下载更新，下载IPFS网关信息和过滤列表信息
if(menu == 'init'):
    filename = 'dianshi.json|dianshi.json'
    for i in filename.split('|'):
        try:
            File = NetFile.url_to_str(resurl + '' + i, 240, 240)
            if(len(File) > 10240):
                LocalFile.write_LocalFile('./out/' + i, File.strip('\n')) 
                print('Get-File-is-True:' + resurl + '' + i + ' FileSize:' + str(len(File)))
        except Exception as ex:
            print('Get-File-is-False:' + resurl + '' + i + '\n' + str(ex))

def write_json():
    '''
    # 写入/追加json文件
    :param obj:
    :return:
    '''
    post=set()
    fp=[]
    for p in range(len(json)):
            if json[p]['text'] not in post:  #如果set中没有这个值（set特性是不能重复）
                    fp.append(json[p])  #fp数组将这个不重复的值存进
                    post.add(json[p]['text'])  #set存进这个不重复的值，为了后面判断是否重复做准备
                    print(json[p])
                    print(post)
                    print(json[p]['text'])
    print(fp)

    #首先读取已有的json文件中的内容
    post=set()
    item_list = []
    alltypename = ''
    with open('./out/tvlist.json', 'r', encoding='utf-8') as f:
        load_dict = json.load(f)
        num_item = len(load_dict)
        for i in range(num_item):
            try:
                if load_dict[i]['tvmd5'] not in post:   #如果set中没有这个值（set特性是不能重复）
                    post.add(str(load_dict[i]['tvmd5']))  #set存进这个不重复的值，为了后面判断是否重复做准备
                    typename = load_dict[i]['typename']
                    if(alltypename.find(typename) == -1):
                        alltypename = alltypename + '\r\n' + typename
                    tvname = load_dict[i]['tvname']
                    tvmd5 = load_dict[i]['tvmd5']
                    tvurl = load_dict[i]['tvurl']

                    item_dict = {'typename':typename, 'tvname':tvname,'tvmd5':tvmd5, 'tvurl':tvurl}
                    item_list.append(item_dict)
                    item_list.append(load_dict[i])
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-87-Exception:' + str(ex))
            
    #读取已有内容完毕
    #将新传入的dict对象追加至list中
    item_list.append(obj)
    #将追加的内容与原有内容写回（覆盖）原文件
    with open('./out/tvlist.json', 'w', encoding='utf-8') as f2:
        json.dump(item_list, f2, ensure_ascii=False)
    LocalFile.write_LocalFile('./out/typename.txt', alltypename.lstrip('\r\n'))
