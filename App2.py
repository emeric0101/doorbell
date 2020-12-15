import datetime
import time
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from phone import video_frame
import PIL.Image  # run pip install Pillow
import PIL.ImageTk
from pyowm.owm import OWM


class App2(Frame):
    def update_clock(self):
        now = time.strftime("%H:%M")
        date = datetime.datetime.now()
        now_date = (str(date.day) + "/" + str(date.month) + "/" + str(date.year))
        self.label.configure(text=now)
        self.label_date.configure(text=now_date)
        self.after(1000, self.update_clock)
        if not video_frame is None:
            cv_img = video_frame
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
            self.image = Canvas()
            self.image.create_image(0, 0, image=photo, anchor=tkinter.NW)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.label = Label(text='', font=("Helvetica", 60), background="#87CEEB")
        self.label.place(x=210, y=20)
        self.label_date = Label(text='', font=("Helvetica", 25), background="#87CEEB")
        self.label_date.place(x=230, y=100)
        self.label0 = Label(text="Météo :", font=("Helvetica", 20), background="#87CEEB")  # This is the head label
        self.label1 = Label(text="Enter the City :")
        self.label2 = Label(text="Temperature :")
        self.label3 = Label(text="Humidity :")
        self.label4 = Label(text="Description  :")
        self.label0.place(x=260, y=160)
        self.label1.place()
        self.label2.place()
        self.label3.place()
        self.label4.place()
        self.update_clock()


def camera():
    open_video()
    fenetre = Tk()
    app = App2(fenetre)
    fenetre.title("Ecran d'accueil")
    fenetre.config(bg="#87CEEB")  # arriere plan bleu
    fenetre.geometry("640x480")
    fenetre.maxsize(640, 480)
    fenetre.minsize(640, 480)
    fenetre.after(1000, App2.update_clock(app))
    fenetre.mainloop()
