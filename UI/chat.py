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
        self.sidebar_frame = Frame(self.window, width=200, height=self.window.winfo_screenheight(), bg='#ff0000')
        self.sidebar_frame.place(x=0, y=0)


        self.lstfriend = Listbox(self.sidebar_frame, width=200, font=14)
        for i,j in data.items():
            status = "offline" if j == None else "online"
            self.lstfriend.insert(END, f"{i}\t\t[{status}]")
        self.lstfriend.bind("<<ListboxSelect>>", self.onSelect)
        self.lstfriend.pack(ipady=100)

        # frame chat 
        self.chat_frame = Frame(self.window, width=self.window.winfo_screenwidth()-200, height=self.window.winfo_screenheight()-100)
        self.chat_frame.place(x=200, y=0)
        self.label = Label(self.chat_frame, text=0, textvariable=self.curChoose, font=14,)
        self.label.pack()
        # contain chat message
        self.bg_frame = Image.open('images\\background1.png').resize((self.window.winfo_screenwidth()-200,self.window.winfo_screenheight()-150))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.chat_frame, image=photo, height=self.window.winfo_screenheight()-100)
        self.bg_panel.image = photo
        self.bg_panel.pack()

        # frame for typing message
        self.typing_frame = Frame(self.window, width=self.window.winfo_screenwidth()-200, height=100, bg='#ff0000')
        self.typing_frame.place(x=200, y=self.window.winfo_screenheight()-100)
    
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        #call start chat
        self.curChoose.set(value)
        #print(self.curChoose.get())

def page():
    window = Tk()
    ChatPage(window, {"ban1": 0, "ban2": 1})
    window.mainloop()


if __name__ == '__main__':
    page()
