import os
from sys import argv
import sys
import tkinter
from tkinter import filedialog
from backend.Client import Client
from UI.signin import SigninPage
from UI.signup import SignupPage
from UI.chat import ChatPage
from tkinter import *
import threading
from datetime import datetime

class ClientUI():
    def __init__(self, ip, port):
        print("oke")
        self.client = Client(ip, port, self.change_status, self.change_message_from_friend)
        self.window = tkinter.Tk()
        self.page = SigninPage(self.window)
        self.page.sign_in_button.bind('<Button-1>', self.handle_sign_in)
        self.page.sign_up_button.bind('<Button-1>', self.change_to_sign_up)
        print("It oke")
    
    def run(self):
        self.window.mainloop()

    def handle_sign_in(self, event):
        username = self.page.username_entry.get()
        password = self.page.password_entry.get()
        rcv_msg = self.client.sign_in(username, password)
        #print(rcv_msg)
        if rcv_msg['flag'] == 0:
            self.page.message.config(text="Incorrect username or password", fg="red")
        else:
            self.page = ChatPage(self.window, rcv_msg['data'])
            self.page.sign_out_button.bind('<Button-1>', self.handle_sign_out)
            self.page.lstfriendOnline.bind("<<ListboxSelect>>", self.onSelect)
            self.page.typing_entry.bind("<Return>", self.change_message_from_me)
            self.page.send_button.bind("<Button-1>", self.change_message_from_me)
            self.page.file_button.bind("<Button-1>", self.handle_file_select)

    def handle_sign_up(self, event):
        username = self.page.username_entry.get()
        password = self.page.password_entry.get()
        rcv_msg = self.client.sign_up(username, password)
        #print(rcv_msg)
        if rcv_msg['flag'] == 0:
            self.page.message.config(text="Username already exists", fg="red")
        else:
            self.page.message.config(text="Sign up successfully", fg="green")

    def handle_sign_out(self, event):
        self.client.sign_out()
        print('[SIGN OUT]')
        self.window.destroy()
        # page = SigninPage(window)
        self.window.quit()

    def handle_file_select(self, event):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if self.page.curChoose.get() != '':
            #print(page.curChoose.get())
            self.client.sendMessage(filename, "", self.page.curChoose.get())
            self.page.message_list.insert(END, f"[me - {filename.split('/')[-1]}]")

    def change_to_sign_up(self, event):
        self.page = SignupPage(self.window)
        self.page.sign_up_button.bind('<Button-1>', self.handle_sign_up)
        self.page.sign_in_button.bind('<Button-1>', self.change_to_sign_in)

    def change_to_sign_in(self, event):
        self.page = SigninPage(self.window)
        self.page.sign_in_button.bind('<Button-1>', self.handle_sign_in)
        self.page.sign_up_button.bind('<Button-1>', self.change_to_sign_up)

    def change_status(self, username, ip):
        # print(username, ip)
        #print(ip)
        if ip == None:
            for index, item in enumerate(self.page.lstfriendOnline.get(0, END)):
                if item == username:
                    self.page.lstfriendOnline.delete(index)

                    self.page.lstfriendOffline.insert(END, username)
                    break
        else:
            for index, item in enumerate(self.page.lstfriendOffline.get(0, END)):
                if item == username:
                    self.page.lstfriendOffline.delete(index)

                    self.page.lstfriendOnline.insert(END, username)
                    break

    def onSelect(self, event):
            sender = event.widget
            idx = sender.curselection()
            if len(idx) != 0:
                value = sender.get(idx)
                self.page.curChoose.set(value)

                # call start chat
                messages = self.client.ConnectFriendtoChat(value)
                self.page.message_list.delete(0, END)
                if messages == None:
                    return
                for message in messages:
                    if message['sender'] == 0:
                        if message['filename'] == '':
                            self.page.message_list.insert(END, f"[me] {message['data']}")
                        else:
                            self.page.message_list.insert(END, f"[me - {message['filename']}]")
                    else:
                        if message['filename'] == '':
                            self.page.message_list.insert(END, f"[{value}] {message['data']}")
                        else:
                            self.page.message_list.insert(END, f"[{value} - {message['filename']}]")

    def change_message_from_friend(self, username, message):
        if self.page.curChoose.get() == username:
            if message['filename'] == '':
                self.page.message_list.insert(END, f"[{username}] {message['data']}")
            else:
                self.page.message_list.insert(END, f"[{username} - {message['filename']}]")

    def change_message_from_me(self, event):
        message = self.page.typing_entry.get()
        self.page.typing_entry.delete(0, END)
        if self.page.curChoose.get() != '':
            #print(page.curChoose.get())
            self.client.sendMessage("", message, self.page.curChoose.get())
            self.page.message_list.insert(END, f"[me] {message}")


# if __name__ == "__main__":
#     client = Client(argv[1], int(argv[2]), change_status, change_message_from_friend)
#     window = tkinter.Tk()
#     page = SigninPage(window)
#     page.sign_in_button.bind('<Button-1>', handle_sign_in)
#     page.sign_up_button.bind('<Button-1>', change_to_sign_up)
#     window.mainloop()
#     # print("close tkinter")
#     # for i in threading.enumerate():
#     #     print(i.getName())
if __name__ == "__main__":
    clientUI = ClientUI(argv[1], int(argv[2]))
    clientUI.run()
