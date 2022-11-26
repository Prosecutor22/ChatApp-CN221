import socket
import threading
from sys import argv
import json
import pandas as pd
from backend.const import *
import sys
import os
import hashlib

def HashPassWord(password: str):
    salt = "KTML"
    key = password + salt
    hashed = hashlib.md5(key.encode('utf-8')).hexdigest()
    return hashed

class Client:
    def __init__(self, ip_address, port, update_status_cb, change_message_cb):
        self.callback = update_status_cb
        self.change_message_cb = change_message_cb

        # get ip of client and create socket to listen from server
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.clientListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(self.ip)
        self.clientListen.bind((self.ip, CLIENT_LISTEN_PORT))
        self.clientListen.listen(1)
        print(f"[START] Client is listening at {self.ip}:{CLIENT_LISTEN_PORT}")
        thread = threading.Thread(target=self.handle_server, args=(), name='Thread handle server')
        thread.start()

        # create client socket to connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, port))
        self.msg = self.client.recv(2048).decode()
        print(self.msg)
        self.isClosed = False
        self.conns = []
    
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

    def handle_server(self):
        (conn, addr) = self.clientListen.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
            
        while True:
            # break if closed
            if self.isClosed:
                break

            msg = conn.recv(2048).decode(FORMAT)
            msg = json.loads(msg)
            print(f'[MESSAGE FROM {addr}] {msg}')
            print(msg)
            # update listFriend and call callback when receive update message from server
            if msg['flag'] == 2:
                f_username = list(msg['data'].keys())[0]
                f_ip = list(msg['data'].values())[0]
                self.friendList.loc[f_username, 'ip'] = f_ip
                self.friendList.loc[f_username, 'socket'] = None
                print(f'[INFO] List friends: {self.friendList}')
                self.callback(f_username, f_ip)
            elif msg['flag'] == 1:
                break
        print(f"[END CONNECTION] {addr} disconnected.")
        conn.close()
        sys.exit(0)

    def handle_P2P(self):
        try:
            while True:
                if self.isClosed:
                    break
                (conn, addr) = self.P2PListen.accept()
                self.conns.append(conn)
                print(f"[NEW CONNECTION PEER] {addr} connected.")
                friend = self.FindFriendbyIP(addr[0])
                self.ConnectFriendtoChat(friend)
                thread = threading.Thread(target=self.receiveMessage, args=(conn, friend))
                thread.start()
        except:
            pass
        print("[END LISTEN FROM OTHER PEER]")
        sys.exit(0)
    
    def sign_up(self, username, password):
        # send sign up message and return received message to caller
        password = HashPassWord(password)
        msg = self.create_auth_message(0, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = json.loads(rcv_msg)
        return rcv_msg
    
    def sign_in(self, username, password):
        # send sign in message
        password = HashPassWord(password)
        msg = self.create_auth_message(1, username, password)
        self.client.send(msg)
        rcv_msg = self.client.recv(2048).decode(FORMAT)
        rcv_msg = eval(json.loads(rcv_msg))

        # update friend list and  when sign in successfully
        if rcv_msg['flag'] == 1:
            self.username = username
            users = rcv_msg['data']
            self.friendList = pd.DataFrame({'ip': users.values()}, index=users.keys())
            self.friendList['socket'] = None
            self.friendList['message'] = None
            print(f'[INFO] List friends: {self.friendList}')
            # start bind the connect from other peer
            self.P2PListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.P2PListen.bind((self.ip, P2P_LISTEN_PORT))
            self.P2PListen.listen(100)
            print(f"[START] Peer is listening at {self.ip}:{P2P_LISTEN_PORT}")
            thread = threading.Thread(target=self.handle_P2P, args=(), name='Thread handle p2p')
            thread.start()
            

        return rcv_msg

    def sign_out(self):
        # send sign out message and close connection
        self.client.send(self.create_auth_message(2, self.username, None))
        self.client.close()
        self.isClosed = True
        self.P2PListen.close()
        for conn in self.conns:
            conn.close()
        for conn in self.friendList['socket'].values:
            if conn != None:
                conn.close()

    # function call when user click on a friend on list friend
    def ConnectFriendtoChat(self, fr_name:str ):
        if (self.friendList).loc[fr_name, 'socket'] != None:
            return self.friendList.loc[fr_name, 'message']
        peerAnswer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.friendList).loc[fr_name, 'socket'] = peerAnswer
        friendIP = (self.friendList).loc[fr_name, 'ip']
        ((self.friendList).loc[fr_name, 'socket']).connect((friendIP, P2P_LISTEN_PORT))
        return self.friendList.loc[fr_name, 'message']
    
    def FindFriendbyIP(self, IP: str):
        fr_name = (self.friendList)[self.friendList["ip"] == IP]
        return fr_name.index[0]
        
    #call when send a message to other 
    def sendMessage(self, filename: str, message: str, username: str):
        print(username)
        self.sendChatMessage(filename, message, self.friendList.loc[username, 'socket'])
        filename = filename.split('/')[-1]
        if self.friendList.loc[username, 'message'] == None:
            self.friendList.loc[username, 'message'] = [{'filename': filename,
                                                        'data': message,
                                                        'sender': 0}]
        else:
            self.friendList.loc[username, 'message'].append({'filename': filename,
                                                        'data': message,
                                                        'sender': 0})
    
    def sendChatMessage(self, name: str, data: str, conn):
        conn.send(self.createChatMessage(name, data))

    def createChatMessage(self, name: str, data: str):
        if name != "":
            data = ''''''
            with open(name, "r") as f:
                for line in f:
                    data += line
            name = name.split('/')[-1]
        message = {
            'filename': name,
            'data': data
        }
        msg = json.dumps(message).encode(FORMAT)
        return msg

    #use for thread
    def receiveMessage(self, conn, name):
        try:
            while True:
                if self.isClosed:
                    break
                msg = conn.recv(2048).decode(FORMAT)
                msg = json.loads(msg)
                msg['sender'] = 1
                if self.friendList.loc[name, 'message'] == None:
                    self.friendList.loc[name, 'message'] = [msg]
                else:
                    self.friendList.loc[name, 'message'].append(msg)

                if msg["filename"] != '':
                    try:
                        os.mkdir('download')
                    except FileExistsError:
                        pass
                    with open(f"download/{msg['filename']}", "w") as file_down:
                        file_down.write(msg["data"])
                # callback to change message: param (name, msg)
                self.change_message_cb(name, msg)
        except:
            pass
        sys.exit(0)
 
