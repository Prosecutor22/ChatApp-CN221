import socket
import threading
from sys import argv
import json
import pandas as pd

FORMAT = 'utf-8'

def sendChatMessage(message: str, ):
    pass

def createChatMessage(name: str, data: str):
    if str == "":
        pass
    else:
        pass
    message = {
        'name': name,
        'data': data
    }
    msg = json.dumps(message)
    return msg

def receiveChatMessage(conn):
    