#!/usr/bin/env python3

import datetime
import json
import os
import sys
from cls import LocalFile
from cls import NetFile

def main():
    # 获取传递的参数
    try:
        menu = sys.argv[1]
        cid = sys.argv[2] if len(sys.argv) > 2 else None
    except IndexError:
        menu = 'check'
    
    print('menu: ' + menu)

    if menu == 'check':
        check_and_update()

def check_and_update():
    try:
        # 读取本地文件内容
        tvbox = load_file('./b.json') or load_file('./FatCat.json')
        r_sites_err = LocalFile.read_LocalFile("./res/r_sites_err.txt")
        
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

def load_file(filepath):
    """加载本地文件内容"""
    if os.path.exists(filepath):
        return LocalFile.read_LocalFile(filepath).replace('\r', '').replace('\n\n', '\n')
    return None

def validate_line(j, r_sites_err):
    """验证行内容是否有效"""
    return j and '"key":' in j and '"name":' in j and '"type":' in j and r_sites_err.find(j) == -1

def clean_line(j):
    """清理行内容"""
    j = j.strip(',')
    if len(j.split('}')) > len(j.split('{')):
        j = j.strip(',')[:-1].strip(',')
    return j

def validate_url(url):
    """验证 URL 是否有效"""
    if url.startswith('http'):
        ustat = NetFile.url_stat(url, 60, 60)
        return ustat not in [404, 0]
    return True

def is_duplicate(tv, addtv, nsfw, spare, r_sites_err):
    """检查是否存在重复内容"""
    j = json.dumps(tv)
    return (addtv + spare + nsfw).find(j) > -1 or (addtv + nsfw).find('"key":"' + tv['key'] + '"') > -1

def log_error(r_sites_err, j):
    """记录错误日志"""
    r_sites_err += '\r\n[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(404) + ':' + j + ','

def unique_key(tv, addtv, nsfw, r_sites_err):
    """检查是否存在唯一键"""
    return (addtv + nsfw + r_sites_err).find('"api":"' + tv['api'] + '"') > -1

def validate_api(tv, addtv, nsfw, r_sites_err):
    """验证 API 是否有效"""
    api = tv['api']
    if (addtv + nsfw + r_sites_err).find(api) > -1:
        return False
    if api.startswith('http'):
        ustat = NetFile.url_stat(api, 60, 60)
        if ustat in [404, 0]:
            log_error(r_sites_err, json.dumps(tv))
            return False
    return True

if __name__ == "__main__":
    main()
