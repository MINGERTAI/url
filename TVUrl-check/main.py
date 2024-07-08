import json
from cls import LocalFile
tvbox = LocalFile.read_LocalFile('fatcat.json')
with open("./out/new_test.json","wb") as f:
    f.write(json.dumps(tvbox,ensure_ascii=False).encode("utf-8"))
    # f.write(json.dumps(dic,ensure_ascii=False,indent=4).encode("utf-8"))
