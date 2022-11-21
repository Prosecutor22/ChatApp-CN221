import socket
import threading
from sys import argv
import json
import pandas as pd

FORMAT = 'utf-8'


# send a chat message: name is absolute path filename, data is normal message, 
def sendChatMessage(name: str, data: str, conn):
    conn.send(createChatMessage(name, data))

def createChatMessage(name: str, data: str):
    if str == "":
        pass
    else:
        data = ''''''
        with open(str, "r") as f:
            for line in f:
                data += line
        name = name.split('\\')[-1]
    message = {
        'name': name,
        'data': data
    }
    msg = json.dumps(message)
    return msg

# using for receiving only one message per call, input is connection
#output: {
#           'name':'Alice_In_Wonderland', 
#           'data': '''dsddjdnafu afnfiuqe
#                       fafwefefweeqfefewf'''
# }
def receiveChatMessage(conn):
    msg = conn.recv(2048).decode(FORMAT)
    msg = json.loads(msg)
    return msg