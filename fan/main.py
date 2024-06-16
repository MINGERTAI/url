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
        if(os.path.exists('./b.json')):
            tvbox = LocalFile.read_LocalFile('./b.json').replace('\r','').replace('\n\n','\n')
        else:
            tvbox = LocalFile.read_LocalFile('./FatCat.json').replace('\r','').replace('\n\n','\n')
        r_sites_err = LocalFile.read_LocalFile("./fan/res/r_sites_err.txt")
        
        addtv = ''
        nsfw = ''
        spare = ''
        tvbox = tvbox.replace('//{','\n{')

        for j in tvbox.split('\n'):
            try:
                if validate_line(j, r_sites_err):
                    j = clean_line(j)
                    tv = json.loads(j)
                    
                    # 检查 Jar 文件是否存在
                    if 'jar' in tv:
                        if not validate_url(tv['jar']):
                            j = j.replace(',"jar":"' + tv['jar'] + '"', '')

                    # 过滤重复内容
                    if is_duplicate(tv, addtv, nsfw, spare, r_sites_err):
                        continue

                    # 分类处理
                    id = tv['type']
                    if id == 3:
                        if 'ext' in tv:
                            if not validate_url(tv['ext']):
                                log_error(r_sites_err, j)
                                continue
                        elif unique_key(tv, addtv, nsfw, r_sites_err):
                            continue
                    elif id >= 0:
                        if not validate_api(tv, addtv, nsfw, r_sites_err):
                            continue
                    else:
                        spare += '\r\n' + j + ','

                    # 根据名字分类
                    if '*' in tv['name']:
                        nsfw += '\r\n' + j + ','
                    else:
                        addtv += '\r\n' + j + ','
                else:
                    print('Main-Line-91-not-tvsite-url:' + j)
            except Exception as ex:
                LocalFile.write_LogFile('Main-Line-93-Exception:' + str(ex) + '\ntvsite:' + j)
        
        # 更新错误日志文件
        LocalFile.write_LocalFile('./res/r_sites_err.txt', r_sites_err.strip('\r\n'))
        print('Line-96:/res/r_sites_err.txt已更新。')

        # 更新 all.txt 文件
        LocalFile.write_LocalFile('./out/all.txt', '"sites":[\r\n//Update:' + str(datetime.datetime.now()) + '\r\n' + addtv + '\r\n' + nsfw + '\r\n' + spare + '\r\n],')
    except Exception as ex:
        LocalFile.write_LogFile('Main-Line-108-Exception:' + str(ex))

if __name__ == "__main__":
    main()
