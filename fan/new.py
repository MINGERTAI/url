import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("./fan/JAR/config.ini")

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
    content = content.replace(url, './fan/JAR/fan.txt')
    content = diy_conf(content)             # 从这里diy_conf添加自己的
    content = modify_content(content)

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

    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("fan/config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)
        with open(./fan/JAR/config.ini", "w") as f:
            config.write(f)

        response = requests.get(url)
        with open("./fan/JAR/fan.txt", "wb") as f:
            f.write(response.content)

def modify_content(content):   # 更改自定义
    # Replace specified key and name  替换"key":"豆豆","name":"全接口智能过滤广告" 为"key":"豆豆","name":"智能AI广告过滤"
    content = re.sub(r'{"key":"豆豆","name":"全接口智能过滤广告",', r'{"key":"豆豆","name":"智能AI广告过滤",', content)
    
    # 删除 //{"key":  整行
    content = re.sub(r'^\s*//\{"key":.*\n', '', content, flags=re.MULTILINE)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)

    # 替换"live"URL
    original_url = "https://www.huichunniao.cn/xh/lib/live.txt"
    replacement_url = "https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1715581924111/live1.txt"
    content = content.replace(original_url, replacement_url)

    return content
    
def diy_conf(content):
    #content = content.replace('https://fanty.run.goorm.site/ext/js/drpy2.min.js', './fan/JS/lib/drpy2.min.js')
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
    # 从fan/res/parses_flags_rules.txt加载要添加的parses+flags+rules内容
    new_content = read_local_file("./fan/res/parses_flags_rules.txt")
    
    # 从fan/res/replace.txt加载指定内容替换，从{"key":"88js"到{"key":"dr_兔小贝"前的内容
    pattern = r'{"key":"88js"(.|\n)*?(?={"key":"dr_兔小贝")'
    replacement = read_local_file("./fan/res/replace.txt")
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 替换指定{"key":"cc"行内容
    pattern = r'{"key":"cc"(.)*\n'
    replacement = r'{"key":"cc","name":"请勿相信视频中广告","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/drpy.js"}\n'
    content = re.sub(pattern, replacement, content)
    
    # 查找"logo":"http行,并在下面行添加parses+flags+rules内容
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if '"logo":"http' in line:
            # 在找到的行之后添加新内容
            new_lines.append(new_content)
    return '\n'.join(new_lines)

def local_conf(content):                                       # diy 修改后，生成a.json  写命令在# 本地包 local_content = local_conf(content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"YiSo")'         # 用于删除{"key":"88js"  到"key":"YiSo"前一行
    replacement = r'{"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/爱看.js"},\n{"key":"drpy_js_美剧网","name":"影视 | 美剧网[js]","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/美剧网.js"},\n{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n{"key":"yaya","name":"鸭鸭┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"https://yayayaaapp.ynf.icu/api.php/app/"},\n{"key":"tiantang","name":"天堂┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://dytt996.com/api.php/app/"},\n{"key":"探探","name":"探探","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"http://ytcms.lyyytv.cn/api.php/app/"},\n{"key":"明帝","name":"明帝","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"https://ys.md214.cn/api.php/app/"},\n'
    content = re.sub(pattern, replacement, content)
    return content
if __name__ == '__main__':
    get_fan_conf()
