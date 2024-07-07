#添加 headers：在请求头中添加 User-Agent 以避免某些服务器的拒绝访问。
#response.text：使用 response.text 获取响应内容。
#精确条件：确保只有完全匹配 "key":、"name": 和 "type": 的行才被处理。
#异常处理：在每行处理过程中添加异常处理，并记录日志。
#通过这些修改，脚本将从指定 URL 下载 shg.json 文件，提取包含 "key":、"name": 和 "type": 的行，并将结果写入到 ./out/11.txt 文件中
import datetime
import json
import os
import requests
import sys
from cls import LocalFile

import re
import base64
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def remove_line(content):
    patterns = [
        r'{"key":"drpy_js_豆瓣"(.|\n)*(?={"key":"高中教育")',   # 删除自{"key":"drpy_js_豆瓣"行到{"key":"高中教育"前一行所有
        r'^\s*{"key":"高中教育".*\n',
        r'{"key":"drpy_js_校长影视"(.|\n)*(?={"key":"drpy_js_磁力熊)',
        r'{"key":"drpy_js_童趣"(.|\n)*(?={"key":"drpy_js_好趣网")',
        r'{"key":"drpy_js_58动漫"(.|\n)*(?={"key":"drpy_js_怡萱动漫")',
        r'^\s*{"key":"drpy_js_怡萱动漫".*\n',
        r'^\s*{"key":"bb","name".*\n',
        r'^\s*{"key":"cc","name".*'      # 删除最后一行不可以添加\n换行代码
    ]    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    return content

def download_file():
    """
    从指定 URL 下载文件并保存到本地路径。
    """
    try:
        # 发送 HTTP GET 请求
        url = "https://raw.githubusercontent.com/qist/tvbox/master/dianshi.json"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # 检查请求是否成功
        response.raise_for_status()

        # 解析 JSON 内容
        tvbox = response.text
        spare = ''
        
        # 分行处理 JSON 内容
        for j in tvbox.split('\n'):
            try:
                if j != '' and j.find('"key":') > -1 and j.find('"name":') > -1 and j.find('"type":') > -1:
                    j = j.strip(',').replace('"type":0','"type":1')
                    if(len(j.split('}')) > len(j.split('{'))):
                        j = j.strip(',')[:-1].strip(',')
                    # 过滤重复的电影网站
                    if spare.find(j) > -1:
                        continue
                    spare += '\r\n' + j
            except Exception as ex:
                LocalFile.write_LogFile(f"解析行时出错: {str(ex)} 行内容: {j}")
        
        content = spare
        content = remove_line(content)
        LocalFile.write_LocalFile('./out/new.txt', content)
        print('读取并删除:./out/new.txt已更新。')

    except Exception as ex:
        LocalFile.write_LogFile(f"下载或处理文件时出错: {str(ex)}")

    download_file()

#############

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("fan/config.ini")

    url = 'http://饭太硬.com/tv'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

    if not match:
        return
    result = match.group(1)

    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5 = m.hexdigest()

    try:
        old_md5 = config.get("md5", "conf")
        if md5 == old_md5:
            print("No update needed")
            return
    except:
        pass

    content = base64.b64decode(result).decode('utf-8')
    url = re.search(r'spider"\:"(.*);md5;', content).group(1)
    content = content.replace(url, './jar/fan.txt')
    #content = remove_line(content)

    with open('xo.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)

    # DIY添加自定义接口，写入a.json
    local_content = local_conf(content)
    with open('a.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)

    content = remove_line(content)        
    # DIY添加自定义接口，写入b.json
    local_content = local_myconf(content)
    with open('b.json', 'w', encoding='utf-8') as f:
        for line in local_content.split('\n'):  # 将内容按行分割
            if line.strip():  # 如果该行非空（移除空白字符后有内容）
                f.write(line + '\n')  # 将非空行写入到文件中，记得在最后加上 '\n' 以保持原有的行分割
        
    # DIY添加自定义接口，写入c.json
    local_content = local_dianshi(content)
    with open('d.json', 'w', encoding='utf-8') as f:
        for line in local_content.split('\n'):  # 将内容按行分割
            if line.strip():  # 如果该行非空（移除空白字符后有内容）
                f.write(line + '\n')  # 将非空行写入到文件中，记得在最后加上 '\n' 以保持原有的行分割

    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("fan/config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)
        with open("fan/config.ini", "w") as f:
            config.write(f)

        response = requests.get(url)
        with open("./jar/fan.txt", "wb") as f:
            f.write(response.content)

def remove_line(content):
    patterns = [
        r'^\s*//\{"key":.*\n',
        r'^\s*{"key":"fan","name":"导航.*\n',
        r'{"key":"Bili"(.)*\n{"key":"Biliych"(.)*\n',
        r'{"key":"Nbys"(.|\n)*(?={"key":"cc")',
        r'^\s*{"name":"live","type":.*\n',
        r'^\s*{ "name": "XIUTAN", "ua":.*\n'
    ]    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)        
    return content

def read_local_file(file_path): #用于加载文本函数
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def local_myconf(content):
    # Replace specified key and name  替换"key":"豆豆","name":"全接口智能过滤广告" 为"key":"豆豆","name":"智能AI广告过滤"
    content = re.sub(r'{"key":"豆豆","name":"全接口智能过滤广告",', r'{"key":"豆豆","name":"智能AI广告过滤",', content)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)
    
    # 从文件加载要添加的新内容
    new_content = read_local_file("./fan/res/parses_flags_rules.txt")
    live_content = read_local_file("./fan/res/lives.txt")

    # 替换指定模式的内容，从{"key":"88js"到{"key":"dr_兔小贝"前的内容
    pattern = r'{"key":"88js"(.|\n)*?(?={"key":"dr_兔小贝")'
    replacement = read_local_file("./fan/res/replace.txt")
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 替换指定{"key":"cc"行内容
    pattern = r'{"key":"cc"(.)*\n'
    replacement = r'{"key":"cc","name":"豆瓣","type":3,"api":"./lib/drpy2.min.js","ext":"./js/drpy.js"}\n'
    content = re.sub(pattern, replacement, content)
   
    # 查找并在 "doh":[{"name":"Google" 之后添加新内容
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if '"doh":[{"name":"Google"' in line:
            # 在找到的行之后添加新内容
            new_lines.append(new_content)
            
    # 查找并在 "lives":[" 之后添加新内容
    final_lines = []
    for line in new_lines:
        final_lines.append(line)
        if '"lives":[' in line:
            # 在找到的行之后添加新内容
            final_lines.append(live_content)
    
    return '\n'.join(final_lines)

def local_dianshi(content):
    # Replace specified key and name  替换"key":"豆豆","name":"全接口智能过滤广告" 为"key":"豆豆","name":"智能AI广告过滤"
    content = re.sub(r'{"key":"豆豆","name":"全接口智能过滤广告",', r'{"key":"豆豆","name":"智能AI广告过滤",', content)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)
    
    # 从文件加载要添加的新内容
    new_content = read_local_file("./fan/res/parses_flags_rules_dianshi.txt")
    live_content = read_local_file("./fan/res/lives.txt")

    # 替换指定模式的内容，从{"key":"88js"到{"key":"dr_兔小贝"前的内容
    pattern = r'{"key":"88js"(.|\n)*?(?={"key":"dr_兔小贝")'
    replacement = read_local_file("./out/new.txt")
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 替换指定{"key":"cc"行内容
    pattern = r'{"key":"cc"(.)*\n'
    replacement = r'{"key":"cc","name":"豆瓣","type":3,"api":"./lib/drpy2.min.js","ext":"./js/drpy.js"}\n'
    content = re.sub(pattern, replacement, content)
   
    # 查找并在 "doh":[{"name":"Google" 之后添加新内容
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if '"doh":[{"name":"Google"' in line:
            # 在找到的行之后添加新内容
            new_lines.append(new_content)
            
    # 查找并在 "lives":[" 之后添加新内容
    final_lines = []
    for line in new_lines:
        final_lines.append(line)
        if '"lives":[' in line:
            # 在找到的行之后添加新内容
            final_lines.append(live_content)
    
    return '\n'.join(final_lines)

def local_conf(content):                                       # diy 修改后，生成a.json  写命令在# 本地包 local_content = local_conf(content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"YiSo")'         # 用于删除{"key":"88js"  到"key":"YiSo"前一行
    replacement = r'{"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":"./lib/drpy2.min.js","ext":"./js/爱看.js"},\n{"key":"drpy_js_美剧网","name":"影视 | 美剧网[js]","type":3,"api":"./lib/drpy2.min.js","ext":"./js/美剧网.js"},\n{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n{"key":"yaya","name":"鸭鸭┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"https://yayayaaapp.ynf.icu/api.php/app/"},\n{"key":"tiantang","name":"天堂┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://dytt996.com/api.php/app/"},\n{"key":"探探","name":"探探","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"http://ytcms.lyyytv.cn/api.php/app/"},\n{"key":"明帝","name":"明帝","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"https://ys.md214.cn/api.php/app/"},\n'
    content = re.sub(pattern, replacement, content)
    return content

if __name__ == '__main__':
    get_fan_conf()
