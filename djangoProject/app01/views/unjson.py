import json
from collections import namedtuple


#  将Json格式的数据转化成Object
def UnJson(json_data):
    json_str = json.dumps(json_data)
    data = json.loads(json_str, object_hook=lambda d: namedtuple('data', d.keys())(*d.values()))
    return data