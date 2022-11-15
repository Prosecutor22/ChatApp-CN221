import socket
import threading
from sys import argv
import json
import pandas as pd

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Client:
    def __init__(self, ip_address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, port))
        self.msg = self.client.recv(2048).decode()
        print(self.msg)
        # self.sendServer(self.createAuthMessage(0, 'minhpp', 'minhpp'))
        # self.friendList
        # self.client.close()

    def createAuthMessage(self, type: int, username: str, password: str) -> str:
        """
        return: str_en(pro, type, username, password)
        """
        message = {
            "pro": "AP",
            "type": type,
            "username": username,
            "password": password
        }
        msg = json.dumps(message)
        return msg
        

    # def sendServer(self, msg):
    #     message = msg.encode(FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(FORMAT)
    #     send_length += b' ' * (HEADER - len(send_length))
    #     self.client.send(send_length)
    #     self.client.send(message)
    #     print(self.client.recv(2048).decode(FORMAT))

    def APClientProcess(self, obj):
        if obj['flag'] == 0:
            print("Fail")
        elif obj['flag'] == 1:
            print("Success")
            friendList = pd.DataFrame(list((obj.data).items()), columns = ['username', 'stt'])
            friendList = friendList.set_index('username')
        elif obj['flag'] == 2:
            df = pd.DataFrame(list((obj.data).items()), columns = ['username', 'stt'])
            df = df.set_index('username')
            friendList.loc[df2.index[0], 'stt'] = df.stt[0]
        else:
            print("Message fault")

    def RProcess(self, obj):
        pass
    
    def receiveServer(self, msg):
        message = msg.decode()
        if message['pro'] == "AP":
            self.APClientProcess(message)
        elif message['pro'] == "RP":
            self.RPprocess(message)
        pass

    def run(self):
        while True:
            print("Sign up")
            username = input("Enter username: ")
            password = input("Enter password: ")
            msg = self.createAuthMessage(0, username, password)
            self.client.send(msg.encode(FORMAT))
            rcv_msg = self.client.recv(2048).decode(FORMAT)
            rcv_msg = json.loads(rcv_msg)
            if rcv_msg['flag'] == 1:
                print('[INFO] Sign up successfully')
                break
            else:
                print('[INFO] Sign up fail')
        while True:
            print("Sign in")
            username = input("Enter username: ")
            password = input("Enter password: ")
            msg = self.createAuthMessage(1, username, password)
            self.client.send(msg.encode(FORMAT))
            rcv_msg = self.client.recv(2048).decode(FORMAT)
            rcv_msg = json.loads(rcv_msg)
            if rcv_msg['flag'] == 1:
                print('[INFO] Sign in successfully')
                print(f'[RESULT] {rcv_msg["data"]}')
                break
            else:
                print('[INFO] Sign in fail')
        self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        self.client.close()

        

if __name__ == "__main__":
    (Client(argv[1], int(argv[2]))).run()
    