import os
import csv
from Server import Server
#fileName = os.getcwd() + '\Data\Server\clientData.csv'
us = 'us'
# userData = [us, us, None, None]
# with open(fileName, 'a+') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for i in range(5):
#         csvwriter.writerow(userData)        
test = Server("ip_address", 1)
for i in range(5):
    test.addNewUser(us, us)
