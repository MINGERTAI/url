import json
with open("fatcat.json","rb") as f:
    dic = json.load(f)
    sites = dic["sites"]
    sites.append({'key': 'test', 'name': 'test', 'type': 3, 'api': 'csp_Douban', 'searchable': 0})  ## 新增
    sites.remove(sites[-1])  ## 删除最后一行
with open("./out/new_test.json","wb") as f:
    f.write(json.dumps(dic,ensure_ascii=False).encode("utf-8"))
    # f.write(json.dumps(dic,ensure_ascii=False,indent=4).encode("utf-8"))
