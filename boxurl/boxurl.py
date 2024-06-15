#!/usr/bin/env python3

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
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'init'
print('menu: ' + menu)

# 本菜单暂时无效
if(menu == 'update'):
    oldexpire = LocalFile.read_LocalFile("./boxurl/res/r_sites_err.txt")
    nettvexpire = LocalFile.read_LocalFile("./boxurl/res/expire.txt")
    # 本地所有失效链接合并去重存储至expires.txt
    allexpire = oldexpire.strip('\n') + '\n' + nettvexpire.strip('\n')
    expires = ''
    expirecount = len(allexpire.split('\n'))
    print('Get-oldexpire.txt: \n' + str(expirecount))
    for i in allexpire.split('\n'):
        if(expires.find(i) == -1):
            expires = expires + i + '\n'
    if(len(expires) > len(oldexpire)):
        LocalFile.write_LocalFile('./boxurl/res/r_sites_err.txt', expires.strip('\n')) 
    print('Get-expire.txt: \n' + str(len(expires)))

    tvlist = LocalFile.read_LocalFile("./boxurl/res/tvlist.json")
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
                                        fjson = './boxurl/res/tvlist.json'
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
        LocalFile.write_LocalFile('./boxurl/res/list.json', boxurl.strip('\n'))
    print('Line-238:tvbox.json已更新，共更新网址[' + str(iii) + ']。')
    #print('Url-All-Clash-To-Mixed-Nodes:\n' + allonesite)

    # 读取所有节点到allonesite新记录后面。
    alltypename = LocalFile.read_LocalFile("./boxurl/res/typename.txt").replace('\r','')
    tvlists = []
    with open('./boxurl/res/tvlist.json', 'r', encoding='utf-8') as f:
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
    LocalFile.write_LocalFile('./boxurl/out/all', alltv)
    print('Line-293-Node整理成功，共有记录' + str(iii) + '条。')


# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if(menu == 'upexpire'):
    r_sites_err = LocalFile.read_LocalFile("./boxurl/res/r_sites_err.txt")
    nettvexpire = LocalFile.read_LocalFile("./boxurl/res/expire.txt")
    nettvexpire = nettvexpire.strip('\n')
    # 处理临时数据和网络失效数据中vmess同一IP和端口过滤列表
    fakeip = LocalFile.read_LocalFile("./boxurl/res/fakeip.txt")
    newallexpire = ''
    for i in nettvexpire.split('\n'):
        try:
            if(i.find('://')>-1):
                i = StrText.get_str_btw((i + '/'), '://', '/', 0)
                if(fakeip.find(i) == -1):
                    newallexpire = newallexpire + '\n' + i
        except Exception as ex:
            LocalFile.write_LogFile('Main-Line-324-Exception:' + str(ex) + '\nexpire:' + i)
    # LocalFile.write_LocalFile('./boxurl/res/fakeip.txt', fakeip)
    
    # 本地所有失效链接合并去重存储至expires.txt
    allexpire = r_sites_err.strip('\n') + '\n' + newallexpire.strip('\n')
    expires = ''
    expirecount = len(allexpire.split('\n'))
    print('Get-oldexpire.txt: \n' + str(expirecount))
    for i in allexpire.split('\n'):
        if(expires.find(i) == -1):
            expires = expires + i + '\n'
    if(len(expires) > len(r_sites_err)):
        LocalFile.write_LocalFile('./boxurl/res/r_sites_err.txt', expires.strip('\n')) 
    print('Get-expire.txt: \n' + str(len(expires)))

if(menu == 'uptvbox'):
    tvlist = LocalFile.read_LocalFile("./boxurl/res/tvlist.json")
    print('Get-tvbox.json: \n' + str(len(tvlist.split('\n'))))
    #sub_link = []
    #for i in range(len(sub_url)):
    #    s_url = sub_url[i]
    boxurl = ''
    boxsites = ''
    allonesite = ''
    list1 = tvlist.split('\n')
    list1 = ListFile.get_list_sort(list1)
    ii = 0
    iii = 0
    # 获取默认值再添加后重写
    alllive = LocalFile.read_LocalFile("./boxurl/res/live.txt")
    r_parses = LocalFile.read_LocalFile("./boxurl/res/r_parses.txt")
    r_parses_err = LocalFile.read_LocalFile("./boxurl/res/r_parses_err.txt")
    tvlist = LocalFile.read_LocalFile("./boxurl/res/all")
    if(tvlist.find('"sites":[')>-1):
        tvlist = StrText.get_str_btw(tvlist, '"sites":[', '],', 0) + ','
    tvjar = ''
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
        # osite_tvurl = 'http://vpei.vmess.com/368a78117708e614f481b0f9ecb5642d.txt'   取消vpn检测
        if(boxurl.find(osite_tvurl) == -1):
            try:
                newboxurl = osite_tvurl.replace('<yyyy>', datetime.datetime.now().strftime('%Y'))
                newboxurl = newboxurl.replace('<mm>', datetime.datetime.now().strftime('%m'))
                newboxurl = newboxurl.replace('<dd>', datetime.datetime.now().strftime('%d'))
                print('Get boxurl link on sub ' + newboxurl)
                boxsites = NetFile.url_to_str(newboxurl, 240, 120)
                boxsites = boxsites.replace(' ','')
                boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').replace('\ufeff', '').strip('\n')
                if (boxsites != '' and (osite_upmd5 != hashlib.md5(boxsites.encode('utf-8')).hexdigest() or osite_tvurl.find('/vpei/')>-1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax')>-1)):
                    # 写入文件
                    LocalFile.write_LocalFile('./boxurl/tmp/' + hashlib.md5(newboxurl.encode('utf-8')).hexdigest() + '.txt', boxsites)
                    osite['upmd5'] = hashlib.md5(boxsites.encode('utf-8')).hexdigest()
                    if (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1453)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax/index2') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=1097)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('out/node') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=731)).strftime("%Y-%m-%d %H:%M:%S")
                    elif (osite_tvurl.find('vpei') > -1 or osite_tvurl.find('k2k4r8n888sny0v16vyfxbjwqrk0vgvh9k84xixh5k6ejdywbdc509ax') > -1):
                        osite['uptime'] = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")

                    else:
                        osite['uptime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    osite['size'] = len(boxsites)
                    i = json.dumps(osite)
                    #　boxsites = boxsites.encode('utf-8').decode('utf-8', 'ignore').strip('\n')
                    print('UpdateTime:' + osite['uptime'] + ' boxsites-len:' + str(len(boxsites)))

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
                                        fjson = './boxurl/res/tvlist.json'
                                        with open(fjson, 'r') as f:
                                            content = json.load(f)     
                                                                
                                        # axis = {"axis":[22, 10, 11]}
                                        content.append(obj)
                                        
                                        print(type(content))
                                        with open(fjson, 'w') as f_new:
                                            json.dump(content, f_new, indent=4, ensure_ascii=True)
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-205-main-Exception:' + str(ex) + '\nosite_tvurl:\n' + onetv)
                    elif (osite['type'] == 'mixed'):
                        boxsites = boxsites.replace('\r','').replace('\n','').replace('\t','').replace('	','').replace(' ','')
                        tvjar = StrText.get_str_btw(boxsites, '"spider":"', '"', 0)
                        if(boxsites.find('"proxy://do=live&type=txt&ext=')>-1):
                            try:
                                onelive = base64.b64decode(StrText.get_str_btw(boxsites, 'proxy://do=live&type=txt&ext=', '"', 0)).decode('utf-8')
                                if(alllive.find(onelive) == -1):
                                    alllive = onelive + '\r\n' + alllive
                            except Exception as ex:
                                LocalFile.write_LogFile('Main-Line-488-Exception:\n' + str(ex))
                        if(boxsites.find('"parses":[') > -1 and boxsites.find('}],') > -1):
                            parses = StrText.get_str_btw(boxsites, '"parses":[', '}],', 0) + '}'
                            parses = parses.replace(' ','').replace('\r','').replace('\n','').replace('//{','{').strip('{').strip('}')
                            for oneparse in parses.split('},{'):        
                                try:
                                    if(oneparse[-3:] == '},}'):
                                        oneparse = oneparse[:-2]
                                    if(len(oneparse.split('{')) == len(oneparse.split('}'))): #指定字符数量-1
                                        oneparse = '{' + oneparse + '}'
                                        if(oneparse.find('"name":"') > -1 and oneparse.find('"url":"') > -1):
                                            onep = json.loads(oneparse)
                                            if(r_parses.find(onep['url']) == -1 and r_parses_err.find(onep['url']) == -1):
                                                if(oneparse.find('"ext":"') > -1):
                                                    r_parses = oneparse + ',' + '\r\n' + r_parses
                                                else:
                                                    r_parses += '\r\n' + oneparse + ','
                                    else:
                                        LocalFile.write_LogFile('Main-Line-457-boxurl:' + newboxurl + '\nparse:' + oneparse)
                                except Exception as ex:
                                    LocalFile.write_LogFile('Main-Line-459-Exception:\n' + str(ex) + '\n' + oneparse)
                        if(boxsites.find('"sites":[') > -1 and boxsites.find('}],') > -1):
                            boxsites = StrText.get_str_btw(boxsites, '"sites":[', '}],', 0) + '}'
                            for onetvurl in boxsites.split('},{'):
                                try:
                                    onetvurl = '{' + onetvurl + '}'
                                    onetvurl = onetvurl.replace('{{','{').replace('}}','}')
                                    osite = json.loads(onetvurl)
                                    if(osite['type'] == 1 or osite['type'] == 2):
                                        tvlist += onetvurl + ',\r\n'
                                    elif(osite['type'] == 3):
                                        if(onetvurl.find('"jar":"') == -1):
                                            tvlist += onetvurl.replace('}',',"jar":"' + tvjar + '"}') + ',\r\n'
                                        else:
                                            tvlist += onetvurl + ',\r\n'
                                    else:
                                        tvlist += onetvurl + ',\r\n'
                                except Exception as ex:
                                    LocalFile.write_LogFile('Main-Line-211-Exception:' + str(ex) + '\nonetvurl:\n' + onetvurl)
                        elif(boxsites.find('proxies:') > -1 and boxsites.find('proxy-groups:') == -1):
                            boxsites = ''
                iii += 1
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-530-Exception:' + str(ex) + '\nosite_tvurl:\n' + osite_tvurl)
            boxurl = boxurl + '\n' + i
    # tvlist = tvlist.replace(',"jar":"' + tvjar + '"','')
    tvlist = tvlist.replace(',"jar":"http://freed.yuanhsing.cf/TVBox/MaooXB2/XBiubiuLA4.jar"','')
    # 去除重复项目
    # write_json()
    # 将节点更新时间等写入配置文件
    if (boxurl.find('uptime') > -1):
        LocalFile.write_LocalFile('./boxurl/res/tvlist.json', boxurl.strip('\r\n'))
        print('Line-532:TvList.json已更新，共更新网址[' + str(iii) + ']。')

    LocalFile.write_LocalFile('./boxurl/out/all', tvlist.strip('\r\n'))
    LocalFile.write_LocalFile('./boxurl/res/live.txt', alllive)
    print('Line-535:/boxurl/res/live.txt已更新。')

    # 检测parses url 是否能正常访问
    parses = r_parses.replace(' ','').replace('\r','').replace('\n','').replace('//{','{').strip('{').strip('}')
    r_parses = '{"name":"解析聚合","type":3,"url":"Demo"},\r\n{"name":"Json并发","type":2,"url":"Parallel"},\r\n{"name":"Json轮询","type":2,"url":"Sequence"},'
    for oneparse in parses.split('},{'):        
        try:
            if(len(oneparse.split('}')) > len(oneparse.split('{'))):
                oneparse = oneparse.strip(',')[:-1].strip(',')
            oneparse = '{' + oneparse + '}'
            if(oneparse.find('"name":"') > -1 and oneparse.find('"url":"') > -1):
                onep = json.loads(oneparse)
                if(r_parses.find(onep['url']) == -1 and r_parses_err.find(onep['url']) == -1):
                    ustat = NetFile.url_stat(onep['url'], 60, 60)
                    if(ustat == 404 or ustat == 0):
                        r_parses_err += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + oneparse + ','
                    else:
                        r_parses += '\r\n' + oneparse + ','
        except Exception as ex:
            LocalFile.write_LogFile('Main-Line-496-Exception:\n' + str(ex) + '\n' + oneparse)
    LocalFile.write_LocalFile('./boxurl/res/r_parses.txt', r_parses.strip('\r\n'))
    print('Line-561:/boxurl/res/r_parses.txt已更新。')
    LocalFile.write_LocalFile('./boxurl/res/r_parses_err.txt', r_parses_err.strip('\r\n'))
    print('Line-563:/boxurl/res/r_parses_err.txt已更新。')

# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if(menu == 'check'):
    try:
        rename = LocalFile.read_LocalFile('./boxurl/res/rename.txt').replace('\r','').replace('\n\n','\n')
        if(os.path.exists('./boxurl/out/all')):
            tvbox = LocalFile.read_LocalFile('./boxurl/out/all').replace('\r','').replace('\n\n','\n')
        else:
            tvbox = LocalFile.read_LocalFile('./boxurl/res/all').replace('\r','').replace('\n\n','\n')
        r_sites_err = LocalFile.read_LocalFile("./boxurl/res/r_sites_err.txt")
        addtv = ''
        nsfw = ''
        spare = ''
        tvbox = tvbox.replace('//{','\n{')
        for j in tvbox.split('\n'):
            try:
                if(j != '' and j.find('"jar":"./') == -1 and j.find('"ext":"./') == -1 and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 and r_sites_err.find(j) == -1):
                    j = j.strip(',').replace('"type":0','"type":1')
                    if(len(j.split('}')) > len(j.split('{'))):
                        j = j.strip(',')[:-1].strip(',')
                    tv = json.loads(j)
                    # 检查自定义Jar文件是否存在
                    if('jar' in tv.keys()):
                        jar = tv['jar']
                        if(jar.find('http') == 0):
                            ustat = NetFile.url_stat(jar, 60, 60)
                            if(ustat == 404 or ustat == 0):
                                j = j.replace(',"jar":"' + jar + '"', '')
                    # 自定义电影网站名称
                    if(('name' in tv.keys()) and ('key' in tv.keys())):
                        if(rename.find(tv['key']) > -1):
                            newname = StrText.get_str_btw(rename.replace('\r',''), tv['key'] + ':', '\n', 0)
                            tv['name'] = newname
                            j = json.dumps(tv)                              
                    # 过滤重复的电影网站
                    if((addtv + spare + nsfw).find(j) > -1):
                        continue
                    # 过滤重复Key的电影网站
                    if((addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1):
                        spare += '\r\n' + j + ','
                        continue
                    # 分类去重
                    id = tv['type']
                    if(id == 1 or id == 4):
                        api = tv['api']
                        if((addtv + nsfw + r_sites_err).find(api) > -1):
                            continue
                        else:
                            if(api.find('http') == 0):
                                ustat = NetFile.url_stat(api, 60, 60)
                                if(ustat == 404 or ustat == 0):
                                    r_sites_err += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + j + ','
                                    continue
                    elif(id == 3):
                        if('ext' in tv.keys()):
                            ext = tv['ext']
                            if((addtv + nsfw + r_sites_err).find(ext) > -1):
                                continue
                            else:
                                if(ext.find('http') == 0):
                                    ustat = NetFile.url_stat(ext, 60, 60)
                                    if(ustat == 404 or ustat == 0):
                                        r_sites_err += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + j + ','
                                        continue
                        else:
                            # 未配置Ext信息，让api值唯一
                            if((addtv + nsfw + r_sites_err).find('"api":"' + tv['api'] + '"') > -1):
                                continue

                    else:
                        spare += '\r\n' + j + ','
                    
                    if(tv['name'].find('*') > -1):
                        nsfw += '\r\n' + j + ','
                    elif(j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1):
                        addtv += '\r\n' + j + ','
                else:
                    print('Main-Line-612-not-tvsite-url:' + j)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-614-Exception:' + str(ex) + '\ntvsite:' + j)
        
        LocalFile.write_LocalFile('./boxurl/res/r_sites_err.txt', r_sites_err.strip('\r\n'))
        print('Line-563:/boxurl/res/r_sites_err.txt已更新。')

        r_spider = LocalFile.read_LocalFile("./boxurl/res/r_spider.txt")
        r_spider = '{''\r\n' + r_spider
        r_lives = LocalFile.read_LocalFile("./boxurl/res/r_lives.txt")
        r_parses = LocalFile.read_LocalFile("./boxurl/res/r_parses.txt")
        r_parses = '\r\n\r\n"parses":[\r\n' + r_parses.replace('},\n{','},\r\n{').strip(',') + '\r\n],'
        r_flags = LocalFile.read_LocalFile("./boxurl/res/r_flags.txt")
        r_flags = '\r\n\r\n' + r_flags
        r_rules = LocalFile.read_LocalFile("./boxurl/res/r_rules.txt").replace('},{','},\r\n{').replace('[{','[\r\n{')
        r_rules = '\r\n' + r_rules
        r_rules = r_rules.replace('\r','').replace('\n','\r\n')
        r_doh = LocalFile.read_LocalFile("./boxurl/res/r_doh.txt")
        r_doh = '\r\n' + r_doh + '\r\n}'

        r_pushagent = LocalFile.read_LocalFile("./boxurl/res/r_pushagent.txt")

        LocalFile.write_LocalFile('./tvbox.json', r_spider + '\r\n' + r_lives + '\r\n"sites":[' + addtv + '\r\n' + r_pushagent + '],'
            + r_parses + r_flags + r_rules + r_doh)

        # LocalFile.write_LocalFile('./boxurl/out/tvbox.json', r_spider + '\r\n\r\n' + r_lives + '\r\n\r\n"sites":[' + addtv + '\r\n' + r_pushagent + '\r\n],'
            # + r_parses + r_flags + r_rules + r_doh)
        LocalFile.write_LocalFile('./boxurl/out/nsfw.txt', r_spider + '\r\n\r\n' + r_lives + '\r\n\r\n"sites":[' + nsfw + '\r\n' + r_pushagent + '\r\n],'
            + r_parses + r_flags + r_rules + r_doh)
        LocalFile.write_LocalFile('./boxurl/out/all', '"sites":[\r\n//Update:' + str(datetime.datetime.now()) + '\r\n' + addtv + '\r\n' + nsfw + '\r\n' + spare + '\r\n' + r_pushagent + '\r\n],')
    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-623-Exception:' + str(ex))
