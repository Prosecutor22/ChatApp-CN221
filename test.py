# import json
# t = {"flag": 1, "data": {'ban1':1, 'ban2': 0}}
# s = json.dumps(str(t))
# de = json.loads(s)
# dic = eval(de)
# print(type(dic['data']))
import pandas as pd
t = pd.DataFrame({}, columns=['r'], index='d')
print(t)