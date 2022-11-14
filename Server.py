import socket
from sys import argv
import threading
import csv
import os

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Server:
    def __init__(self, ip_address: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip_address, port))
        self.server.listen(100)
        print("ok")
        self.fileName = os.getcwd() + '\Data\Server\clientData.csv'

    
    def searchUserName(self, username: str):
        with open(self.fileName, 'a+') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == username:
                    return row
        return None
    
    # return 1 if register OK, else 0
    def addNewUser(self, username: str, password: str):
        if self.searchUserName(username) != None:
            return 0
        userData = [username, password, None, None]
        with open(self.fileName, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(userData)        
        return 1  
      
    # return 1 if authenticate successfully else 0
    def authenticate(self, username: str, password: str) -> int:
        user = self.searchUserName(username)
        if user == None or password != user[1]:
            return 0
        return 1
    
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
        conn.close()
    
    def run(self):
        while True:
            (conn, addr) = self.server.accept()
            print(conn, addr)
            # thread = threading.Thread(target=self.handle_client, args=(conn,addr))
            # self.thread.run()
            conn.send(b"Welcome to hell")
            conn.close()
                    

if __name__ == "__main__":
    (Server(argv[1], int(argv[2]))).run()