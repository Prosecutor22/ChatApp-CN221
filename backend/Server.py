import socket
from sys import argv
import threading
import csv
import os
import json
import pandas as pd
from const import *

class Server:
    def __init__(self, ip_address: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip_address, port))
        self.server.listen(100)
        print(f"[START] Server is listening at {ip_address}:{port}")
        self.fileNameClient = os.getcwd() + '/Data/Server/clientData.csv'
        self.filenameListFriend = os.getcwd() + '/Data/Server/listFriend.txt'
        self.df = pd.read_csv(self.fileNameClient, index_col='username')
        self.df['IP'] = None
        self.arrOfSocket = {}

    def setUserStatus(self, username: str, status: int) -> int:
        self.df.loc[username, 'Status'] = status
        return 1
    
    def setUserIP(self, username: str, IP: str) -> int:
        self.df.loc[username, 'IP'] = IP
        return 1

    def searchUserName(self, username: str) -> list:
        '''
        return: list[username, password, IP, status]
        '''
        if username in self.df.index:
            res = [username]
            for i in self.df.loc[[username]].values[0]:
                res.append(i)
            return res
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
        self.df = pd.concat([self.df, pd.DataFrame({'password': [password], 'IP': [None]}, index=[username])])    
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
        '''
        return: {'ban1': 1, 'ban2': 0} 
        '''
        with open(self.filenameListFriend, "r") as f:
            for line in f:
                tmp = line.split()
                if tmp[0] == username:
                    tmp = [x for x in tmp[1].split(',')]
                    res = {}
                    for i in tmp:
                        res[i] = self.df.loc[i, 'IP']
                    return res
                else:
                    continue
        return {}

    def handle_client(self, conn, addr):
        '''
        handle client in a separate thread
        '''
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send(b'[INFO] Connected')
        # cho nay co connect toi client lun ko
        while True:
            msg = conn.recv(2048).decode(FORMAT)
            msg = json.loads(msg)
            print(f'[MESSAGE FROM {addr}] {msg}')
            response = self.processMessage(msg, addr)
            conn.send(response.encode(FORMAT))
            if msg["type"] == 2:
                break  
        print(f"[END CONNECTION] {addr} disconnected.")
        conn.close()

    def run(self):
        while True:
            (conn, addr) = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn,addr))
            thread.start()
    
    # def sendMessageToClient(self, username: str, destinationAddr):
    #     '''
    #     username: name of client that will be sent
    #     destinationAddr: IP of client that will be sent
    #     '''
    #     listFr = self.get_listfriend(username)
    #     message = {"flag": 2,"data": listFr}
    #     msg = json.dumps(str(message))
    #     self.arrOfSocket[username].send(msg)

    def sendMessageToAllFriend(self, fri_list, userNameChangeState, IPChangeState):
        '''
        fri_list: list of name of destination
        send: {usrname: IP}
        '''
        for name, IP in fri_list.items():
            # self.sendMessageToClient(name, IP)
            msg = {"flag": 2, "data": {userNameChangeState: IPChangeState}}
            msg = json.dumps(msg)
            if name in self.arrOfSocket.keys():
                if self.arrOfSocket[name] is not None:
                    self.arrOfSocket[name].send(msg.encode())
            

    def processMessage(self, msg, addr):
        '''
        msg: object(type, username, password)
        return: str_en(flag, data)
        '''
        if msg["type"] == 0: #sign up
            res = self.addNewUser(msg["username"], msg["password"])
            return json.dumps({"flag": res, "data": None})
        elif msg["type"] == 1: #login
            res = self.authenticate(msg["username"], msg["password"])
            if res == 0: #fail login
                return json.dumps(str({"flag": 0, "data": None}))
            else:
                # create socket for communication
                # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.client.connect((ip_address, port))
                # self.msg = self.client.recv(2048).decode()
                # print(self.msg)
                # self.isClosed = False
            
                # # get ip of client and create socket to listen from server
                # self.hostname = socket.gethostname()
                # self.ip = socket.gethostbyname(self.hostname)
                # self.clientListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.clientListen.bind((self.ip, CLIENT_LISTEN_PORT))
                # self.clientListen.listen(1)
                # print(f"[START] Client is listening at {self.ip}:{CLIENT_LISTEN_PORT}")
                
                # self.df.loc[msg["username"], 'listenPort'] = msg['port']
                
                fri_list = self.get_listfriend(msg["username"])
                
                # self.setUserStatus(msg["username"], 1)
                # print(addr[0])
                self.setUserIP(msg["username"], addr[0])
                self.arrOfSocket[msg["username"]] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.arrOfSocket[msg["username"]].connect((addr[0], CLIENT_LISTEN_PORT))
                self.sendMessageToAllFriend(fri_list, msg["username"], addr[0])
                return json.dumps(str({"flag": res, "data": fri_list}))

        else: 
            # logout
            res = self.setUserStatus(msg["username"], 0) & self.setUserIP(msg["username"], None)
            fri_list = self.get_listfriend(msg["username"])
            print(fri_list)
            self.arrOfSocket[msg["username"]].send(json.dumps({"flag": 1, "data": None}).encode())
            self.arrOfSocket[msg["username"]].close()
            self.arrOfSocket[msg["username"]] = None
            self.sendMessageToAllFriend(fri_list, msg["username"], None)
            return json.dumps({"flag": res, "data": None})

if __name__ == "__main__":
    (Server(argv[1], int(argv[2]))).run()