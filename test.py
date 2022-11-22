# import json
# t = {"flag": 1, "data": {'ban1':1, 'ban2': 0}}
# s = json.dumps(str(t))
# de = json.loads(s)
# dic = eval(de)
# print(type(dic['data']))
# import pandas as pd
# t = {'ban1': 0, 'bab2': 2}
# t = pd.DataFrame({'t':t.values()}, index=t.keys())
# print(t)
import socket
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print(ip)