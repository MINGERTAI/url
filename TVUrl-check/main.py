import json
import pprint
from cls import LocalFile
tvbox = LocalFile.read_LocalFile('./fatcat.json')
data = pprint.pprint(tvbox)
with open("./out/new_test.json","wb") as f:
    f.write(data)
