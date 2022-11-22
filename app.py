import os
from sys import argv
import tkinter
from backend.Client import Client
from UI.signin import SigninPage
from UI.signup import SignupPage
from UI.chat import ChatPage
from tkinter import *

def handle_sign_in(event):
    global page
    username = page.username_entry.get()
    password = page.password_entry.get()
    rcv_msg = client.sign_in(username, password)
    print(rcv_msg)
    if rcv_msg['flag'] == 0:
        page.message.config(text="Incorrect username or password", fg="red")
    else:
        page = ChatPage(window, rcv_msg['data'])
        page.sign_out_button.bind('<Button-1>', handle_sign_out)
        page.lstfriendOnline.bind("<<ListboxSelect>>", onSelect)
        page.typing_entry.bind("<Return>", change_message_from_me)
        page.send_button.bind("<Button-1>", change_message_from_me)
        
def handle_sign_up(event):
    global page
    username = page.username_entry.get()
    password = page.password_entry.get()
    rcv_msg = client.sign_up(username, password)
    print(rcv_msg)
    if rcv_msg['flag'] == 0:
        page.message.config(text="Username already exists", fg="red")
    else:
        page.message.config(text="Sign up successfully", fg="green")

def handle_sign_out(event):
    global page
    client.sign_out()
    print('[SIGN OUT]')
    page = SigninPage(window)

def change_to_sign_up(event):
    global page 
    page = SignupPage(window)
    page.sign_up_button.bind('<Button-1>', handle_sign_up)
    page.sign_in_button.bind('<Button-1>', change_to_sign_in)

def change_to_sign_in(event):
    global page 
    page = SigninPage(window)
    page.sign_in_button.bind('<Button-1>', handle_sign_in)
    page.sign_up_button.bind('<Button-1>', change_to_sign_up)

def change_status(username, ip):
    # print(username, ip)
    global page
    if ip == None:
        for index, item in enumerate(page.lstfriendOnline.get(0, END)):
            if item == username:
                page.lstfriendOnline.delete(index)

                page.lstfriendOffline.insert(END, username)
                break
    else:
        for index, item in enumerate(page.lstfriendOffline.get(0, END)):
            if item == username:
                page.lstfriendOffline.delete(index)

                page.lstfriendOnline.insert(END, username)
                break

def onSelect(event):
        sender = event.widget
        idx = sender.curselection()
        if len(idx) != 0:
            value = sender.get(idx)
            page.curChoose.set(value)

            # call start chat
            messages = client.ConnectFriendtoChat(value)
            page.message_list.delete(0, END)
            if messages == None:
                return
            for message in messages:
                if message['sender'] == 0:
                    page.message_list.insert(END, f"{message['data']} [me]".rjust(150))
                else:
                    page.message_list.insert(END, f"[{value}] {message['data']}")

def change_message_from_friend(username, message):
    global page
    if page.curChoose.get() == username:
        page.message_list.insert(END, f"[{username}] {message['data']}")

def change_message_from_me(event):
    global page
    message = page.typing_entry.get()
    page.typing_entry.delete(0, END)
    print(page.curChoose.get())
    client.sendMessage("", message, page.curChoose.get())
    page.message_list.insert(END, f"{message} [me]".rjust(150))
    

if __name__ == "__main__":
    client = Client(argv[1], int(argv[2]), change_status, change_message_from_friend)
    window = tkinter.Tk()
    page = SigninPage(window)
    page.sign_in_button.bind('<Button-1>', handle_sign_in)
    page.sign_up_button.bind('<Button-1>', change_to_sign_up)
    window.mainloop()

