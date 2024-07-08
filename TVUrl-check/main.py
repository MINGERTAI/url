import json
import pprint
with open("fatcat.json","rb") as f:
with open("./out/new_test.json","wb") as f:
    f.write(json.dumps(pprint(data)).encode("utf-8"))
