from tkinter import *
from PIL import ImageTk, Image

class ChatPage:
    def __init__(self, window, data):
        self.window = window
        #self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Chat Page')
        self.curChoose = StringVar()

        # frame side bar
        self.sidebar_frame = Frame(self.window, width=400, height=self.window.winfo_screenheight(), bg='#ff0000')
        self.sidebar_frame.place(x=0, y=0)


        self.lstfriendOnline = Listbox(self.sidebar_frame, width=400, font=16, fg="green")
        for i,j in data.items():
            if j != "":
                self.lstfriendOnline.insert(END, i)
        self.lstfriendOnline.bind("<<ListboxSelect>>", self.onSelect)
        self.lstfriendOnline.pack(ipady=100)

        self.lstfriendOffline = Listbox(self.sidebar_frame, width=400, font=16, fg="red")
        for i,j in data.items():
            if j == "":
                self.lstfriendOffline.insert(END, i)
        self.lstfriendOffline.bind("<<ListboxSelect>>", self.onSelect)
        self.lstfriendOffline.pack(ipady=100)

        # frame chat 
        self.chat_frame = Frame(self.window, width=self.window.winfo_screenwidth()-400, height=self.window.winfo_screenheight()-100)
        self.chat_frame.place(x=400, y=0)
        self.label = Label(self.chat_frame, text=0, textvariable=self.curChoose, font=16,)
        self.label.pack()
        # contain chat message
        self.bg_frame = Image.open('images\\background1.png').resize((self.window.winfo_screenwidth()-400,self.window.winfo_screenheight()-150))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.chat_frame, image=photo, height=self.window.winfo_screenheight()-100)
        self.bg_panel.image = photo
        self.bg_panel.pack()

        # frame for typing message
        self.typing_frame = Frame(self.window, width=self.window.winfo_screenwidth()-400, height=100, bg='#ff0000')
        self.typing_frame.place(x=402, y=self.window.winfo_screenheight()-100)
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        print(idx)
        if len(idx) != 0:
            value = sender.get(idx)
            # call start chat
            self.curChoose.set(value)
        #print(self.curChoose.get())

def page():
    window = Tk()
    ChatPage(window, {"khanh": "", "nguyen quang khanh": "192.168.0.15", "friend 007": "1111", "friend 001": ""})
    window.mainloop()


if __name__ == '__main__':
    page()
