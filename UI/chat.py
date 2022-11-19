from tkinter import *
from PIL import ImageTk, Image

class ChatPage:
    def __init__(self, window):
        self.window = window
        #self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Chat Page')
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(expand='yes')

        # frame list friend
        self.lstfriend_frame = Frame(self.bg_panel, bg='#111111', width=300, height=768)
        self.lstfriend_frame.place(x=0, y=0)

        # frame chat 
        self.chat_frame = Frame(self.bg_panel, bg='#111111', width=1066, height=768, background='#111111')
        self.chat_frame.place(x=300, y=0)


def page():
    window = Tk()
    ChatPage(window)
    window.mainloop()


if __name__ == '__main__':
    page()
