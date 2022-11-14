import socket
import threading
from sys import argv

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Client:
    def __init__(self, ip_address, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, port))
        self.msg = self.client.recv(2048).decode()
        print(self.msg)
        self.client.close()
        

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(FORMAT))
        

if __name__ == "__main__":
    print(argv[1], argv[2])
    client = Client(argv[1], int(argv[2]))
    