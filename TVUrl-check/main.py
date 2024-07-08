import json
import pprint
from cls import LocalFile
tvbox = LocalFile.read_LocalFile('./fatcat.json')
pprint.pprint(tvbox)
