import socket
import threading
from sys import argv
import json
import pandas as pd

FORMAT = 'utf-8'

P2P_LISTEN_PORT = 4444

class Client:
    def __init__(self, ip_address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, port))
        
        self.hostname=socket.gethostname()
        self.IPAddr=socket.gethostbyname(self.hostname)
        
        self.clientListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.clientListen.bind((self.IPAddr, 222))
        self.host, self.portListen = self.clientListen.getsockname()
        self.msg = self.client.recv(2048).decode()
        print(self.msg)
        self.friendList = []

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
        return msg.encode(FORMAT)

    def APClientProcess(self, obj):
        if obj['flag'] == 0:
            print("Fail")
        elif obj['flag'] == 1:
            print("Success")
            self.friendList = pd.DataFrame(list((obj.data).items()), columns = ['username', 'stt'])
            self.friendList = self.friendList.set_index('username')
            self.friendList['portListen'] = None
            self.friendList['IP'] = None
        elif obj['flag'] == 2:
            df = pd.DataFrame(list((obj.data).items()), columns = ['username', 'stt'])
            df = df.set_index('username')
            self.friendList.loc[df.index[0], 'stt'] = df.stt[0]
            if (df.stt[0] == 0):
                self.friendList.loc[df.index[0], 'IP'] = None
        else:
            print("Message fault")
    
    def receiveServer(self, msg):
        message = msg.decode()
        if message['pro'] == "AP":
            self.APClientProcess(message)
        elif message['pro'] == "SCP":
            self.SCPprocess(message)
        pass

    def handle_server(self, conn, addr):
        while True:
            msg = conn.recv(2048).decode(FORMAT)
            msg = json.loads(msg)
            self.APClientProcess(msg)

    def run(self):
        while True:
            (conn, addr) = self.clientListen.accept()
            thread = threading.Thread(target=self.handle_server, args=(conn,addr))
            thread.start()
    
    def sign_up(self, username, password):
        msg = self.createAuthMessage(0, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = json.loads(rcv_msg)
        return rcv_msg
    
    def sign_in(self, username, password):
        msg = self.createAuthMessage(1, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = eval(json.loads(rcv_msg))
        return rcv_msg

    def sign_out(self):
        self.client.send(self.createAuthMessage(2, None, None))
        self.client.close()

    def ConnectFriendtoChat(self, fr_name:str ):
        peerAnswer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.friendList).loc[fr_name, 'socketAnswer'] = peerAnswer
        friendIP = (self.friendList).loc[fr_name, 'IP']
        ((self.friendList).loc[fr_name, 'socketAnswer']).connect((friendIP, P2P_LISTEN_PORT))

    '''

    '''

if __name__ == "__main__":
    (Client(argv[1], int(argv[2]))).run()
    