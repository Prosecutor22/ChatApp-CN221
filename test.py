import pandas as pd

# data = {'ban1':1,'ban2':0, 'ban3': 1}
# df = pd.DataFrame(list(data.items()), columns = ['username', 'stt'])
# df = df.set_index('username')

# data2 = {'ban2':1}
# df2 = pd.DataFrame(list(data2.items()), columns = ['username', 'stt'])
# df2 = df2.set_index('username')
# df.loc[df2.index[0], 'stt'] = df2.stt[0]

# print(df)
t = pd.read_csv('D:\Computer Network\BTL\ChatApp-CN221\Data\Server\clientData.csv', index_col='username')
r = ['thinh']
p = t.loc[['thinhlqh']].values[0]
for i in p:
    r.append(i)
print(r)

