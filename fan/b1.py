import requests
import json
import hashlib
import configparser
import re
import os

import datetime
from gettext import find
import json
import sys
from cls import LocalFile
from cls import NetFile

headers = {'User-Agent': 'okhttp/3.15'}

def save_website_content_as_json_and_check_updates(url, file_name):
    # 定义配置文件和jar文件的保存路径
    config_directory = os.path.join("fan", "FatCat")
    config_path = os.path.join(config_directory, "config.ini")
    
    # 确保目标目录存在
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            new_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            old_md5 = config.get('DEFAULT', 'md5', fallback='')
            if new_md5 != old_md5:
                print("检测到更新。")
                # 更新配置文件中的md5值
                config['DEFAULT']['md5'] = new_md5
                with open(config_path, 'w') as configfile:
                    config.write(configfile)
                
                spider = data.get('spider')
                if spider:
                    jar_url, jar_md5 = re.match(r'http://[^/]+/jar/(.+?);md5;([a-f0-9]{32})', spider).groups()
                    full_jar_url = f"http://like.xn--z7x900a.com/jar/{jar_url}"
                    jar_response = requests.get(full_jar_url)
                    if jar_response.status_code == 200:
                        jar_file_name = jar_url.split('/')[-1]
                        # 构建jar文件的完整保存路径
                        jar_file_path = os.path.join(config_directory, jar_file_name)
                        with open(jar_file_path, 'wb') as jar_file:
                            jar_file.write(jar_response.content)
                        print(f"jar文件已下载到：{jar_file_path}")
                        # 更新配置文件
                        config['DEFAULT']['jar_md5'] = jar_md5
                        with open(config_path, 'w') as configfile:
                            config.write(configfile)
                        print("jar文件的md5值已更新。")
                    else:
                        print(f"jar文件下载失败，状态码：{jar_response.status_code}")

                if 'spider' in data:
                    original_url = data['spider'].split(';md5;')[0]
                    data['spider'] = data['spider'].replace(original_url, f'./fan/FatCat/{jar_file_name}')
                # 假设已经有一个字典 data 和变量 jar_file_name
                for key in data:
                    # 检查值是否为字符串类型
                    if isinstance(data[key], str):
                        # 替换 'http://js.xn--z7x900a.com' 为 './fan/FatCat'
                        data[key] = data[key].replace('http://js.xn--z7x900a.com/', './fan/FatCat/')

                # 将修改后的data保存为JSON文件
                #json_file_path = os.path.join(config_directory, file_name + '.json')
                #with open(json_file_path, 'w', encoding='utf-8') as file:
                with open(file_name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"数据已以JSON格式保存到{file_name}")
            else:
                print("未检测到更新。")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 目标URL
url = 'http://肥猫.com'
# 文件名，不包括扩展名
file_name = 'FatCat'

save_website_content_as_json_and_check_updates(url, file_name)


# 获取传递的参数
try:
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    menu = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        cid = sys.argv[1:][1]
except:
    menu = 'check'
print('menu: ' + menu)

# 下载FatCat.json中的所有Url订阅链接将其合并
if(menu == 'check'):
    try:
        tvbox = LocalFile.read_LocalFile('FatCat.json').replace('\r','').replace('\n\n','\n')
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


        # r_pushagent = LocalFile.read_LocalFile("./res/r_pushagent.txt")
        r_update = '{\r\n//Update:' + str(datetime.datetime.now()) + '\r\n'

        LocalFile.write_LocalFile('./all.txt', '"sites":[\r\n//Update:' + str(datetime.datetime.now()) + '\r\n' + addtv + '\r\n' + nsfw + '\r\n' + spare + '\r\n],')
