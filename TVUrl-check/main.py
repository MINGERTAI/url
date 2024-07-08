import json
with open("fatcat.json","rb") as f:
    dic = json.load(f)
    sites = dic["sites"]
    sites.append({'key': 'test', 'name': 'test', 'type': 3, 'api': 'csp_Douban', 'searchable': 0})  ## 新增
    sites.remove(sites[-1])  ## 删除最后一行
    
local_content = json.dumps(dic,ensure_ascii=False)
with open('./out/new_test.json', 'w', encoding='utf-8') as f:
    for line in local_content.split('\n'):  # 将内容按行分割
        if line.strip("},"):  # 如果该行非空（移除空白字符后有内容）
            f.write(line + '\n')  # 将非空行写入到文件中，记得在最后加上 '\n' 以保持原有的行分割
#with open("./out/new_test.json","wb") as f:
    #f.write(json.dumps(dic,ensure_ascii=False).encode("utf-8"))
    # f.write(json.dumps(dic,ensure_ascii=False,indent=4).encode("utf-8"))
