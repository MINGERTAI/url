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
    content = content.replace(url, './fan/JAR/fan.txt')
    content = diy_conf(content)           # 从这里diy_conf添加自己的
    content = modify_content(content)     # 从这里diy_conf添加自己的

    with open('xo.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
    # 本地包
    local_content = local_conf(content)
    with open('a.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)
    # 本地包
    local_content = local_myconf(content)
    with open('b.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)

    local_content = local_newconf(content)
    with open('c.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)

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
        with open("./fan/JAR/fan.txt", "wb") as f:
            f.write(response.content)

def modify_content(content):   # 从这里添加自己的
    # Replace specified key and name  替换"key":"豆豆","name":"全接口智能过滤广告" 为"key":"豆豆","name":"AI广告过滤"
    content = re.sub(r'{"key":"豆豆","name":"全接口智能过滤广告",', r'{"key":"豆豆","name":"AI广告过滤",', content)
    
    # 删除 //{"key":  整行
    content = re.sub(r'^\s*//\{"key":.*\n', '', content, flags=re.MULTILINE)
    print(content)

    # 替换"logo"URL
    new_logo_url = "https://ghproxy.net/https://raw.githubusercontent.com/ne7359/url/main/fan/AW1.gif"
    content = re.sub(r'"logo":"[^"]+"', f'"logo":"{new_logo_url}"', content)

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

def local_newconf(content):
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"dr_兔小贝")'
    replacement = ocalFile.read_LocalFile("./fan/res/pushagent.txt")
    content = re.sub(pattern, replacement, content)
    return content

def local_myconf(content):                                           # diy 修改后，生成b.json  写命令在# 本地包 local_content = local_myconf(content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"dr_兔小贝")'          # 用于删除{"key":"88js"  到"key":"dr_兔小贝"前一行
    replacement = r'{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1,"categories":["国产动漫","日韩动漫","国产剧","韩国剧","日本剧","综艺片","动漫片","动作片","喜剧片","爱情片","科幻片","恐怖片","剧情片","战争片","台湾剧","香港剧","欧美剧","记录片","海外剧","泰国剧","大陆综艺","港台综艺","日韩综艺","欧美综艺","欧美动漫","港台动漫","海外动漫","体育","足球","篮球","网球","斯诺克"]},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1,"categories":["国产动漫","日韩动漫","国产剧","韩国剧","日本剧","动漫片","动作片","喜剧片","爱情片","科幻片","恐怖片","剧情片","战争片","香港剧","欧美剧","记录片","台湾剧","海外剧","泰国剧","大陆综艺","港台综艺","日韩综艺","欧美综艺","欧美动漫","港台动漫","海外动漫"]},\n{"key":"haiwaikan","name":"海外看┃采集","type":1,"api":"https://haiwaikan.com/api.php/provide/vod","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod","searchable":1,"changeable":1},\n{"key":"索尼","name":"索尼┃采集","type":1,"api":"https://suoniapi.com/api.php/provide/vod","searchable":1,"changeable":1},\n{"key":"drpy_js_360影视","name":"官源┃360","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/360影视.js"},\n{"key":"drpy_js_奇珍异兽","name":"官源┃爱奇艺","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/奇珍异兽.js"},\n{"key":"drpy_js_百忙无果","name":"官源┃芒果","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/百忙无果.js"},\n{"key":"drpy_js_腾云驾雾","name":"官源┃腾讯","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/腾云驾雾.js"},\n{"key":"drpy_js_菜狗","name":"官源┃搜狗","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/菜狗.js"},\n{"key":"drpy_js_优酷","name":"官源┃优酷","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/优酷.js"},\n{"key":"Aid","name":"🚑急救┃教学","type":3,"api":"csp_FirstAid","searchable":0,"quickSearch":0,"changeable":0,"style": { "type": "rect", "ratio":3.8}},\n'
    content = re.sub(pattern, replacement, content)
    return content

def local_conf(content):                                       # diy 修改后，生成a.json  写命令在# 本地包 local_content = local_conf(content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"YiSo")'         # 用于删除{"key":"88js"  到"key":"YiSo"前一行
    replacement = r'{"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/爱看.js"},\n{"key":"drpy_js_美剧网","name":"影视 | 美剧网[js]","type":3,"api":"./fan/JS/lib/drpy2.min.js","ext":"./fan/JS/js/美剧网.js"},\n{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n{"key":"yaya","name":"鸭鸭┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"https://yayayaaapp.ynf.icu/api.php/app/"},\n{"key":"tiantang","name":"天堂┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://dytt996.com/api.php/app/"},\n{"key":"探探","name":"探探","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"http://ytcms.lyyytv.cn/api.php/app/"},\n{"key":"明帝","name":"明帝","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"https://ys.md214.cn/api.php/app/"},\n'
    content = re.sub(pattern, replacement, content)
    return content
if __name__ == '__main__':
    get_fan_conf()
