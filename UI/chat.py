from tkinter import *
from PIL import ImageTk, Image
class ChatPage:
    def __init__(self, window, data, callback):
        self.window = window
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Chat Page')
        self.callback = callback
        self.window.protocol("WM_DELETE_WINDOW", self.handle_sign_out)
        self.curChoose = StringVar()
        for i in self.window.winfo_children():
            i.destroy()
    
        self.sidebar_frame = Frame(self.window, width=400, height=self.window.winfo_screenheight(), bg='#00ff00')
        self.sidebar_frame.place(x=0, y=0)


        self.lstfriendOnline = Listbox(self.sidebar_frame, width=400, font=16, fg="green")
        for i,j in data.items():
            if j != None:
                self.lstfriendOnline.insert(END, i)
        self.lstfriendOnline.pack(ipady=50)

        self.lstfriendOffline = Listbox(self.sidebar_frame, width=400, font=16, fg="red")
        for i,j in data.items():
            if j == None:
                self.lstfriendOffline.insert(END, i)
        self.lstfriendOffline.pack(ipady=50)

        self.sign_out_button = Button(self.window, text="Sign out", font=("yu gothic ui", 16, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.sign_out_button.place(x=100, y = 725)
        # frame chat 
        self.chat_frame = Frame(self.window, width=self.window.winfo_screenwidth()-400, height=self.window.winfo_screenheight()-100)
        self.chat_frame.place(x=400, y=0)
        self.label = Label(self.chat_frame, text=0, textvariable=self.curChoose, font=16,)
        self.label.place(x=0, y=0)

        self.message_list = Listbox(self.chat_frame, width=self.window.winfo_screenwidth()-400, font=("TkFixedFont", 16), fg="blue", bg="white", height=30)
        
        self.message_list.place(x=0, y=50)

        self.typing_frame = Frame(self.window, width=self.window.winfo_screenwidth()-400, height=100, bg='#b0cbf7')
        self.typing_frame.place(x=402, y=self.window.winfo_screenheight()-100)

        self.typing_entry = Entry(self.typing_frame, highlightthickness=0, relief=FLAT, bg="white", fg="black",
                                    font=("yu gothic ui ", 16, "bold"))
        self.typing_entry.place(x=40, y=30, width=650)

        self.send_button = Button(self.typing_frame, text="Send", font=("yu gothic ui", 16, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.send_button.place(x=710, y = 20)

        self.file_button = Button(self.typing_frame, text="Send File", font=("yu gothic ui", 16, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.file_button.place(x=940, y = 20)

    def handle_sign_out(self):
        self.callback()
        print('[SIGN OUT]')
        self.window.destroy()
        self.window.quit()

def page():
    window = Tk()
    ChatPage(window, {"khanh": None, "nguyen quang khanh": "192.168.0.15", "friend 007": "1111", "friend 001": None})
    window.mainloop()


if __name__ == '__main__':
    page()
