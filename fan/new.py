import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

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
    content = diy_conf(content)             # 这里添加diy_conf

    with open('xo.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
        
    # DIY添加自定义接口，写入a.json
    local_content = local_conf(content)
    with open('a.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)
        
    # DIY添加自定义接口，写入b.json
    local_content = local_myconf(content)
    with open('b.json', 'w', encoding='utf-8') as f:
        for line in local_content.split('\n'):  # 将内容按行分割
            if line.strip():  # 如果该行非空（移除空白字符后有内容）
                f.write(line + '\n')  # 将非空行写入到文件中，记得在最后加上 '\n' 以保持原有的行分割
        
    # DIY添加自定义接口，写入c.json
    local_content = local_dianshi(content)
    with open('c.json', 'w', encoding='utf-8') as f:
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
    
def diy_conf(content):
    #content = content.replace('https://fanty.run.goorm.site/ext/js/drpy2.min.js', './lib/drpy2.min.js')
    #content = content.replace('公众号【神秘的哥哥们】', '豆瓣')
    pattern = r'{"key":"Bili"(.)*\n{"key":"Biliych"(.)*\n'
    replacement = ''
    content = re.sub(pattern, replacement, content)
    pattern = r'{"key":"Nbys"(.|\n)*(?={"key":"cc")'
    replacement = ''
    content = re.sub(pattern, replacement, content)

    return content

def read_local_file(file_path):   # 用于加载read_local_file("./fan/res/replace.txt") 函数
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def local_myconf(content):
    # Replace specified key and name  替换"key":"豆豆","name":"全接口智能过滤广告" 为"key":"豆豆","name":"智能AI广告过滤"
    content = re.sub(r'{"key":"豆豆","name":"全接口智能过滤广告",', r'{"key":"豆豆","name":"智能AI广告过滤",', content)
    
    # 删除 //{"key":  整行
    content = re.sub(r'^\s*//\{"key":.*\n', '', content, flags=re.MULTILINE)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)

    # 删除 {"name":"live","type": 整行
    content = re.sub(r'^\s*{"name":"live","type":.*\n', '', content, flags=re.MULTILINE)
    # 删除 { "name": "XIUTAN", "ua": 整行
    content = re.sub(r'^\s*{ "name": "XIUTAN", "ua":.*\n', '', content, flags=re.MULTILINE)
    
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

def remove_specific_blocks(content):
    patterns = [
        r'^\s*//\{"key":.*\n',
        r'^\s*{"name":"live","type":.*\n',
        r'^\s*{ "name": "XIUTAN", "ua":.*\n',
        r'^\s*{"key":"fan","name":"导航.*\n'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
    return content

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
    replacement = read_local_file("./out/dianshi.txt")
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

    # 删除指定行
    content = remove_specific_blocks(content)
    return content

def local_conf(content):                                       # diy 修改后，生成a.json  写命令在# 本地包 local_content = local_conf(content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"YiSo")'         # 用于删除{"key":"88js"  到"key":"YiSo"前一行
    replacement = r'{"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":"./lib/drpy2.min.js","ext":"./js/爱看.js"},\n{"key":"drpy_js_美剧网","name":"影视 | 美剧网[js]","type":3,"api":"./lib/drpy2.min.js","ext":"./js/美剧网.js"},\n{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n{"key":"yaya","name":"鸭鸭┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"https://yayayaaapp.ynf.icu/api.php/app/"},\n{"key":"tiantang","name":"天堂┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://dytt996.com/api.php/app/"},\n{"key":"探探","name":"探探","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"http://ytcms.lyyytv.cn/api.php/app/"},\n{"key":"明帝","name":"明帝","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"https://ys.md214.cn/api.php/app/"},\n'
    content = re.sub(pattern, replacement, content)
    return content

if __name__ == '__main__':
    get_fan_conf()
