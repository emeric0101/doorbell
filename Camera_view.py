import datetime
import time
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from phone import close_video
from PIL import ImageTk
from PIL import Image
import cv2
from phone import video_frame_container, open_video
import PIL.Image  # run pip install Pillow
import PIL.ImageTk
from pyowm.owm import OWM


class Timer:
    def __init__(self, parent, canvas, image):
        # variable storing time
        self.seconds = 0
        # label displaying time
        # start the timer
        self.parent = parent
        self.canvas = canvas
        self.image = image
        self.parent.after(1000, self.refresh_label)
        self.serverimage = None
        self.video_frame = None
        self.cv_img = None

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time        # display the new time
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.video_frame = video_frame_container.get_frame()
        if self.video_frame is not None:
            self.cv_img = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
            self.serverimage = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img), master=self.canvas)
            self.canvas.create_image(0, 0, image=self.serverimage)
        self.parent.after(100, self.refresh_label)


def update(image, fenetre):
    # video_frame = video_frame_container.get_frame()
    # if video_frame is not None:
    # cv_img = video_frame
    # photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    # update_img(photo, image)
    print("il se passe qqchose !")
    fenetre.after(1000, update)


def camera():
    open_video()
    fenetre = Tk()
    # app2 = App2(fenetre)
    fenetre.title("Caméra")
    fenetre.config(bg="#87CEEB")  # arriere plan bleu
    fenetre.geometry("640x480")
    fenetre.maxsize(640, 480)

    def stop_fen():
        fenetre.destroy()
        close_video()

    canvas = Canvas(fenetre, width=640, height=400)
    canvas.pack()
    render = PhotoImage(file="test.png", master=canvas)
    image = canvas.create_image(0, 0, image=render, anchor=NW)
    fenetre.resizable(0, 0)
    fenetre.minsize(640, 480)
    btn_quit_cams = Button(fenetre, text="\n     Quitter     \n", command=stop_fen)
    btn_quit_cams.place(x=270, y=410)
    timer = Timer(fenetre, canvas, image)
    fenetre.protocol('WM_DELETE_WINDOW', stop_fen)
    fenetre.mainloop()


def stop_connection():
    close_video()
