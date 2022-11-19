import os
from sys import argv
import tkinter
from backend.Client import Client
from UI.signin import SigninPage
from UI.signup import SignupPage

def handle_sign_in(event):
    global page, client
    username = page.username_entry.get()
    password = page.password_entry.get()
    recv_msg = client.sign_in(username, password)
    print(recv_msg)

def change_to_sign_in(event):
    pass

if __name__ == "__main__":
    client = Client(argv[1], int(argv[2]))
    window = tkinter.Tk()
    page = SigninPage(window)
    page.sign_in_button.bind('<Button-1>', handle_sign_in)
    page.sign_up_button.bind('<Button-1>', lambda event: print(event), )
    window.mainloop()
