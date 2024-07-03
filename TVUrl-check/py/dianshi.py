import datetime
import json
import os
import re
import sys
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
if menu == 'uptvbox':
    try:
        if os.path.exists('./out/tmp.txt'):
            tvbox = LocalFile.read_LocalFile('./out/tmp.txt').replace('\r', '').replace('\n\n', '\n')
        else:
            tvbox = LocalFile.read_LocalFile('./code/dianshi.json').replace('\r', '').replace('\n\n', '\n')
        addjson = LocalFile.read_LocalFile("./code/addjson.txt")

        addtv = ''
        nsfw = ''
        spare = ''
        tvbox = tvbox.replace('//{', '\n{')
        for j in tvbox.split('\n'):
            try:
                if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1 and addjson.find(j) == -1:
                    j = j.strip(',')
                    if len(j.split('}')) > len(j.split('{')):
                        j = j.strip(',')[:-1].strip(',')
                    tv = json.loads(j)
                    # 检查自定义Jar文件是否存在
                    if 'jar' in tv.keys():
                        jar = tv['jar']
                        if jar.find('http') == 0:
                            ustat = NetFile.url_stat(jar, 60, 60)
                            if ustat == 404 or ustat == 0:
                                j = j.replace(',"jar":"' + jar + '"', '')
                    # 过滤重复的电影网站
                    if (addtv + spare + nsfw).find(j) > -1:
                        continue
                    # 过滤重复Key的电影网站
                    if (addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1:
                        spare += '\r\n' + j + ','
                        continue
                    # 分类去重
                    id = tv['type']
                    if id == 3:
                        if 'ext' in tv.keys():
                            ext = tv['ext']
                            if (addtv + nsfw + addjson).find(ext) > -1:
                                continue
                            else:
                                if ext.find('http') == 0:
                                    ustat = NetFile.url_stat(ext, 60, 60)
                                    if ustat == 404 or ustat == 0:
                                        addjson += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + j + ','
                                        continue
                    elif id >= 0:
                        api = tv['api']
                        if (addtv + nsfw + addjson).find(api) > -1:
                            continue
                        else:
                            if api.find('http') == 0:
                                ustat = NetFile.url_stat(api, 60, 60)
                                if ustat == 404 or ustat == 0:
                                    addjson += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(ustat) + ':' + j + ','
                                    continue
                    else:
                        spare += '\r\n' + j + ','
                    
                    if tv['name'].find('*') > -1:
                        nsfw += '\r\n' + j + ','
                    elif j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1:
                        addtv += '\r\n' + j + ','
                else:
                    print('Main-Line-91-not-tvsite-url:' + j)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)
        
        myjson = addtv + '\r\n' + nsfw + '\r\n' + spare
        LocalFile.write_LocalFile('./out/tmp.txt', myjson)
        print('Line-96:./out/tmp.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))

if menu == 'del':
    def remove_line(content):
        patterns = [
            r'{"key":"drpy_js_豆瓣"(.|\n)*(?={"key":"高中教育")',   # 删除自{"key":"drpy_js_豆瓣"行到{"key":"高中教育"前一行所有
            r'^\s*{"key":"高中教育".*\n',
            r'^\s*{"key":"蛋蛋".*'      # 删除最后一行不可以添加\n换行代码
        ]    
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        return content

    #try:
        #if os.path.exists('./out/tmp.txt'):
            #content = LocalFile.read_LocalFile('./out/tmp.txt').replace('\r', '').replace('\n\n', '\n')
        #else:
            #content = LocalFile.read_LocalFile('./out/json.txt').replace('\r', '').replace('\n\n', '\n')

        content = LocalFile.read_LocalFile('./out/tmp.txt').replace('\r', '').replace('\n\n', '\n')

        # 应用删除特定行的逻辑
        content = remove_line(content)
        LocalFile.write_LocalFile('./out/newjson.txt', content)

    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))

        #with open('./out/newjson.txt', 'w', newline='', encoding='utf-8') as f:
            #f.write(content)

    #except Exception as e:
       #print(f"An error occurred: {e}")
