import os
from sys import argv
import tkinter
from backend.Client import Client
from UI.signin import SigninPage
from UI.signup import SignupPage
from tkinter import *

def handle_sign_in(event):
    global page
    username = page.username_entry.get()
    password = page.password_entry.get()
    recv_msg = client.sign_in(username, password)
    print(recv_msg)
    if recv_msg['flag'] == 0:
        page.message.config(text="Incorrect username or password")

def handle_sign_up(event):
    global page
    username = page.username_entry.get()
    password = page.password_entry.get()
    recv_msg = client.sign_up(username, password)
    print(recv_msg)
    if recv_msg['flag'] == 0:
        page.message.config(text="Username already exists")

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

if __name__ == "__main__":
    client = Client(argv[1], int(argv[2]))
    window = tkinter.Tk()
    page = SigninPage(window)
    page.sign_in_button.bind('<Button-1>', handle_sign_in)
    page.sign_up_button.bind('<Button-1>', change_to_sign_up)
    window.mainloop()

