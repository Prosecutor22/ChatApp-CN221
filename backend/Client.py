import socket
import threading
from sys import argv
import json
import pandas as pd
from backend.const import *

class Client:
    def __init__(self, ip_address, port):
        # create client socket to connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, port))
        self.msg = self.client.recv(2048).decode()
        print(self.msg)
        self.isClosed = False
        
        # get ip of client and create socket to listen from server
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.clientListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientListen.bind((self.ip, CLIENT_LISTEN_PORT))
        self.clientListen.listen(1)
        print(f"[START] Client is listening at {self.ip}:{CLIENT_LISTEN_PORT}")

    def create_auth_message(self, type, username, password):
        # create and encode as binaries Auth message
        message = {
            "pro": "AP",
            "type": type,
            "username": username,
            "password": password
        }
        msg = json.dumps(message)
        return msg.encode(FORMAT)

    def handle_server(self, conn, addr, callback):
        print(f"[NEW CONNECTION] {addr} connected.")
        while True:
            # break if closed
            if self.isClosed:
                break

            msg = conn.recv(2048).decode(FORMAT)
            msg = json.loads(msg)
            print(f'[MESSAGE FROM {addr}] {msg}')

            # update listFriend and call callback when receive update message from server
            if msg['flag'] == 2:
                f_username = msg['data'].keys()[0]
                f_ip = msg['data'].values()[0]
                self.friendList.loc[f_username, 'ip'] = f_ip
                print(f'[INFO] List friends: {self.friendList}')
                callback(f_username, f_ip)
        print(f"[END CONNECTION] {addr} disconnected.")
        conn.close()
    
    def sign_up(self, username, password):
        # send sign up message and return received message to caller
        msg = self.create_auth_message(0, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = json.loads(rcv_msg)
        return rcv_msg
    
    def sign_in(self, username, password, callback):
        # send sign in message
        msg = self.create_auth_message(1, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = eval(json.loads(rcv_msg))

        # update friend list and  when sign in successfully
        if rcv_msg['flag'] == 1:
            (conn, addr) = self.clientListen.accept()
            thread = threading.Thread(target=self.handle_server, args=(conn, addr, callback))
            thread.start()
            users = rcv_msg['data']
            self.friendList = pd.DataFrame({'username': users.keys(), 'ip': users.values()}, index=['username'])   
            print(f'[INFO] List friends: {self.friendList}')

        return rcv_msg

    def sign_out(self):
        # send sign out message and close connection
        self.client.send(self.create_auth_message(2, None, None))
        self.client.close()
        self.isClosed = True

    def ConnectFriendtoChat(self, fr_name:str ):
        peerAnswer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.friendList).loc[fr_name, 'socketAnswer'] = peerAnswer
        friendIP = (self.friendList).loc[fr_name, 'IP']
        ((self.friendList).loc[fr_name, 'socketAnswer']).connect((friendIP, P2P_LISTEN_PORT))

    