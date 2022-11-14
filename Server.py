import socket
from sys import argv
import threading
import csv
import os
import json
import pandas as pd


FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Server:
    def __init__(self, ip_address: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip_address, port))
        self.server.listen(100)
        print(f"[START] Server is listening at {ip_address}:{port}")
        self.fileNameClient = os.getcwd() + '\Data\Server\clientData.csv'
        self.filenameListFriend = os.getcwd() + '\Data\Server\listFriend.txt'
        self.df = pd.read_csv(self.fileNameClient, index_col='username')
        self.df['IP'] = None
        self.df['Status'] = 0

    
    def searchUserName(self, username: str) -> list:
        '''
        return: list[username, password, IP, status]
        '''
        if username in self.df.index:
            # res = [username]
            # for i in list(self.df.loc([[username]]).values[0]):
            #     res.append(i)
            # return res
            return [username,username]
        else:
            return None
    
    # return 1 if register OK, else 0
    def addNewUser(self, username: str, password: str) -> int:
        '''
        return: int 
        0 -> exist usr
        1 -> not exist usr -> add success
        '''
        if self.searchUserName(username) != None:
            return 0
        userData = [username, password]
        with open(self.fileNameClient, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(userData)   
        #self.df.append(pd.DataFrame({'password': [password], 'IP': [None], 'Status': [0]}), index=username)    
        return 1  
      
    def authenticate(self, username: str, password: str) -> int:
        '''
        return: int
        0 -> login fail
        1 -> login success   data = {'ban1':1,'ban2':0}
        '''
        user = self.searchUserName(username)
        if user == None or password != user[1]:
            return 0
        return 1
    
    def get_listfriend(self, username):
        with open(self.filenameListFriend, "r") as f:
            for line in f:
                tmp = line.split()
                if tmp[0] == username:
                    return [x for x in tmp[1].split(',')]
                else:
                    continue
        return []

    def handle_client(self, conn, addr):
        '''
        handle client in a separate thread
        '''
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send(b'[INFO] Connected')
        connected = True
        while connected:
            msg = conn.recv(2048).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                msg = json.loads(msg)
                response = self.processMessage(msg)
                conn.send(response.encode(FORMAT))
        print(f"[END CONNECTION] {addr} disconnected.")
        conn.close()
    
    def run(self):
        while True:
            (conn, addr) = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn,addr))
            thread.run()

    def processAPMessage(self, msg):
        '''
        msg: object(pro, type, username, password)
        return: str_en(flag, data)
        '''
        if msg["type"] == 0: #sign up
            res = self.addNewUser(msg["username"], msg["password"])
            return json.dumps({"flag": res, "data": None})
        elif msg["type"] == 1: #login
            res = self.authenticate(msg["username"], msg["password"])
            if res == 0: #fail login
                return json.dumps({"flag": 0, "data": None})
            else:
                fri_list = self.get_listfriend(msg["username"])
                return json.dumps({"flag": res, "data": fri_list})
        else: 
            # logout
            pass
    

    def processMessage(self, msg):
        '''
        msg: object(pro, ...)
        return: str_en(...)
        '''
        print(msg)
        if msg['pro'] == "AP":
            return self.processAPMessage(msg)
        elif msg['pro'] == "SCP":
            return "Receive SCP Message"
        else:
            return "Receive CP Message"
        

if __name__ == "__main__":
    (Server(argv[1], int(argv[2]))).run()