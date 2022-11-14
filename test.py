import pandas as pd

# data = {'ban1':1,'ban2':0, 'ban3': 1}
# df = pd.DataFrame(list(data.items()), columns = ['username', 'stt'])
# df = df.set_index('username')

# data2 = {'ban2':1}
# df2 = pd.DataFrame(list(data2.items()), columns = ['username', 'stt'])
# df2 = df2.set_index('username')
# df.loc[df2.index[0], 'stt'] = df2.stt[0]

# print(df)
t = pd.read_csv('E:/HCMUT/HK_221/MANG_MAY_TINH/Ass1/ChatApp-CN221/Data/Server/clientData.csv', index_col='username')
# r = ['thinh']
# for i in list(t.loc[['thinhlqh']].values[0]):
#     r.append(i)
# print(r)
# t = t.append(pd.DataFrame({'password': ['i'], 'IP': [None], 'Status': [0]}, index=['ue']))
# print(t)
t['IP'] = None
t['Status'] = 0
username = 'thinhlqh'
if username in t.index:
    res = [username]
    for i in t.loc[[username]].values[0]:
        res.append(i)
    print(res)



