import json
import pprint
from cls import LocalFile
tvbox = LocalFile.read_LocalFile('./fatcat.json')
with open("./out/new_test.json","wb") as f:
    f.write(json.dumps(pprint(tvbox)).encode("utf-8"))
