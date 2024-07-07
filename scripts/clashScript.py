import os
import re
import datetime
import requests
import argparse
import base64
import smtplib

# 时间
year = datetime.datetime.today().strftime("%Y") # 指令中间不加#号就自动补零
month = datetime.datetime.today().strftime("%m") # 指令中间不加#号就自动补零
day = datetime.datetime.today().strftime("%d") # 指令中间不加#号就自动补零
date = datetime.datetime.today().strftime("%Y%m%d") # 指令中间不加#号就自动补零

def download_clash():
    # 创建文件夹
    if not os.path.exists("clash"):
        os.mkdir("clash")

    def httpGetText(url):
        try:
            req = requests.get(url, verify=False)
            if req.status_code == 200:
                return req.text
        except Exception as e:
            print(f'httpGetText failed: %s' % (e))

    # 免费节点
    result = httpGetText('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml')
    if result:
        fp = open("clash/Clash.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()
        
    # 免费节点1
    result = httpGetText('https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml')
    if result:
        fp = open("clash/Clash1.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()

    # 免费节点2
    result = httpGetText('https://raw.githubusercontent.com/ripaojiedian/freenode/main/clash')
    if result:
        fp = open("clash/Clash2.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()

    #https://clashnode.com/wp-content/uploads/2023/04/20230419.yaml
    # 免费节点3
    result = httpGetText("https://clashnode.com/wp-content/uploads/" + year + "/" + month + "/" + date + ".yaml")
    if result:
        fp = open("clash/Clash3.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()
        
    # 免费节点4
    result = httpGetText("https://raw.githubusercontent.com/vxiaov/free_proxy_ss/main/clash/clash.provider.yaml")
    if result:
        fp = open("clash/Clash4.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()

    # 免费节点5
    result = httpGetText('https://raw.githubusercontent.com/aiboboxx/clashfree/main/clash.yml')
    if result:
        fp = open("clash/Clash5.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()

    # 免费节点6
    result = httpGetText('https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub')
    if result:
        fp = open("clash/Clash6.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()
        
    # 免费节点7
    result = httpGetText('https://raw.githubusercontent.com/Flik6/getNode/main/clash.yaml')
    if result:
        fp = open("clash/Clash7.yml", "w+", encoding='utf-8')
        # print("----" + result)
        fp.write(result)
        fp.close()

if __name__ == "__main__":

    # 下载文件
    download_clash()
