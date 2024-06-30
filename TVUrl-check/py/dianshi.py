import datetime
from gettext import find
import json
import os
import requests
import sys
from cls import LocalFile
from cls import NetFile

def delete_lines(content):
    """删除指定模式的行"""
    patterns = [
        r'{"key":"drpy_js_豆瓣","name":(.|\n)*?(?={"key":"Nbys","name":"🛫泥巴┃飞")',
        r'{"key":"drpy_js_58动漫","name":"动漫",.*?\n.*?\n.*?"key":"drpy_js_A8音乐","name":"音频"',
        r'{"key":"drpy_js_影视之家\[V2\]","name":"影视",.*?\n.*?\n.*?"key":"drpy_js_360影视","name":"官源"',
        r'{"key":"bb","name":"配置接口完全免费"}'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
    return content

# 获取传递的参数
try:
    # 0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if len(sys.argv[1:]) > 1:
        cid = sys.argv[1:][1]
except:
    menu = 'check'
print('menu: ' + menu)

# 下载Node.json中的所有Url订阅链接将其合并，生成本地vpei-new.txt，同步至Github后改名为vpei.txt文件
if menu == 'check':
    try:
        if os.path.exists('./out/dianshi.txt'):
            tvbox = LocalFile.read_LocalFile('./out/dianshi.txt').replace('\r', '').replace('\n\n', '\n')
        else:
            tvbox = LocalFile.read_LocalFile('./code/dianshi.json').replace('\r', '').replace('\n\n', '\n')
        
        r_sites_err = LocalFile.read_LocalFile("./code/r_sites_err.txt")
        
        addtv = ''
        nsfw = ''
        spare = ''
        tvbox = tvbox.replace('//{','\n{')
        for j in tvbox.split('\n'):
            try:
                if(j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 and r_sites_err.find(j) == -1):
                    j = j.strip(',')
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
                        
                    elif(id >= 0):
                        api = tv['api']
                        if((addtv + nsfw + r_sites_err).find(api) > -1):
                            continue
                        else:
                            if(api.find('http') == 0):
                                ustat = NetFile.url_stat(api, 60, 60)
                                if(ustat == 404 or ustat == 0):
                                    r_sites_err += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + j + ','
                                    continue

                    else:
                        spare += '\r\n' + j + ','
                    
                    if(tv['name'].find('*') > -1):
                        nsfw += '\r\n' + j + ','
                    elif(j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1):
                        addtv += '\r\n' + j + ','
                else:
                    print('Main-Line-91-not-tvsite-url:' + j)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)
        
        LocalFile.write_LocalFile('./code/r_sites_err.txt', r_sites_err.strip('\r\n'))
        print('Line-96:/res/r_sites_err.txt已更新。')
        
        # 删除指定行
        tvbox = delete_lines(tvbox)
        
        # 将修改后的内容写回文件
        LocalFile.write_LocalFile('./out/dianshi.txt', addtv + '\r\n' + nsfw + '\r\n' + spare)
        
    除了 Exception 之外:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))
