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
# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if menu == 'tvbox':
tvlist = LocalFile.read_LocalFile("./res/tvlist.json")
    list1 = tvlist.split('\n')
    list1 = ListFile.get_list_sort(list1)
    print('Get-tvbox.json: \n' + str(len(list1)))

    boxurl = ''
    boxsites = ''
    allonesite = ''
    ii = 0
    iii = 0
    for i in list1:
        ii += 1
        print('\nNodes-List-OneNodeList:\n' + i)
        if(i == ''):
            continue
        else:
            osite = json.loads(i)
            osite_uptime = osite['uptime']
            osite_upmd5 = osite['upmd5']
            osite_tvurl = osite['tvurl']
            osite_size = osite['size']
        if(boxurl.find(osite_tvurl) == -1):
            try:
                newboxurl = osite_tvurl.replace('<yyyy>', datetime.datetime.now().strftime('%Y'))
                newboxurl = newboxurl.replace('<mm>', datetime.datetime.now().strftime('%m'))
                newboxurl = newboxurl.replace('<dd>', datetime.datetime.now().strftime('%d'))
                print('Get node link on sub ' + newboxurl)
                requests.adapters.DEFAULT_RETRIES = 3 # 增加重连次数
                s = requests.session()
                s.keep_alive = False # 关闭多余连接
                s.verify = False
                rq = s.get(newboxurl, timeout=(240, 120)) #连接超时 和 读取超时
                # rq = s.get(newboxurl, keep_alive=False, verify=False, timeout=(240, 120)) #连接超时 和 读取超时
                # rq.encoding = 'utf-8'
                if (rq.status_code != 200 and rq.status_code != 301 and rq.status_code != 302):
                    print('[GET Code {}] Download sub error on link: '.format(rq.status_code) + osite_upurl)
                    boxurl = boxurl + '\n' + i
                    continue
                # boxsites = (rq.content).decode('utf-8', 'ignore') # 可用
                # print(str(isinstance(rq.text, basestring)))
                # print(str(chardet.detect(rq.text)))
                if(rq.encoding != None):
                    boxsites = rq.text.encode(rq.encoding).decode('utf-8')
                else:
                    boxsites = rq.text.encode('utf-8') #unicode -> str
                    boxsites = boxsites.decode('utf-8') #str -> unicode
                boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').replace('\ufeff', '').strip('\n')
                if (boxsites != '' and osite_upmd5 != hashlib.md5(boxsites.encode('utf-8')).hexdigest()):
                    osite['upmd5'] = hashlib.md5(boxsites.encode('utf-8')).hexdigest()
                    if (osite_tvurl.find('k51qzi5uqu5dgc33fk7pd3093uw5ouejcyhwicv6gtfersoetui51qxq62zn5a') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1453)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax/index') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1097)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('out/node') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=731)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('vpei') > -1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    #elif (ii > 115):
                    #    osite['uptime'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        osite['uptime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    osite['size'] = len(boxsites)
                    i = json.dumps(osite)
                    print('UpdateTime:' + osite['uptime'] + ' boxsites-len:' + str(len(boxsites)))
                    # if(IsValid.isBase64(boxsites)):
                    #     boxsites = StrText.get_str_base64(boxsites) # Base64格式化
                    #     boxsites = base64.b64decode(boxsites).decode('utf-8')
                    #     print('Url-All-Nodes-is-Base64:' + newboxurl)
                    # else:
                    #     print('Url-All-Nodes-no-Base64:' + newboxurl)
                    allonesite = ''
                    if (osite['type'] == 'tlive'):
                        alltv = boxsites #NetFile.url_to_str(osite_tvurl, 240, 240)
                        
                        typename = ''
                        for onetv in alltv.split('\n'):
                            try:
                                onetv = onetv.rstrip('\r').replace(' ','')
                                if(onetv != ''):
                                    if(onetv.find(',#genre#') > -1):
                                        typename = onetv.split(',')[0]
                                        if(typename.find('韩') > -1 or typename.find('韩国') > -1):
                                            typename = '韩国频道'
                                        elif(typename.find('cctv') > -1 or typename.find('央视') > -1):
                                            typename = '央视频道'
                                        elif(typename.find('卫视') > -1):
                                            typename = '卫视频道'
                                    elif(onetv.find(',') > -1 and onetv.find('://') > -1):
                                        tvname = onetv.split(',')[0]
                                        tvurl = onetv.split(',')[1]
                                        #obj字典对象为新增内容
                                        # .encode('utf-8') #unicode -> str
                                        # .decode('utf-8') #str -> unicode
                                        obj = {"typename": "" + typename.encode('utf-8').decode('utf-8') + "","tvname": "" + tvname.encode('utf-8').decode('utf-8') + "","tvmd5": "" + hashlib.md5(tvurl.encode('utf-8')).hexdigest() + "","tvurl": "" + tvurl + ""}
                                        #write_json(obj)
                                        print(obj)
                                        # obj = json.dumps(obj, encoding='utf-8', ensure_ascii=False)
                                        print(str(obj))
                                        print(type(obj))
                                        # dictinfo = json.loads(obj)
                                        fjson = './res/tvlist.json'
                                        with open(fjson, 'r') as f:
                                            content = json.load(f)     
                                                                
                                        # axis = {"axis":[22, 10, 11]}
                                        content.append(obj)
                                        
                                        print(type(content))
                                        with open(fjson, 'w') as f_new:
                                            json.dump(content, f_new, indent=4, ensure_ascii=True)
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-205-Exception:' + str(ex) + '\nonesite:\n' + onetv)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-272-main-Exception:' + str(ex) + '\nosite_tvurl:\n' + osite_tvurl)
            boxurl = boxurl + '\n' + i
    # 去除重复项目
    # write_json()
    # 将节点更新时间等写入配置文件
    if (boxurl.find('uptime') > -1):
        LocalFile.write_LocalFile('./res/list.json', boxurl.strip('\n'))
    print('Line-238:tvbox.json已更新，共更新网址[' + str(iii) + ']。')
    #print('Url-All-Clash-To-Mixed-Nodes:\n' + allonesite)


    tvlists = []
    with open('./res/tvlist.json', 'r', encoding='utf-8') as f:
        tvlists = json.load(f)
    num_item = len(tvlists)
    alltv = ''
    oldtypename = ''
    for ii in alltypename.split('\n'):
        for i in range(num_item):
            try:
                typename = tvlists[i]['typename'].decode("unicode-escape")
                tvname = tvlists[i]['tvname'].decode("unicode-escape")
                tvurl = tvlists[i]['tvurl'].decode("unicode-escape")
                if(tvname.find(ii) == -1 or typename == ii):
                    if(ii == oldtypename):
                        alltv += '\r\n' + typename + ',' + tvurl
                    else:
                        alltv += '\r\n\r\n' + typename + ',#genre#'
                # tvname = load_dict[i]['tvname']
                # tvmd5 = load_dict[i]['tvmd5']
                # tvurl = load_dict[i]['tvurl']
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-264-Exception:' + str(ex) + '\nonesite:' + i)
    alltv = alltv.strip('\n').encode('utf-8')
    # allboxs.json = base64.b64encode(boxsites.strip('\n').encode('utf-8')).decode('utf-8')
    LocalFile.write_LocalFile('./out/all', alltv)
    print('Line-293-Node整理成功，共有记录' + str(iii) + '条。')
