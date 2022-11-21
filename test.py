# import json
# t = {"flag": 1, "data": {'ban1':1, 'ban2': 0}}
# s = json.dumps(str(t))
# de = json.loads(s)
# dic = eval(de)
# print(type(dic['data']))

import pandas as pd

rcv_msg = {'data': [{'username': 'khanhnq', 'ip': '111'}, {'username': 'eeee', 'ip': '222'}]}
# rcv_msg = {'khanhnq': 'aaaa', 'thinh': 'bbb'}
# friendList = pd.DataFrame({'username': ['test'], 'ip': ['000']}, index=['username'])
# print(rcv_msg.keys(), rcv_msg.values())

# for user in rcv_msg['data']:
#     self.friendList.concat([user['username'], user['ip']])
#     pd.concat([friendList, pd.DataFrame({'username': user['username'], 'ip': user['ip']})])
# friendList = friendList.append(pd.DataFrame({'username': rcv_msg.keys(), 'ip': rcv_msg.values()}, index=['username']))
friendList = pd.DataFrame({'username': [user['username'] for user in rcv_msg['data']], \
                           'ip': [user['ip'] for user in rcv_msg['data']]})

print(friendList)
print(friendList.loc[1])
            