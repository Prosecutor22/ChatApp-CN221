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
    print(username, ip)

if __name__ == "__main__":
    client = Client(argv[1], int(argv[2]), change_status)
    window = tkinter.Tk()
    page = SigninPage(window)
    page.sign_in_button.bind('<Button-1>', handle_sign_in)
    page.sign_up_button.bind('<Button-1>', change_to_sign_up)
    window.mainloop()

